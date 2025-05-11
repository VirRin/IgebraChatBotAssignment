import os
import json
import re
from flask import Flask, request, jsonify, render_template
from groq import Groq
from typing import List
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
CONTENT_PATH = os.path.join(BASE_DIR, 'educational_content.txt')

# Default educational content
DEFAULT_CONTENT = """Education System Overview
1. Primary Education (Grades 1-5)
• Focuses on foundational skills
• Core subjects: Reading, Writing, Math, Science

2. Secondary Education (Grades 6-12)
• Prepares students for college/career
• Includes electives and advanced courses

3. Teaching Methods
• Active learning strategies
• Technology integration
• Differentiated instruction"""

def ensure_files_exist():
    """Create required files if they don't exist."""
    if not os.path.exists(CONTENT_PATH):
        with open(CONTENT_PATH, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_CONTENT)
    
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump({"GROQ_API_KEY": "your-api-key-here"}, f)
        raise ValueError("Please configure your GROQ_API_KEY in config.json")

def load_educational_content():
    """Load and chunk educational content."""
    try:
        with open(CONTENT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        return chunk_text(content)
    except Exception as e:
        print(f"Error loading content: {e}")
        return chunk_text(DEFAULT_CONTENT)

def chunk_text(text: str, chunk_size: int = 1500) -> List[str]:
    """Split content into pedagogically meaningful chunks."""
    chunks = []
    current_chunk = []
    current_length = 0
    
    # Split by paragraphs or major sections
    paragraphs = re.split(r'\n\s*\n', text)
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        para_length = len(para)
        if current_length + para_length > chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_length = 0
            
        current_chunk.append(para)
        current_length += para_length
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

# Initialize application
ensure_files_exist()
try:
    config = json.load(open(CONFIG_PATH))
    client = Groq(api_key=config["GROQ_API_KEY"])
except Exception as e:
    print(f"Initialization error: {e}")
    client = None

edu_chunks = load_educational_content()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    if not client:
        return jsonify({"error": "Service unavailable"}), 503
    
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({"error": "Empty query"}), 400
        
        # Find relevant educational context
        relevant_context = find_relevant_content(user_query, edu_chunks)
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an expert educational assistant. Provide accurate, 
                    structured responses based on this context:\n\n{relevant_context}\n\n
                    Guidelines:
                    - Be concise but thorough
                    - Use markdown formatting
                    - Suggest additional resources when helpful"""
                },
                {"role": "user", "content": user_query}
            ],
            temperature=0.6,
            max_tokens=1024
        )
        
        return jsonify({
            "response": response.choices[0].message.content
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def find_relevant_content(query: str, chunks: List[str], top_n: int = 2) -> str:
    """Find most relevant educational content for the query."""
    query_terms = set(word.lower() for word in re.findall(r'\w+', query))
    scored_chunks = []
    
    for chunk in chunks:
        chunk_terms = set(word.lower() for word in re.findall(r'\w+', chunk))
        score = len(query_terms & chunk_terms)
        
        # Boost score if terms appear in headings
        first_line = chunk.split('\n')[0].lower()
        first_line_terms = set(word.lower() for word in re.findall(r'\w+', first_line))
        score += 2 * len(query_terms & first_line_terms)
        
        scored_chunks.append((score, chunk))
    
    # Return top N chunks
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    return "\n\n".join(chunk for score, chunk in scored_chunks[:top_n])

@app.route('/api/content', methods=['GET', 'POST'])
def manage_content():
    """Endpoint to get or update educational content."""
    try:
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
            
            new_content = request.json.get('content')
            if not new_content:
                return jsonify({"error": "Content cannot be empty"}), 400
                
            with open(CONTENT_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            global edu_chunks
            edu_chunks = chunk_text(new_content)
            return jsonify({"message": "Content updated successfully"})
        
        # GET request
        with open(CONTENT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# Bengali Family Health FAQ Assistant (Flask + Groq)

This project is a web-based chatbot application designed to answer questions related to Bengali family health. It uses the **Groq API** for generating intelligent responses and processes a pre-defined FAQ dataset for retrieving relevant answers.

## Features
- **Intelligent Chatbot:** Powered by the Groq API.
- **Language Support:** Responds in **Bengali** and **English**.
- **FAQ-Based Responses:** Focused on family health-related FAQs.
- **Content-Driven Retrieval:** Uses a pre-loaded FAQ content file (`book.txt`) for contextual answers.
- **Backend Framework:** Flask with CORS support for cross-origin requests.

---

## Prerequisites

Before running the project, ensure you have the following installed:
- Python 3.12 or later.
- A valid Groq API key.
- The following Python libraries:
  - Flask
  - Flask-CORS
  - Groq API SDK
- A text file named `book.txt` containing FAQ content, placed in the project directory.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/flask-family-health-chatbot.git
cd flask-family-health-chatbot
```

### 2. Install the Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Your Groq API Key
1. Create a file named `config.json` in the root directory.
2. Add the following content to the file:
   ```json
   {
       "GROQ_API_KEY": "your-groq-api-key-here"
   }
   ```

---

## Usage

### Run the Application
To start the Flask application, use the following command:
```bash
python app.py
```

### Access the Chatbot
The chatbot will be available locally at:
```
http://127.0.0.1:5000
```

---

## Deployment

To deploy this application, you can use platforms like **Vercel**, **Heroku**, or any Flask-compatible hosting service.

1. Ensure your `requirements.txt` file is up to date:
   ```bash
   pip freeze > requirements.txt
   ```

2. Follow the hosting platform's deployment instructions, ensuring the `book.txt` and `config.json` files are included.

---

## Troubleshooting

1. **Dependency Issues:**
   If there are issues installing dependencies, ensure they are compatible with Python 3.12. Run:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Groq API Errors:**
   - Verify your API key in `config.json`.
   - Check your usage limits and model availability on the Groq dashboard.

3. **File Not Found (book.txt):**
   Ensure the `book.txt` file is in the project root directory.

---

## Future Enhancements
- Add NLP techniques for more accurate context retrieval.
- Enable user authentication for personalized responses.
- Support for additional languages beyond Bengali and English.

---

## License
This project is licensed under the MIT License.

---

# AI-Powered Customer Support FAQ Assistant

An intelligent customer support chatbot built using Python, Streamlit, and Machine Learning techniques. The system uses TF-IDF vectorization and cosine similarity to identify relevant answers from a predefined FAQ knowledge base.

## Project Overview

The AI-Powered Customer Support FAQ Assistant is designed to automate responses to frequently asked customer questions.

Users can enter questions through an interactive chat interface. The system processes the question, compares it with stored FAQs, and returns the most relevant answer. If the similarity score is below the configured confidence threshold, the chatbot provides a fallback response.

## Objectives

- Automate frequently asked customer support queries.
- Build a searchable FAQ knowledge base.
- Use NLP techniques for question matching.
- Retrieve answers using cosine similarity.
- Handle questions outside the knowledge base.
- Store chat history and user feedback using SQLite.
- Provide an administrative interface to manage FAQs.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web-based user interface |
| Scikit-learn | Machine learning and text vectorization |
| TF-IDF | Text feature extraction |
| Cosine Similarity | Question matching |
| Pandas | FAQ dataset management |
| NumPy | Numerical operations |
| SQLite | Database and feedback storage |

## Key Features

1. **Interactive Chatbot:** Allows users to ask questions through a web interface.
2. **FAQ Matching:** Uses TF-IDF and cosine similarity to find relevant questions.
3. **Automated Responses:** Retrieves answers from the FAQ dataset.
4. **Fallback Mechanism:** Handles questions that do not match the knowledge base confidently.
5. **Admin Dashboard:** Supports adding, editing, deleting, and searching FAQs.
6. **Chat History:** Stores user queries and response information.
7. **User Feedback:** Allows users to provide feedback on chatbot answers.
8. **Performance Statistics:** Displays response and chatbot usage statistics.

## Project Structure

```text
FAQ_Assistant/
│
├── app.py
├── admin.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── faqs.csv
│
├── modules/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── retrieval.py
│   └── database.py
│
└── database/
    └── faq_database.db
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Powered-Customer-Support-FAQ-Assistant.git
```

### 2. Navigate to the Project Folder

```bash
cd AI-Powered-Customer-Support-FAQ-Assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the Chatbot

```bash
python -m streamlit run app.py
```

### 7. Run the Admin Dashboard

Open another terminal, activate the virtual environment, and execute:

```bash
python -m streamlit run admin.py
```

## Working Methodology

1. The user enters a question in the chatbot.
2. The input question is cleaned using text preprocessing.
3. TF-IDF converts FAQ questions into numerical vectors.
4. Cosine similarity compares the user's question with stored FAQ questions.
5. The system identifies the highest-scoring FAQ.
6. If the similarity score meets the confidence threshold, the corresponding answer is displayed.
7. Otherwise, a fallback response is generated.
8. Chat information and feedback are stored in SQLite.

## Sample Test Questions

- How can I request a refund?
- Where can I track my order?
- How do I reset my password?
- How can I enroll in a course?
- How can I contact customer support?

An unrelated question, such as "Who won the FIFA World Cup?", can be used to test the fallback mechanism.

## Future Enhancements

- Integration with Large Language Models (LLMs).
- Multilingual customer support.
- Voice-based question input.
- Advanced semantic search using sentence embeddings.
- Deployment on cloud platforms.
- Improved analytics and reporting.

## Project Information

**Project Name:** AI-Powered Customer Support FAQ Assistant

**Programming Language:** Python

**Project Type:** Machine Learning / Natural Language Processing

**Interface:** Streamlit

**Database:** SQLite

**Purpose:** Academic project and demonstration of an intelligent FAQ-based customer support system.

## License

This project is developed for educational and academic purposes.
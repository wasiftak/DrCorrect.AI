
# 🧠 DrCorrect.AI - Medical Terminology Assistant

DrCorrect.AI is a web-based text editor designed to assist medical professionals, students, and researchers in writing accurate and efficient clinical notes 🩺. It combines a real-time medical spell-checker with a powerful AI assistant to provide suggestions, automatic corrections, and in-depth text analysis.

The application features a modern, minimalist user interface inspired by digital notebooks, creating a focused and pleasant writing environment.

## 🚀 Live Demo
You can try DrCorrect.AI live at the following URL:

https://drcorrect-ai.onrender.com/

## ✨ Key Features

  - **📝 Real-time Medical Spelling Suggestions:** As you type, the application suggests completions for medical terms from a comprehensive vocabulary, helping to speed up your writing process.
  - **🪄 Intelligent Auto-Correction:** Automatically corrects common misspellings for medical terms if there is only one clear and unambiguous correction available.
  - **🤖 AI-Powered Text Analysis:** Select any portion of your text and use the integrated AI assistant (powered by the Google Gemini API) to get a detailed analysis, definition, or explanation of the medical concepts.
  - **🎨 Modern User Interface:** A clean, notebook-style interface with a dark toolbar and a large, clear font for a comfortable writing experience.
  - **👆 Simple and Intuitive Controls:** Easily analyze, copy, or clear your text with dedicated buttons in the toolbar.

## 🛠️ Tech Stack

  - **Backend:** 🐍 Python with Flask
  - **Frontend:** 🌐 HTML5, CSS3, JavaScript
  - **AI Integration:** 🤖 Google Gemini API
  - **Core Logic:** Custom Python modules for text processing (`text_processor.py`) and AI interaction (`ai_helper.py`).

## ⚙️ Setup and Installation

Follow these steps to set up and run the project on your local machine.

### 1\. Prerequisites

  - Python 3.8 or higher
  - `pip` for package management
  - A Google Gemini API Key

### 2\. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 3\. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4\. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5\. Set Up Environment Variables

The application requires a Google Gemini API key to power its AI features. You need to set this as an environment variable.

```bash
# For macOS/Linux
export GEMINI_API_KEY="your_api_key_here"

# For Windows
set GEMINI_API_KEY="your_api_key_here"
```

### 6\. Run the Application

Once the setup is complete, you can run the Flask web server.

```bash
python app.py
```

🚀 The application will be running at `http://127.0.0.1:5000`. Open this URL in your web browser to start using DrCorrect.AI.

## 💡 How to Use

  - **Typing Area:** Simply start typing your medical notes in the main text area.
  - **Autocomplete:** If you type a word that's three or more characters long, a suggestion box will appear. You can use the `ArrowUp`/`ArrowDown` keys and `Enter` or `Tab` to accept a suggestion.
  - **Autocorrect:** When you press the spacebar, the application will check the previously typed word and automatically correct it if a clear correction is found.
  - **AI Analysis:** Select any text in the editor and click the **sparkle icon** (`✨`) in the top-right toolbar. The analysis will appear in the "AI Assistant" sidebar on the right.

## 📁 Project Structure

```
/
|-- app.py                  # Main Flask application file
|-- text_processor.py         # Handles spelling, suggestions, and corrections
|-- ai_helper.py              # Manages communication with the Gemini API
|-- medical_vocabulary.txt    # The dictionary of medical terms
|-- requirements.txt          # Project dependencies
|-- /static
|   |-- /css
|   |   |-- style.css         # All styling for the application
|   |-- /js
|       |-- script.js       # Frontend logic for interactivity
|-- /templates
    |-- index.html            # The main and only HTML page
```

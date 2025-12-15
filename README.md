# 📄 Document Word and Adjective Analyzer

This is a desktop application built with Python's Tkinter and the Natural Language Toolkit (NLTK). It allows users to upload a PDF or DOCX file, performs a text analysis in a separate thread to prevent GUI lockup, and generates a report detailing:

1.  **Total Word Count**
2.  **Top 10 Most Frequent Adjectives** (using Part-of-Speech Tagging)

## ✨ Features

* **GUI Interface:** Easy-to-use desktop interface built with Tkinter.
* **File Support:** Supports both `.pdf` and `.docx` file formats.
* **Non-Blocking Analysis:** Analysis is run in a separate thread (`threading`) to keep the GUI responsive during processing of large files.
* **NLTK Integration:** Uses `nltk` for tokenization and Part-of-Speech tagging to accurately identify adjectives.

## 🚀 Getting Started

Follow these steps to set up and run the application on your local machine.

### Prerequisites

You need Python 3.6+ installed.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/document-analyzer-app.git](https://github.com/YourUsername/document-analyzer-app.git)
    cd document-analyzer-app
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The script will automatically download the necessary NLTK data resources (`punkt`, `averaged_perceptron_tagger`, etc.) when it runs for the first time.*

### Running the Application

Execute the main Python script from your terminal:

```bash
python gui_analyzer.py
```

## 💻 Project Structure
```
document-analyzer-app/
├── gui_analyzer.py        # The main application script
├── requirements.txt       # List of Python dependencies (pypdf, python-docx, nltk)
├── .gitignore             # Files and directories to ignore for Git
└── README.md              # Project information and setup instructions
```

## ⚙️ Git Commands to Setup

Assuming you have initialized a local Git repository and created the files above, use these commands to push your project to a remote service like GitHub:

1.  **Initialize Git in your project folder (if not already done):**
    ```bash
    git init
    ```

2.  **Add all necessary files to the staging area:**
    ```bash
    git add gui_analyzer.py requirements.txt .gitignore README.md
    ```

3.  **Commit the initial files:**
    ```bash
    git commit -m "Initial commit: Add document analyzer app and setup files."
    ```

4.  **Connect to your remote repository and push (Replace placeholders):**
    ```bash
    git remote add origin https://github.com/YourUsername/document-analyzer-app.git
    git push -u origin main
    ```
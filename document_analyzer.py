import os
import re
from collections import Counter
from pypdf import PdfReader
from docx import Document
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# --- 1. Dedicated NLTK Setup Function ---
def setup_nltk_resources():
    """
    Ensures all necessary NLTK data (punkt and averaged_perceptron_tagger) 
    are downloaded before any NLP operations begin. This version is highly robust 
    against missing resources.
    """
    resources_to_download = [
        'punkt', 
        'averaged_perceptron_tagger', 
        # Including the specific English version as a backup check
        'averaged_perceptron_tagger_eng' 
    ]
    
    print("Checking and downloading NLTK resources...")
    
    for resource_name in resources_to_download:
        try:
            # Try to find the resource using its standard path (often just the name works)
            # This check can sometimes fail even if the data is there, but we try it first.
            nltk.data.find(f'taggers/{resource_name}') 
            # If find succeeds, we can skip the download printout
            # print(f"'{resource_name}' is already available.")
            continue
        except LookupError:
             # If the resource is not found, download it
            print(f"Downloading required NLTK resource: '{resource_name}'...")
            try:
                # Use quiet=True to minimize terminal spam
                nltk.download(resource_name, quiet=True)
                print(f"'{resource_name}' downloaded successfully.")
            except Exception as e:
                # This block handles critical download failures
                print(f"FATAL ERROR: Could not download {resource_name}. Error: {e}")
                # Re-raise the error to stop the program, as we can't proceed without it.
                raise

    print("NLTK setup complete.")
# ----------------------------------------------------

def get_document_text(file_path):
    """Extracts text from a PDF or DOCX file."""
    if not os.path.exists(file_path):
        return f"Error: File not found at path: {file_path}"
        
    _, file_extension = os.path.splitext(file_path)
    text = ""

    if file_extension.lower() == '.pdf':
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        except Exception as e:
            return f"Error reading PDF: {e}"

    elif file_extension.lower() == '.docx':
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
        except Exception as e:
            return f"Error reading DOCX: {e}"

    else:
        return f"Unsupported file type: {file_extension}. Please use .pdf or .docx"

    return text

def analyze_text(text):
    """
    Performs word count and adjective frequency analysis using POS tagging.
    """
    # 1. Tokenization (Requires 'punkt')
    tokens = word_tokenize(text)
    
    # Filter for words only (basic cleaning using regex)
    words = [word.lower() for word in tokens if re.fullmatch(r'\w+', word)]
    total_word_count = len(words)

    # 2. Part-of-Speech Tagging (Requires 'averaged_perceptron_tagger')
    tagged_words = pos_tag(tokens)
    

    # Filter for adjectives. 'JJ' tags indicate adjectives (JJ, JJR, JJS)
    adjectives = [word.lower() for word, tag in tagged_words if tag.startswith('JJ')]

    # 3. Adjective Scoreboard
    adjective_counts = Counter(adjectives)
    top_adjectives = adjective_counts.most_common(10)

    return total_word_count, top_adjectives

def generate_markdown_report(word_count, top_adjectives, file_path):
    """Generates the analysis results in Markdown format."""
    markdown = f"## 📄 Document Analysis Report\n\n"
    markdown += f"**File Analyzed:** `{os.path.basename(file_path)}`\n\n"
    markdown += "---\n\n"
    
    # 1. Total Word Count
    markdown += f"### ✅ Total Word Count\n\n"
    markdown += f"The document contains **{word_count:,}** words.\n\n"
    
    # 2. Adjective Scoreboard
    markdown += f"### 🏆 Top 10 Adjective Scoreboard\n\n"
    
    if not top_adjectives:
        markdown += "No adjectives were found in the document to display a scoreboard.\n"
    else:
        # Create a Markdown Table
        markdown += "| Rank | Adjective | Count |\n"
        markdown += "| :--- | :-------- | :---- |\n"
        
        for rank, (adjective, count) in enumerate(top_adjectives, 1):
            markdown += f"| {rank} | **{adjective}** | {count} |\n"
            
    return markdown

def main_app():
    """Main function to handle user input and run the application."""
    
    # Run the NLTK setup first! This is the most critical part.
    try:
        setup_nltk_resources()
    except Exception:
        print("\n\nApplication halted due to NLTK setup failure. Please fix the download error and rerun.")
        return

    print("\n" + "=" * 50)
    print("      Python Document Word and Adjective Analyzer")
    print("=" * 50)
    
    # --- Ask for User Input ---
    while True:
        file_path = input("Enter the full path to your DOCX or PDF file: ")
        
        if not file_path:
            print("Path cannot be empty. Please try again.")
            continue
            
        file_path = file_path.strip().strip('\'"') 

        document_text = get_document_text(file_path)
        
        # Check for errors from file reading
        if isinstance(document_text, str) and (document_text.startswith("Error") or document_text.startswith("Unsupported")):
            print("\n--- Document Processing Failed ---")
            print(document_text)
            print("-" * 35)
        else:
            break

    # Perform analysis
    print("\nAnalyzing document... Please wait.")
    word_count, top_adjectives = analyze_text(document_text)

    # Generate and print the Markdown report
    markdown_report = generate_markdown_report(word_count, top_adjectives, file_path)
    
    print("\n" + "=" * 50)
    print("       🎉 Analysis Complete - Markdown Report 🎉")
    print("=" * 50)
    print(markdown_report)

if __name__ == "__main__":
    main_app()
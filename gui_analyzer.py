import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from collections import Counter
from pypdf import PdfReader
from docx import Document
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# ==============================================================================
# 1. CORE ANALYSIS & NLTK SETUP (from previous version)
# ==============================================================================

def setup_nltk_resources():
    """Ensures necessary NLTK data are downloaded."""
    resources_to_download = [
        'punkt', 
        'averaged_perceptron_tagger', 
        'averaged_perceptron_tagger_eng' 
    ]
    
    # Check if download is required before proceeding
    for resource_name in resources_to_download:
        try:
            # Check for resource existence
            nltk.data.find(f'taggers/{resource_name}') 
        except LookupError:
            # If not found, download it silently
            try:
                nltk.download(resource_name, quiet=True)
            except Exception as e:
                # If download fails, raise a critical error
                raise Exception(f"Failed to download NLTK resource '{resource_name}': {e}")
            
# Run NLTK setup once at the start
try:
    setup_nltk_resources()
except Exception as e:
    # If NLTK setup fails, print the error and exit the script
    print(f"CRITICAL ERROR during NLTK setup: {e}")
    # We can't use Tkinter's messagebox yet, so print to terminal
    exit()

def get_document_text(file_path):
    """Extracts text from a PDF or DOCX file."""
    # ... (Keep this function exactly the same as before) ...
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
    """Performs word count and adjective frequency analysis."""
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if re.fullmatch(r'\w+', word)]
    total_word_count = len(words)

    # Part-of-Speech Tagging
    tagged_words = pos_tag(tokens)

    # Filter for adjectives. 'JJ' tags indicate adjectives
    adjectives = [word.lower() for word, tag in tagged_words if tag.startswith('JJ')]

    # Adjective Scoreboard
    adjective_counts = Counter(adjectives)
    top_adjectives = adjective_counts.most_common(10)

    return total_word_count, top_adjectives

def generate_markdown_report(word_count, top_adjectives, file_path):
    """Generates the analysis results in Markdown format."""
    # ... (Keep this function exactly the same as before) ...
    markdown = f"## 📄 Document Analysis Report\n\n"
    markdown += f"**File Analyzed:** `{os.path.basename(file_path)}`\n\n"
    markdown += "---\n\n"
    
    markdown += f"### ✅ Total Word Count\n\n"
    markdown += f"The document contains **{word_count:,}** words.\n\n"
    
    markdown += f"### 🏆 Top 10 Adjective Scoreboard\n\n"
    
    if not top_adjectives:
        markdown += "No adjectives were found in the document to display a scoreboard.\n"
    else:
        markdown += "| Rank | Adjective | Count |\n"
        markdown += "| :--- | :-------- | :---- |\n"
        
        for rank, (adjective, count) in enumerate(top_adjectives, 1):
            markdown += f"| {rank} | **{adjective}** | {count} |\n"
            
    return markdown

# ==============================================================================
# 2. TKINTER GUI APPLICATION CLASS
# ==============================================================================

class DocumentAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Word & Adjective Analyzer")
        master.geometry("600x400") # Set initial window size
        master.resizable(False, False)

        self.file_path = ""
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')

        # --- Frames ---
        self.main_frame = ttk.Frame(master, padding="20 20 20 20")
        self.main_frame.pack(fill='both', expand=True)

        self.initial_screen()

    def clear_frame(self):
        """Destroys all widgets in the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- Screen 1: File Selection ---
    def initial_screen(self):
        self.clear_frame()

        # Title
        ttk.Label(self.main_frame, text="Document Word and Adjective Analyzer", 
                  font=("Helvetica", 16, "bold")).pack(pady=20)

        # File path display
        self.path_var = tk.StringVar(value="No file selected.")
        ttk.Label(self.main_frame, textvariable=self.path_var, wraplength=550, 
                  font=("Helvetica", 10)).pack(pady=10)

        # Browse Button
        self.browse_button = ttk.Button(self.main_frame, text="Select Document (.pdf or .docx)", 
                                        command=self.browse_file, width=35)
        self.browse_button.pack(pady=10)

        # Analyze Button
        self.analyze_button = ttk.Button(self.main_frame, text="Analyze Document", 
                                         command=self.start_analysis, state=tk.DISABLED, width=35)
        self.analyze_button.pack(pady=20)
        
        ttk.Label(self.main_frame, text="Powered by Python & NLTK").pack(side=tk.BOTTOM, pady=5)


    def browse_file(self):
        # Open file dialog limited to DOCX and PDF
        file_path = filedialog.askopenfilename(
            defaultextension=".pdf",
            filetypes=[("Documents", "*.pdf *.docx")]
        )
        if file_path:
            self.file_path = file_path
            self.path_var.set(os.path.basename(file_path))
            self.analyze_button.config(state=tk.NORMAL)
        else:
            self.file_path = ""
            self.path_var.set("No file selected.")
            self.analyze_button.config(state=tk.DISABLED)

    # --- Screen 2: Analysis Animation/Progress ---
    def start_analysis(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file before analyzing.")
            return

        self.clear_frame()
        self.master.title("Analyzing...")

        ttk.Label(self.main_frame, text="Analyzing Document...", 
                  font=("Helvetica", 16, "bold")).pack(pady=40)

        # Animation Placeholder (using a determinate progressbar for visual feedback)
        self.progress_bar = ttk.Progressbar(self.main_frame, orient='horizontal', 
                                            length=300, mode='indeterminate')
        self.progress_bar.pack(pady=20)
        self.progress_bar.start(10) # Starts the progress animation

        ttk.Label(self.main_frame, text="This may take a few moments for large files.").pack(pady=10)

        # Start analysis in a separate thread
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.start()

    def run_analysis(self):
        """Function run in a separate thread to prevent GUI lockup."""
        
        # 1. Extract Text
        document_text = get_document_text(self.file_path)
        
        if isinstance(document_text, str) and (document_text.startswith("Error") or document_text.startswith("Unsupported")):
            # Analysis failed, update GUI on the main thread
            self.master.after(0, lambda: self.show_error_result(document_text))
            return
            
        # 2. Analyze Text
        try:
            word_count, top_adjectives = analyze_text(document_text)
            
            # 3. Generate Report
            report = generate_markdown_report(word_count, top_adjectives, self.file_path)
            
            # Analysis successful, update GUI on the main thread
            self.master.after(0, lambda: self.final_result_screen(report))
            
        except Exception as e:
            # Analysis failed due to an unexpected error (e.g., NLTK issue after check)
            error_msg = f"Unexpected analysis error: {str(e)}"
            self.master.after(0, lambda: self.show_error_result(error_msg))

    def show_error_result(self, error_msg):
        """Displays a message if analysis fails."""
        self.progress_bar.stop()
        self.clear_frame()
        messagebox.showerror("Analysis Failed", error_msg)
        self.initial_screen() # Return to the start screen

    # --- Screen 3: Results Display (Final Screen) ---
    def final_result_screen(self, report):
        self.progress_bar.stop()
        self.clear_frame()
        self.master.title("Analysis Results")

        ttk.Label(self.main_frame, text="✅ Analysis Complete!", 
                  font=("Helvetica", 16, "bold"), foreground="green").pack(pady=10)
        
        # Display the results (using a Text widget for the Markdown report)
        report_label = ttk.Label(self.main_frame, text="Report (Markdown Format):", font=("Helvetica", 10, "bold"))
        report_label.pack(anchor='w', padx=5, pady=(15, 5))
        
        # Create a scrollable Text widget for the report
        text_frame = ttk.Frame(self.main_frame)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.report_text = tk.Text(text_frame, wrap='word', height=15, width=70, 
                                   yscrollcommand=scrollbar.set, font=("Courier", 10))
        self.report_text.insert(tk.END, report)
        self.report_text.config(state=tk.DISABLED) # Make it read-only
        self.report_text.pack(side=tk.LEFT, fill='both', expand=True)
        
        scrollbar.config(command=self.report_text.yview)

        # Back to Start Button
        ttk.Button(self.main_frame, text="Analyze Another Document", 
                   command=self.initial_screen, width=30).pack(pady=15)
        
# ==============================================================================
# 3. RUN THE APPLICATION
# ==============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentAnalyzerGUI(root)
    root.mainloop()
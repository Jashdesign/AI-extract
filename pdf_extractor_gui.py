import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from test import PDFTextExtractor  # Assuming your core logic is saved in this file

class PDFExtractorApp:
    def __init__(self, root):
        self.extractor = PDFTextExtractor()
        self.root = root
        self.root.title("PDF Text Extractor")
        self.root.geometry("800x600")

        self._create_widgets()

    def _create_widgets(self):
        # Top label
        self.label = tk.Label(self.root, text="Select a PDF to extract text from:", font=("Arial", 14))
        self.label.pack(pady=10)

        # Button to select PDF
        self.select_btn = tk.Button(self.root, text="Choose PDF", command=self.choose_pdf, font=("Arial", 12))
        self.select_btn.pack(pady=5)

        # Text display area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 10))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Save button
        self.save_btn = tk.Button(self.root, text="Save Extracted Text", command=self.save_text, state=tk.DISABLED)
        self.save_btn.pack(pady=5)

    def choose_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.text_area.delete(1.0, tk.END)
            threading.Thread(target=self.extract_text, args=(file_path,), daemon=True).start()

    def extract_text(self, pdf_path):
        self.text_area.insert(tk.END, "Extracting text...\nPlease wait...\n\n")
        extracted_text = self.extractor.extract_text(pdf_path)
        if extracted_text:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, extracted_text)
            self.save_btn.config(state=tk.NORMAL)
            self.last_pdf_path = pdf_path
        else:
            self.text_area.delete(1.0, tk.END)
            messagebox.showerror("Error", "Failed to extract text from the PDF.")

    def save_text(self):
        if hasattr(self, 'last_pdf_path'):
            output_path = os.path.splitext(self.last_pdf_path)[0] + "_extracted.txt"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Saved", f"Text saved to:\n{output_path}")

def main():
    root = tk.Tk()
    app = PDFExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
# PDF Text Extraction Tool

A Python tool for extracting text from both digital and scanned PDFs, with automatic OCR fallback for image-based documents.

## Features

- 📄 **Universal PDF Support**: Handles both text-based and scanned PDFs
- 🔍 **Automatic OCR**: Falls back to Tesseract OCR when text extraction fails
- 🏗 **Structure Analysis**: Detects sections, tables, and lists in documents
- 💾 **Metadata Extraction**: Preserves document metadata (author, title, etc.)
- 📂 **Batch Processing**: Can process multiple PDFs in a directory

## Installation

### Prerequisites
- Python 3.6+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (for scanned PDFs)

### Install dependencies
```bash
pip install PyPDF2 pytesseract pdf2image pillow pandas
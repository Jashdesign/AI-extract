import os
import sys
from typing import Optional
import PyPDF2
import pytesseract
from PIL import Image
import pdf2image
import io

class PDFTextExtractor:
    def __init__(self):
        self._verify_dependencies()
        
    def _verify_dependencies(self):
        """Check required dependencies are installed"""
        try:
            pytesseract.get_tesseract_version()
        except EnvironmentError:
            print("Tesseract OCR is not installed or not in PATH")
            print("Install from https://github.com/UB-Mannheim/tesseract/wiki")
            sys.exit(1)

    def extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF file
        Args:
            pdf_path: Path to PDF file
        Returns:
            Extracted text or None if failed
        """
        if not os.path.exists(pdf_path):
            print(f"Error: File not found at {pdf_path}")
            return None

        try:
            # First try direct text extraction (for text-based PDFs)
            text = self._extract_text_from_pdf(pdf_path)
            
            # If little/no text found, try OCR (for scanned PDFs)
            if not text or len(text.strip()) < 50:
                print("Attempting OCR extraction...")
                ocr_text = self._extract_text_with_ocr(pdf_path)
                text = f"{text}\n\n[OCR EXTRACTED TEXT]\n\n{ocr_text}" if text else ocr_text
                
            return text.strip() if text else None
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text directly from PDF (for text-based PDFs)"""
        text = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return '\n'.join(text)

    def _extract_text_with_ocr(self, pdf_path: str) -> str:
        """Convert PDF pages to images and perform OCR"""
        text = []
        
        # Convert PDF pages to images
        images = pdf2image.convert_from_path(pdf_path)
        
        for i, image in enumerate(images):
            # Save temporary image for debugging
            image_path = f"temp_page_{i+1}.jpg"
            image.save(image_path, "JPEG")
            
            # Perform OCR
            page_text = pytesseract.image_to_string(Image.open(image_path))
            text.append(page_text)
            
            # Clean up
            os.remove(image_path)
            
        return '\n'.join(text)

def main():
    print("PDF Text Extractor")
    print("------------------")
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = input("Enter PDF file path: ").strip('"')
    
    extractor = PDFTextExtractor()
    extracted_text = extractor.extract_text(pdf_path)
    
    if extracted_text:
        print("\nExtracted Text:")
        print("---------------")
        print(extracted_text[:2000] + "..." if len(extracted_text) > 2000 else extracted_text)
        
        # Save to text file
        output_path = os.path.splitext(pdf_path)[0] + "_extracted.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"\nFull text saved to: {output_path}")
    else:
        print("No text could be extracted from the PDF.")

if __name__ == "__main__":
    main()
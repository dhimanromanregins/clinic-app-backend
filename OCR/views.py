import PyPDF2
import re

def extract_urn_number_from_pdf(pdf_path, target_text):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        extracted_text = ""

        # Extract text from all pages
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()

        # Normalize the text: remove excessive spaces and line breaks
        normalized_text = re.sub(r'\s+', ' ', extracted_text)
        print("Normalized Extracted Text:\n", normalized_text)

        # Regular expression to find the six-digit number after 'URN'
        pattern = fr"{re.escape(target_text)}\s*-\s*(\d{{7}})"
        match = re.search(pattern, normalized_text)

        if match:
            urn_number = match.group(1)
            print(f"Six-digit number found after '{target_text}': {urn_number}")
            return urn_number
        else:
            print(f"No six-digit number found after '{target_text}'.")
            return None

pdf_path = "/home/sahil/Downloads/Document 12.pdf"
target_text = "URN"
extract_urn_number_from_pdf(pdf_path, target_text)

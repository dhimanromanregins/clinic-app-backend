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

        print("Extracted Text:\n", extracted_text)

        # Regular expression to find the six-digit number after 'URN'
        pattern = fr"{target_text}\s*(\d{{6}})"
        match = re.search(pattern, extracted_text)

        if match:
            urn_number = match.group(1)
            print(f"Six-digit number found after '{target_text}': {urn_number}")
            return urn_number
        else:
            print(f"No six-digit number found after '{target_text}'.")
            return None


pdf_path = "/home/sahil/Music/Pediatric_Clinic/OCR/URN.pdf"
target_text = "URN"
extract_urn_number_from_pdf(pdf_path, target_text)

import PyPDF2
import re
from django.db import models
from django.core.exceptions import ValidationError

def extract_urn_from_pdf(pdf_file):
    """
    Extract URN (six-digit number after 'URN') from the PDF.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""

        # Extract text from all pages
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()

        # Regular expression to find the six-digit number after 'URN'
        pattern = r"URN\s*(\d{6})"
        match = re.search(pattern, extracted_text)

        if match:
            return match.group(1)
        else:
            raise ValidationError("No six-digit URN number found in the PDF.")
    except Exception as e:
        raise ValidationError(f"Error extracting URN from PDF: {str(e)}")

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='uploads/pdfs/')
    urn_number = models.CharField(max_length=6, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pdf_file:
            try:
                urn_number = extract_urn_from_pdf(self.pdf_file)
                self.urn_number = urn_number
            except ValidationError as e:
                raise e

        super().save(*args, **kwargs)

    def __str__(self):
        return f"PDF: {self.pdf_file.name}, URN: {self.urn_number}"

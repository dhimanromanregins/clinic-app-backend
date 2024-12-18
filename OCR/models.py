import fitz
import re
from django.db import models
from children.models import Child, Documents
from django.core.exceptions import ValidationError

def extract_urn_from_pdf(file):
    """
    Extract URN (5-8 digit number after 'URN') from the PDF file using PyMuPDF.
    """
    try:
        # Check if the file is a file-like object or a path
        if hasattr(file, 'read'):  # For file-like objects
            pdf_document = fitz.open(file)
        else:  # Assume file is a path
            pdf_document = fitz.open(file)

        extracted_text = ""

        # Extract text from all pages
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text() or ""  # Handle None
            extracted_text += page_text

        # Normalize the extracted text to handle inconsistent formatting
        normalized_text = re.sub(r'[\s\-]+', ' ', extracted_text)

        # Debug: Print normalized text for troubleshooting
        print("Normalized Extracted Text:\n", normalized_text)

        # Regular expression to match 'URN' followed by a 5-8 digit number
        pattern = r"URN\s*(\d{5,8})"
        match = re.search(pattern, normalized_text)

        if match:
            return match.group(1)  # Return the 5-8 digit URN number
        else:
            # Return None if no match is found
            return None
    except Exception as e:
        # Log unexpected errors for debugging
        print(f"An unexpected error occurred: {str(e)}")
        return None


class UploadedPDF(models.Model):
    # Choices for the category of the document
    CATEGORY_CHOICES = [
        ('medical_report', 'Medical Report'),
        ('sick_leave', 'Sick Leave'),
        ('parent_sick_leave', 'Parent Sick Leave'),
        ('prescription', 'Prescription'),
        ('lab_report', 'Lab Report'),
        ('To_whome_may_concern', 'To Whome May Concern'),
    ]

    pdf_file = models.FileField(upload_to='uploads/pdfs/')
    urn_number = models.CharField(max_length=8, blank=True, null=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='medical_report',  # Default value
    )

    def save(self, *args, **kwargs):
        """
        Override save method to extract URN and add the document to the `Documents` model
        if URN matches with UAE_number in the `Child` table.
        """
        is_new_instance = not self.pk
        super().save(*args, **kwargs)

        if is_new_instance and self.pdf_file:
            # Extract URN from the uploaded PDF file
            urn_result = extract_urn_from_pdf(self.pdf_file.path)
            if urn_result and re.match(r"^\d{5,8}$", urn_result):
                self.urn_number = urn_result
                super().save(update_fields=['urn_number'])


                matching_child = Child.objects.filter(UAE_number=urn_result).first()
                if matching_child:

                    Documents.objects.create(
                        parent=matching_child.parent,
                        child=matching_child,
                        Name=self.category,
                        document=self.pdf_file,
                        category=self.category,
                    )
            else:
                self.urn_number = "0"
                super().save(update_fields=['urn_number'])

    def __str__(self):
        return f"PDF: {self.pdf_file.name}, URN: {self.urn_number}, Category: {self.get_category_display()}"

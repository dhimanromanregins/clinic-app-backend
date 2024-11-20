from django import forms
from .models import Child

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = [ 'full_name', 'child_id_number', 'relation', 'date_of_birth', 'gender', 'UAE_number', 'insurance']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        child = super().save(commit=False)
        if self.user:
            child.parent_id = self.user.id  # Set the parent_id directly
        if commit:
            child.save()
        return child

    # Custom validation for `child_id_number` to check if it meets specific format (you can modify it to fit your needs)
    def clean_child_id_number(self):
        child_id_number = self.cleaned_data.get('child_id_number')
        if not child_id_number.isdigit():
            raise forms.ValidationError("Child ID number must be numeric.")
        return child_id_number

    # Custom validation for `UAE_number`
    def clean_UAE_number(self):
        uae_number = self.cleaned_data.get('UAE_number')
        if uae_number and not uae_number.isdigit():
            raise forms.ValidationError("UAE number must be numeric.")
        return uae_number

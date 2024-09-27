from django import forms
from .models import Child


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['profile_picture', 'first_name', 'last_name', 'child_id_number', 'relation', 'date_of_birth', 'gender']
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
from django import forms
from .models import Patient

class SearchForm(forms.Form):
    Search = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"query form-control", 
            "placeholder": "Search",
            "arial-label": "Search"
        })
    )
class AddPatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddPatientForm, self).__init__(*args, **kwargs)
        placeholders = [
            'First name', 'Last name', 'ssn (###-###-###)',
            'Contact', 'Address', '@example.com',
            'Date of Surgery (yy-dd-mm)', 'Date of Recovery (yy-dd-mm)',
            'Date of birth (yy-dd-mm)', 'Surgery', 
        ]
        self.fields['image'].widget = forms.FileInput(attrs = {'class': 'form-control'})
        self.fields['surgery_details'].widget = forms.Textarea(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Write surgery details here...'
            }
        )
        # Create a new collection of keys, excluding fields which don't require any placeholder
        excluded_fields = ('slug', 'image', 'gender', 'marital_status', 'surgery_details')
        clean_fields = [field for field in self.fields.keys() if field not in excluded_fields]
        for field_name, placeholder in zip(clean_fields, placeholders):
            self.fields[field_name].widget = forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': placeholder
                }
            )            
    class Meta:
        model = Patient
        fields = (
            'first_name', 'last_name', 'image', 
            'cnic', 'gender', 'contact', 'address', 
            'email', 'marital_status', 'surgery_date',
            'recovery_date', 'date_of_birth', 'surgery',
            'surgery_details'
        )
from django import forms
from .models import FishermanProfile

class FishermanRegistrationForm(forms.ModelForm):
    class Meta:
        model = FishermanProfile
        fields = ['location', 'license_id', 'phone_number', 'address', 'id_proof', 'license_document']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Kochi, Kerala'}),
            'license_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your fishing license ID'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 1234567890'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full address'}),
            'id_proof': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'license_document': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'location': 'Location',
            'license_id': 'Fishing License ID',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'id_proof': 'ID Proof (Aadhaar/Driving License)',
            'license_document': 'Fishing License Document',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].required = True
        self.fields['license_id'].required = True
        self.fields['phone_number'].required = True
        self.fields['address'].required = True


from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    """Form for students to submit complaints."""

    class Meta:
        model = Complaint
        fields = ['category', 'priority', 'subject', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief subject of your complaint'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the issue in detail...'
            }),
        }


class ComplaintUpdateForm(forms.ModelForm):
    """Form for admin/warden to update complaint status."""

    class Meta:
        model = Complaint
        fields = ['status', 'priority', 'resolution_notes', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'resolution_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Resolution notes...'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

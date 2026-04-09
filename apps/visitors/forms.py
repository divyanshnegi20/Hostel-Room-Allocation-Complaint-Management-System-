from django import forms
from .models import VisitorEntry


class VisitorEntryForm(forms.ModelForm):
    """Form to log a visitor."""

    class Meta:
        model = VisitorEntry
        fields = ['student', 'visitor_name', 'visitor_phone', 'relation', 'purpose', 'id_proof']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # If student is logging, pre-select themselves
        if user and user.is_student:
            self.fields['student'].initial = user
            self.fields['student'].widget = forms.HiddenInput()

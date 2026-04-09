from django import forms
from .models import Room, Bed, Allocation
from apps.accounts.models import CustomUser


class RoomForm(forms.ModelForm):
    """Form to create/edit rooms."""

    class Meta:
        model = Room
        fields = ['room_number', 'floor', 'room_type', 'total_beds', 'is_ac',
                  'monthly_rent', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class BedForm(forms.ModelForm):
    """Form to create/edit beds."""

    class Meta:
        model = Bed
        fields = ['bed_label', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AllocationForm(forms.ModelForm):
    """Form for allocating a bed to a student."""

    student = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='student'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Allocation
        fields = ['student', 'start_date', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes...'
            }),
        }

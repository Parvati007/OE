from django import forms
from .models import UserStyleProfile, BODY_TYPE_CHOICES, SKIN_TONE_CHOICES, GENDER_CHOICES, COLOR_CHOICES, CLOTHING_TYPE_CHOICES


class UserStyleProfileForm(forms.ModelForm):
    favourite_colors = forms.MultipleChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select all your favorite colors"
    )
    
    preferred_clothing_types = forms.MultipleChoiceField(
        choices=CLOTHING_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select all your preferred clothing types"
    )

    class Meta:
        model = UserStyleProfile
        fields = ['height', 'skin_tone', 'body_type', 'favourite_colors', 'preferred_clothing_types', 'gender']
        widgets = {
            'height': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 175 cm or 5\'9"'}),
            'skin_tone': forms.Select(attrs={'class': 'form-select'}),
            'body_type': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'height': 'Height',
            'skin_tone': 'Skin Tone',
            'body_type': 'Body Type',
            'favourite_colors': 'Favourite Colors',
            'preferred_clothing_types': 'Preferred Clothing Types',
            'gender': 'Gender (Optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Load existing JSON data into form fields
            if self.instance.favourite_colors:
                self.initial['favourite_colors'] = self.instance.favourite_colors
            if self.instance.preferred_clothing_types:
                self.initial['preferred_clothing_types'] = self.instance.preferred_clothing_types

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Save the list data to JSON fields
        instance.favourite_colors = self.cleaned_data.get('favourite_colors', [])
        instance.preferred_clothing_types = self.cleaned_data.get('preferred_clothing_types', [])
        if commit:
            instance.save()
        return instance


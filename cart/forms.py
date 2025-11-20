from django import forms

class CartAddProductForm(forms.Form):
    size = forms.ChoiceField(choices=[])
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'style': 'width: 80px;'
    }))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    def __init__(self, *args, sizes=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sizes:
            self.fields['size'].choices = [(s, s) for s in sizes]
            self.fields['size'].widget.attrs.update({'class': 'form-control'})
from django import forms

from .models import Quote


class QuoteForm(forms.ModelForm):
    quote   = forms.CharField(label='Check Share of Search',
                              required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Search'}))

    class Meta:
        model = Quote
        fields = ['quote']

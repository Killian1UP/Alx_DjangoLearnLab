from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)

class ExampleForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
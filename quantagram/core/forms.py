from django import forms

class NewsSearchForm(forms.Form):
    query = forms.CharField(label='Enter...')


class SearchForm(forms.Form):
    query = forms.CharField(label='Search for a Blog User...')
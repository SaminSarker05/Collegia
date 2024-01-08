from django import forms

class FoodSearchForm(forms.Form):
    food_name = forms.CharField(label='Enter the name of the food')


class SearchForm(forms.Form):
    query = forms.CharField(label='Search User...')
from django import forms


class SearchForm(forms.Form):
    sat_name = forms.CharField(max_length=100)

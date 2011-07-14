from django import forms

class SearchForm(forms.Form):
	search_box = forms.CharField(label = '')

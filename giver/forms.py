from django import forms

class EmailForm(forms.Form):
  email = forms.EmailField(required=True, 
                          label='', 
                          widget=forms.TextInput(attrs={'type':'email',
                                                 'placeholder':'Enter your email'}))
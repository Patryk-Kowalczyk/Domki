from django import forms
from django.core.validators import RegexValidator


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="", widget=forms.TextInput(attrs={'placeholder': 'Imie'}))
    contact_mail = forms.EmailField(required=False, label="", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Wpisz poprawny format numeru telefonu")
    phone_number = forms.CharField(required=False, validators=[phone_regex], max_length=17, label="", widget=forms.TextInput(attrs={'placeholder': 'Numer telefonu'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Wiadomość"}), label="", required=False)

from django import forms
from django.core.validators import RegexValidator


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="", widget=forms.TextInput(attrs={'placeholder': 'Imie'}))
    contact_mail = forms.EmailField(required=False, label="", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Wpisz poprawny format numeru telefonu")
    phone_number = forms.CharField(required=False, validators=[phone_regex], max_length=17, label="", widget=forms.TextInput(attrs={'placeholder': 'Numer telefonu'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Wiadomość"}), label="", required=False)
    consent1 = forms.BooleanField(required=True, label='Wyrażam zgodę na przetwarzanie moich danych osobowych przez firmę "Domy Drewniane Szczecin" w zakresie niezbędnym do przedstawienia produktu i przygotowania oferty.')
    consent2 = forms.BooleanField(required=True, label='Wyrażam zgodę na przetwarzanie przez firmę "Domy Drewniane Szczecin" moich danych osobowych w postaci imienia, nazwiska, nr telefonu, adresu poczty elektronicznej w celu przesyłania mi informacji techniczno-marketingowych dotyczących produktów i usług oferowanych przez BTC Sp. z o.o. za pomocą środków komunikacji elektronicznej, stosownie do treści przepisu art. 10 ust. 1 i 2 ustawy o świadczeniu usług drogą elektroniczną.')

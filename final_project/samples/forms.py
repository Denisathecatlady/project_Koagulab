from django import forms
from .models import Sample, TestResult, TestType, Patient
import re

class SampleForm(forms.ModelForm):
    """Formulář pro zadávání vzorku."""
    class Meta:
        model = Sample
        fields = ['patient', 'note', 'collection_date']
        labels = {
            'patient': 'Pacient',
            'note': 'Poznámka:',
            'collection_date': 'Datum odběru',
        }

class TestResultForm(forms.ModelForm):
    """Formulář pro zadání výsledku laboratorního testu."""
    class Meta:
        model = TestResult
        fields = ['test_type', 'value', 'note']
        labels = {
            'test_type': 'Typ testu',
            'value': 'Hodnota',
            'note': 'Poznámka:',
        }

class TestTypeForm(forms.ModelForm):
    """Formulář pro vytvoření nového typu laboratorního testu."""
    class Meta:
        model = TestType
        fields = ['name', 'unit']
        labels = {
            'name': 'Název',
            'unit': 'Jednotka',
        }

class PatientForm(forms.ModelForm):
    """Formulář pro zadání údajů pacienta."""
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'birth_number', 'insurance_company', 'note']
        labels = {
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'birth_number': 'Rodné číslo',
            'insurance_company': 'Pojišťovna',
            'note': 'Poznámka:',
        }

    def clean_birth_number(self):
        """
        Ověří správnost zadaného rodného čísla dle českého formátu (dělení 11).
        Povolený formát: 9 nebo 10 číslic, volitelné lomítko.
        """
        birth_number = self.cleaned_data['birth_number']
        if birth_number == '':
            return birth_number

        rc = birth_number.replace('/', '')
        if not re.match(r'^\d{9,10}$', rc):
            raise forms.ValidationError(
                "Zadejte rodné číslo ve formátu RRRRMMDD/XXXX nebo RRRRMMDDXXXX (9–10 číslic)."
            )

        if len(rc) == 10:
            if int(rc) % 11 != 0:
                raise forms.ValidationError("Neplatné rodné číslo (špatná kontrolní číslice).")
        elif len(rc) != 9:
            raise forms.ValidationError("Rodné číslo musí mít 9 nebo 10 číslic.")

        return birth_number

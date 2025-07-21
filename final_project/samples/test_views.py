import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from samples.models import Patient, Sample, TestType, TestResult
from django.utils import timezone

@pytest.mark.django_db
def test_patient_list_view(client):
    """
    Ověří, že view pro seznam pacientů je přístupné a správně vrací stránku.
    """
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    response = client.get(reverse('patient_list'))
    assert response.status_code == 200
    assert 'Žádní pacienti nebyli nalezeni.' in response.content.decode() or 'Seznam pacientů' in response.content.decode()

@pytest.mark.django_db
def test_add_patient_view(client):
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    data = {
        'first_name': 'Jan',
        'last_name': 'Novak',
        'birth_number': '9001010007',
        'insurance_company': '111',
        'note': 'Testovací pacient',
    }

    response = client.post(reverse('add_patient'), data)
    assert response.status_code == 302
    assert Patient.objects.filter(first_name='Jan', last_name='Novak').exists()

@pytest.mark.django_db
def test_add_sample_view(client):
    """
    Ověří, že lze přidat vzorek konkrétnímu pacientovi.
    """
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    patient = Patient.objects.create(
        first_name='Jana',
        last_name='Nováková',
        birth_number='9001011235',
        insurance_company='222',
    )

    response = client.post(reverse('add_sample', args=[patient.id]), {
        'sample_code': '',
        'patient': patient.id,
        'note': '',
        'collection_date': timezone.now().strftime('%Y-%m-%dT%H:%M'),
    })

    assert response.status_code == 302
    sample = Sample.objects.filter(patient=patient).first()
    assert sample is not None

@pytest.mark.django_db
def test_add_test_result_view(client):
    """
    Ověří, že je možné přidat výsledek testu k existujícímu vzorku.
    """
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')

    patient = Patient.objects.create(
        first_name='Marek',
        last_name='Tvrdý',
        birth_number='9001011235',
        insurance_company='333',
    )
    sample = Sample.objects.create(patient=patient, sample_code='S555', collection_date=timezone.now(), created_by=user)
    test_type = TestType.objects.create(name='APTT', unit='s')

    response = client.post(reverse('add_test_result', args=[sample.id]), {
        'test_type': test_type.id,
        'value': '32.5',
        'note': 'OK',
    })

    assert response.status_code == 302
    assert TestResult.objects.filter(sample=sample, test_type=test_type).exists()

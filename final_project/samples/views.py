from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Sample, TestType, Patient
from .forms import SampleForm, TestTypeForm, TestResultForm, PatientForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


@login_required
def sample_list(request):
    """
    Zobrazí seznam všech vzorků uložených v databázi.
    Přístup povolen pouze přihlášeným uživatelům.
    """
    samples = Sample.objects.all()
    return render(request, 'sample_list.html', {'samples': samples})


@login_required
def add_sample(request, patient_id):
    """
    Umožňuje přidat nový vzorek k danému pacientovi.
    Po úspěšném uložení přesměruje zpět na detail pacienta.
    """
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            sample = form.save(commit=False)
            sample.created_by = request.user
            sample.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = SampleForm()

    return render(request, 'add_sample.html', {'form': form, 'patient': patient})

# Slovník referenčních rozmezí pro různé typy testů
REFERENCE_INTERVALS = {
    "APTT": {"unit": "s", "normal_time_min": 26.0, "normal_time_max": 40.0},
    "AT": {"unit": "%", "min": 80.0, "max": 120.0},
    "D-dimer": {"unit": "mg/L FEU", "min": 0.0, "max": 0.5},
    "FM": {"unit": "mg/L", "max": 7.0},
    "PT": {"unit": "s", "normal_time_min": 11.0, "normal_time_max": 14.0},
    "TT": {"unit": "s", "normal_time_min": 14.0, "normal_time_max": 21.0},
}

@login_required
def sample_detail(request, sample_id):
    """
    Zobrazí detail vybraného vzorku včetně všech výsledků testů
    a k nim odpovídajících referenčních rozmezí.
    """
    sample = get_object_or_404(Sample, id=sample_id)
    test_results = sample.test_results.all()

    results_with_reference = []
    for result in test_results:
        ref = REFERENCE_INTERVALS.get(result.test_type.name)
        results_with_reference.append({
            "result": result,
            "reference": ref,
        })

    return render(request, 'sample_detail.html', {
        'sample': sample,
        'results_with_reference': results_with_reference,
    })


@login_required
def add_test_type(request):
    """
    Umožňuje přidat nový typ testu do systému.
    Typicky používáno správcem laboratoře.
    """
    if request.method == 'POST':
        form = TestTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('test_type_list')
    else:
        form = TestTypeForm()
    return render(request, 'add_test_type.html', {'form': form})


@login_required
def add_test_result(request, sample_id):
    """
    Přidá nový výsledek testu ke konkrétnímu vzorku.
    Výsledek se ukládá společně s informací o datu měření.
    """
    sample = get_object_or_404(Sample, id=sample_id, created_by=request.user)

    if request.method == 'POST':
        form = TestResultForm(request.POST)
        if form.is_valid():
            test_result = form.save(commit=False)
            test_result.sample = sample
            test_result.result_date = timezone.now().date()
            test_result.save()
            return redirect('sample_detail', sample_id=sample.id)
    else:
        form = TestResultForm()

    return render(request, 'add_test_result.html', {'form': form, 'sample': sample})


@login_required
def patient_list(request):
    """
    Zobrazí seznam všech pacientů v systému.
    """
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, patient_id):
    """
    Detailní pohled na konkrétního pacienta, včetně všech jeho vzorků.
    """
    patient = get_object_or_404(Patient, id=patient_id)
    samples = patient.samples.all()

    return render(request, 'patient_detail.html', {
        'patient': patient,
        'samples': samples,
    })

@login_required
def add_patient(request):
    """
    Umožňuje přidat nového pacienta do systému.
    """
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

@login_required
def test_type_list(request):
    """
    Zobrazí seznam všech typů testů dostupných v laboratoři.
    """
    test_types = TestType.objects.all()
    return render(request, 'test_type_list.html', {'test_types': test_types})

def register(request):
    """
    Registrace nového uživatele do systému.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_list')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


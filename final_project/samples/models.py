from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Patient(models.Model):
    """
    Model pro uchování údajů o pacientovi.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_number = models.CharField(max_length=20, blank=True)
    insurance_company = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Sample(models.Model):
    """
    Model reprezentující odebraný vzorek od pacienta.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='samples', null=True, blank=True)
    collection_date = models.DateTimeField(default=timezone.now)
    sample_code = models.CharField(max_length=50, unique=True, blank=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='samples')

    def save(self, *args, **kwargs):
        """
        Uloží vzorek. Vygeneruje se automaticky.
        """
        if not self.sample_code:
            last_id = Sample.objects.order_by('-id').first()
            next_number = 1 if not last_id else last_id.id + 1
            self.sample_code = f"KOAG-{next_number:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sample_code} - {self.patient}"

class TestType(models.Model):
    """
    Model pro typ laboratorního testu (např. APTT, PT, AT).
    """
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    reference_min = models.FloatField(null=True, blank=True)
    reference_max = models.FloatField(null=True, blank=True)
    normal_time_min = models.FloatField(null=True, blank=True)
    normal_time_max = models.FloatField(null=True, blank=True)
    normal_ratio_min = models.FloatField(null=True, blank=True)
    normal_ratio_max = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class TestResult(models.Model):
    """
    Model pro uchování výsledku laboratorního testu ke konkrétnímu vzorku.
    """
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='test_results')
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    value = models.FloatField()
    result_date = models.DateField()
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.test_type.name}: {self.value}"

class Attachment(models.Model):
    """
    Model pro přílohy k jednotlivým vzorkům (např. PDF, obrázky).
    """
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"Attachment for {self.sample.sample_code}"

from django.contrib import admin
from .models import Sample, TestType, TestResult, Attachment, Patient

admin.site.register(Sample)
admin.site.register(TestType)
admin.site.register(TestResult)
admin.site.register(Attachment)
admin.site.register(Patient)


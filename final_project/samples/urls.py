from django.urls import path
from . import views
from .views import register


urlpatterns = [
    path('', views.patient_list, name='patient_list'),  # výchozí stránka – seznam pacientů
    path('add/', views.add_patient, name='add_patient'),  # přidání pacienta
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'),  # detail pacienta
    path('<int:patient_id>/add_sample/', views.add_sample, name='add_sample'),  # přidání vzorku pacientovi
    path('samples/<int:sample_id>/', views.sample_detail, name='sample_detail'),  # detail vzorku
    path('samples/<int:sample_id>/add_test/', views.add_test_result, name='add_test_result'),  # přidání výsledku testu ke vzorku
    path('test-types/add/', views.add_test_type, name='add_test_type'),  # přidání typu testu
    path('test-types/', views.test_type_list, name='test_type_list'),  # seznam typů testů
    path('accounts/register/', register, name='register'),
]
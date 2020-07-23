from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'patients'
urlpatterns = [
	path('', views.patients_list, name='patients_list'),
	# api url-patterns
	path('api/', views.patients_list_api_view, name='patients_list_api'),
	path('api/<slug:patient_slug>/', views.patient_detail_api_view, name='patient_detail_api'),
	
	# general patterns
	path('add/', views.add_patient, name='patient_new'),
	path('<slug:patient_slug>/', views.patient_detail, name='patient_detail'),
	path('<slug:patient_slug>/edit/', views.edit_patient, name='patient_edit'),
	path('<slug:patient_slug>/delete/', views.delete_patient, name='delete_patient'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
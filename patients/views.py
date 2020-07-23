from django.shortcuts import render, redirect
from .models import Patient
from .forms import SearchForm, AddPatientForm
from django.contrib.postgres.search import SearchVector
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PatientSerializer

def patients_list(request):

	""" Handles Patients List and also provide Search facility """
	patients = Patient.objects.all()
	headers = [
		field.name for field in Patient._meta.get_fields() if field.name not in ('id', 'slug', 'surgery_details', 'image')
	]

	search_form = SearchForm()
	search_results = []
	query = None

	if 'Search' in request.GET:
		search_form = SearchForm(request.GET)
		if search_form.is_valid():
			query = search_form.cleaned_data.get('Search')
			search_results = Patient.objects.annotate(
				search = SearchVector('first_name', 'surgery', 'cnic'),
			).filter(search=query)

	# calculate percentage of male and female patients
	males 			 = len(Patient.males.all())
	males_percentage = round(((males/len(patients)) * 100), 1)

	females 		   = len(Patient.females.all())
	females_percentage = round(((females/len(patients)) * 100), 1)

	context = {
		'headers': headers,
		'patients': patients,
		'males': males,
		'females': females,
		'males_percentage': males_percentage,
		'females_percentage': females_percentage,
		'search_form': search_form,
		'search_results': search_results
	}
	return render(request, 'patients/list.html', context)

def patient_detail(request, patient_slug):
	""" Show the details of a particular patient """
	patient = Patient.objects.get(slug=patient_slug)
	return render(request, 'patients/detail.html', {'patient': patient})

def add_patient(request):
	""" To add new patient in the database """
	if request.method == 'POST':
		form = AddPatientForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			print("View Executed...........")
			form.save()
			return redirect('patients:patients_list')
	else:
		form = AddPatientForm()
	return render(request, 'patients/add.html', {'form': form})

def edit_patient(request, patient_slug):
	""" Edit the patient's data """
	patient = Patient.objects.get(slug=patient_slug)
	form = AddPatientForm(request.POST or None, request.FILES or None, instance=patient)

	if form.is_valid():
		form.save()
		form = AddPatientForm()
		return redirect('patients:patients_list')
	return render(request, 'patients/edit.html', {'form':form})

def delete_patient(request, patient_slug):
	""" Delete a patient from database, if exists """
	try:
		patient = Patient.objects.get(slug=patient_slug)
	except patient.DoesNotExist:
		raise Exception("Requested patient does not exist.")
	# delete patient
	patient.delete()
	return redirect('patients:patients_list')

# ================================================================
# PATIENTS REST-API VIEWS
# ================================================================

@api_view(['GET', 'POST'])
def patients_list_api_view(request, format=None):
	""" List all patients or add a new patient """
	if request.method == 'GET':
		patients = Patient.objects.all()
		serializer = PatientSerializer(patients, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = PatientSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def patient_detail_api_view(request, patient_slug, format=None):
	""" Retrieve, Update or Delete Patient """

	try:
		patient = Patient.objects.get(slug=patient_slug)
	except patient.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = PatientSerializer(patient)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = PatientSerializer(patient, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
	
	elif request.method == 'DELETE':
		patient.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
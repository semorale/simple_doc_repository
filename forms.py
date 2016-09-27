# -*- encoding: utf-8 -*-

#STDLIB importa

#Core Django Imports
from django import forms
from django.forms.widgets import *
#Third Party apps imports

#Imports local apps
from .models import Doc, Category, Section


class DocCreateForm(forms.ModelForm):
	date = forms.DateTimeField(input_formats=['%Y-%m-%d','%d-%m-%Y'],widget=forms.TextInput(attrs={"class": "form-control", "id":"date-input"}))
	class Meta:
		model= Doc
		exclude = ('timestamp','uploader')
		widgets ={
			'name' : TextInput(attrs={"class": "form-control"}),
			'description' : TextInput(attrs={"class": "form-control"}),
			'category' : Select(attrs={"class": "form-control", "id":"selectCategoria"}),
			'section' : Select(attrs={"class": "form-control",  "id":"selectSeccion"})
		}

class CategoryCreateForm(forms.ModelForm):
	class Meta:
		model= Category
		fields= '__all__'
		widgets ={
		 'name':TextInput(attrs={"class": "form-control"}),
		 'description': TextInput(attrs={"class": "form-control"})
		}

class SectionCreateForm(forms.ModelForm):
	class Meta:
		model= Section
		fields= '__all__'
		widgets ={
			'name':TextInput(attrs={"class": "form-control"}),
		 	'description': TextInput(attrs={"class": "form-control"}),
			'category': Select(attrs={"class": "form-control"})
		}

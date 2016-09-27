# -*- encoding: utf-8 -*-

#STDLIB importa
from datetime import date,datetime
import time
from unidecode import unidecode

#Core Django Imports
from django.db import connection

from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import  View,ListView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.text import get_valid_filename
#Third Party apps imports
import simplejson as json
#Imports local apps
from .models import Doc, Category,Section
from .forms import DocCreateForm, CategoryCreateForm, SectionCreateForm

class CreateDoc(SuccessMessageMixin,CreateView):
	models = Doc
	form_class = DocCreateForm
	template_name='doc_create_form.html'

	def form_valid(self,form):
		form.instance.uploader=self.request.user
		form.instance.name = get_valid_filename(form.instance.name)
		return super(CreateDoc,self).form_valid(form)

	def get_success_url(self):
		return reverse('repository:Create Doc')

	def get_context_data(self, **kwargs):
		contexto = super(CreateDoc, self).get_context_data(**kwargs)
		contexto['action'] = reverse('repository:Create Doc')
		return contexto

	def form_invalid(self, form):
		return HttpResponse("form is invalid.. this is just an HttpResponse object")

	success_message = 'Doc Create Successfully'

class CreateCategory(SuccessMessageMixin,CreateView):
	models = Category
	form_class = CategoryCreateForm
	template_name='category_create_form.html'

	def get_success_url(self):
		return reverse('repository:Create Category')

	def get_context_data(self, **kwargs):
		contexto = super(CreateCategory, self).get_context_data(**kwargs)
		contexto['action'] = reverse('repository:Create Category')
		return contexto

	success_message = 'Category Create Successfully'

class CreateSection(SuccessMessageMixin,CreateView):
	models = Section
	form_class = SectionCreateForm
	template_name='section_create_form.html'

	def get_success_url(self):
		return reverse('repository:Create Section')

	def get_context_data(self, **kwargs):
		contexto = super(CreateSection, self).get_context_data(**kwargs)
		contexto['action'] = reverse('repository:Create Section')
		return contexto

	success_message = 'Section Create Successfully'

class ListDoc(ListView):
	model = Doc
	template_name='doc_list.html'

	def get_context_data(self, **kwargs):
		contexto = super(ListDoc, self).get_context_data(**kwargs)
		contexto['lista_categorias'] = Category.objects.all().values('id','name')
		return contexto

	def get_queryset(self,**kwargs):
		return Doc.objects.all().order_by("category","section","date")

class DownloadDoc(TemplateView):
	def get(self, request,*args,**kwargs):
		contexto = super(DownloadDoc, self).get_context_data(**kwargs)
		id_documento = contexto['id_documento']
		documento = Doc.objects.get(pk=id_documento)
		url = u"/media/{0}".format(documento.upload)
		response =  HttpResponse()
		response['Content-Disposition'] = u'attachment; filename="{0}_{1}_{2}_{3}.{4}"'.format(documento.date.strftime("%d-%m-%Y"),documento.name,documento.category,documento.section, str(documento.upload).split(".")[-1])
		response['X-Accel-Redirect'] = url.encode('utf-8')
		return response

class ListSections(View):
	def get(self, request,*args,**kwargs):
		categoria = request.GET['categoria']
		return JsonResponse(dict(secciones = list(Section.objects.filter(category=categoria).values('name','id'))))

class SearchDocs(View):
	def get(self, request):
		fecha_inicial=request.GET.get("fecha_inicial","")
		fecha_final=request.GET.get("fecha_final","")
		kwargs=request.GET.dict()
		for i,j in kwargs.items():
			if j=="":
				del kwargs[i]
		if "fecha_inicial" in kwargs:
			del kwargs["fecha_inicial"]
		if "fecha_final" in kwargs:
			del kwargs["fecha_final"]
		if fecha_inicial !="" and fecha_final !="":
			kwargs["date__range"]= (datetime.strptime(fecha_inicial,"%d-%m-%Y").date(),datetime.strptime(fecha_final,"%d-%m-%Y").date())
		documents= Doc.objects.select_related('category', 'section').filter(**kwargs).order_by("category","date")
		list_docs=[]
		for i in documents:
			list_docs.append({'name':i.name,'description':i.description,'category':i.category.name,'section':i.section.name,'date':i.date.isoformat(),'id':i.id, 'uploader':i.uploader.username})
		return HttpResponse(json.dumps(list_docs), content_type="application/json")

class Rest(View):
	def delete(self, request, *args,**kwargs):
		data = self.kwargs
		if 'id' in data:
			document = get_object_or_404(Doc,pk=data['id'])
			if document.uploader.id == request.user.id or request.user.profile.tipo=="Administrador" or request.user.is_superuser:
				document.delete()
				return JsonResponse({"meta":{},"data":{}}, status=200)
			else:
				return JsonResponse({"meta":{"error":"Usuario no cuenta con los permisos necesarios"},"data":{}}, status=403)
		else:
			return JsonResponse({"meta":{"error":"id no enviada"},"data":{}}, status=400)

	def get(self, request, *args,**kwargs):
		data = self.kwargs
		if 'id' in data:
			document = get_object_or_404(Doc,pk=data['id'])
			if document.uploader.id == request.user.id or request.user.profile.tipo=="Administrador" or request.user.is_superuser:
				return JsonResponse({"meta":{},"data":{"nombre":document.name,"descripcion":document.description,"fecha":document.date.isoformat(),"proceso":document.category.id,"tipo":document.section.id,"id":document.id}}, safe=False ,status=200)
			else:
				return JsonResponse({"meta":{"error":"Usuario no cuenta con los permisos necesarios"},"data":{}}, status=403)
		else:
			return JsonResponse({"meta":{"error":"id no enviada"},"data":{}}, status=400)


	def post(self, request, *args,**kwargs):
		data = self.kwargs
		if 'id' in data:
			document = get_object_or_404(Doc,pk=data['id'])
			form = DocCreateForm(request.POST or None,request.FILES or None, instance=document)
			if form.is_valid():
				form.save()
				return JsonResponse({"meta":{},"data":{}}, status=200)
			else:
				return JsonResponse({"meta":{},"data":{}}, status=400)
		else:
			return JsonResponse({"meta":{"error":"id no enviada"},"data":{}}, status=400)

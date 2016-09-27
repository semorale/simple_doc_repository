# -*- encoding: utf-8 -*-

#STDLIB imports
#Core Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import get_valid_filename
#Third Party apps imports

#Imports local apps

class Category(models.Model):
	name = models.CharField(max_length=135, blank=False, null=False)
	description = models.CharField(max_length=135, blank=False, null=False)

	def __unicode__(self):
		return u'%s' % (self.name)

class Section(models.Model):
	name = models.CharField(max_length=135, blank=False, null=False)
	description = models.CharField(max_length=135, blank=False, null=False)
	category = models.ForeignKey(Category, blank=False, null=False)

	def __unicode__(self):
		return u'%s' % (self.name)

def user_directory_path(instance, filename):
	return u'simple_doc_repository/{0}/{1}'.format(instance.category, get_valid_filename(filename))

class Doc(models.Model):
	name = models.CharField(max_length=135, blank=False, null=False)
	description = models.CharField(max_length=135, blank=False, null=False)
	date = models.DateTimeField()
	timestamp = models.DateTimeField(auto_now_add=True)
	upload = models.FileField(upload_to=user_directory_path)
	category = models.ForeignKey(Category, blank=False, null=False)
	section = models.ForeignKey(Section, blank=False, null=False)
	uploader= models.ForeignKey(User, blank=False, null=False)
	def __unicode__(self):
		return u'{0} -- {1}'.format(self.name,self.timestamp.strftime('%d-%m-%Y %H:%M'))

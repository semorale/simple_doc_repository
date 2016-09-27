# -*- encoding: utf-8 -*-
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from .views import CreateDoc,CreateCategory,CreateSection,ListDoc,DownloadDoc, ListSections, SearchDocs, Rest

urlpatterns = [
	url(r'^(?P<id>(\d)+)$', csrf_exempt(Rest.as_view()),name='rest view'),
    url(r'^create_doc/$',CreateDoc.as_view(),name='Create Doc'),
    url(r'^create_category/$',CreateCategory.as_view(),name='Create Category'),
    url(r'^create_section/$',CreateSection.as_view(),name='Create Section'),
    url(r'^list_doc/$',ListDoc.as_view(),name='List Doc'),
    url(r'^download_doc/(?P<id_documento>(\w)+)/$',DownloadDoc.as_view(),name='Download Doc'),
    url(r'^sections/$',csrf_exempt(ListSections.as_view()),name='ajax list Section'),
    url(r'^search/$',csrf_exempt(SearchDocs.as_view()),name='ajax search docs'),
]
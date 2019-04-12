from django.urls import path

from . import views

urlpatterns = [
    path('objects', views.thing_descriptor, name='objects_view'),
    path('objects/<oid>/properties/<pid>', views.location_tag, name='tag_view')
]

from cmath import e
from django.urls import path
from django.urls import re_path

from . import views



urlpatterns = [
    path("wiki", views.index, name="index"),
    path("wiki/newpage", views.newPage, name = "newPage"),
    path("wiki/random", views.randomPage, name="randomPage"),
    path("wiki/<str:entryName>", views.getEntry, name="getEntry"),
    path("wiki/<str:editEntryName>/edit", views.editEntry, name="editEntry")
]

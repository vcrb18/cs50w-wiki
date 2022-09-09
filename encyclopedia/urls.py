from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/random", views.random, name="random"),
    path("wiki/add.html", views.add, name="add"),
    path("wiki/<str:name>", views.entry, name="name"),
    path("search", views.search, name="search"),
    path("edit/<str:name>", views.edit, name="edit")
]

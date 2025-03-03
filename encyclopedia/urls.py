from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.page, name="wiki-page"),
    path("result/", views.search, name="search"),
    path("newpage/", views.create_new_page, name="new-page"),
    path("edit/<str:title>", views.edit_page, name="edit"),
    path("random/", views.random_page, name="random-page"),
]

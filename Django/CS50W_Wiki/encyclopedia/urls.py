from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random", views.random, name="random"),
    path("create", views.create, name="create"),
    path('edit/<str:title>', views.edit, name='edit'),
    path('search/', views.search, name='search')
]

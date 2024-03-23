from django.urls import path

from . import views

urlpatterns = [ path("", views.index, name="index"), 
                path("david", views.david, name="david"),
                path("<str:name>", views.greet, name="greet"),
                path("some_view/<str:name>", views.some_view, name="some_view"),
                path("some_view/", views.some_view, name="some_view")
]


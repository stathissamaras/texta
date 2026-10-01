from django.urls import path

from . import views

app_name = "configurator"

urlpatterns = [
    path("", views.configurator, name="index"),
    path("eikona/<str:kentrika>/<str:plaina>/", views.eikona, name="eikona"),
]
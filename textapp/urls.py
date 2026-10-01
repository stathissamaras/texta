from django.urls import path
from . import views

app_name = 'textapp'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter'),
    path('newsletter/confirm/<str:token>/', views.newsletter_confirm,
        name='newsletter_confirm'),
    path('newsletter/unsubscribe/<str:token>/', views.newsletter_unsubscribe,
        name='newsletter_unsubscribe'),

    path('newsletter/sent/', views.newsletter_sent, name='newsletter_sent'),
    path('materials/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('facilities/', views.FacilitiesView.as_view(), name='facilities'),
    path('legal/', views.LegalView.as_view(), name='legal'),
]

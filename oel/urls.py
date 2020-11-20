from django.urls import path, include

from . import views

app_name = 'oel'
urlpatterns = [
    path('<int:einsatz_id>/', views.oel, name='oel'),
    path('<int:einsatz_id>/neue_einheit', views.neue_einheit, name='neue_einheit'),
    path('<int:einsatz_id>/neue_einsatzstelle', views.neue_einsatzstelle, name='neue_einsatzstelle'),
    path('<int:einsatz_id>/<int:einsatzstelle>/zuweisen', views.einheit_zuweisen, name='einheit_zuweisen'),
    path('<int:einsatz_id>/<int:einsatzstelle>/erledigt', views.einsatzstelle_erledigt, name='einsatzstelle_erledigt'),
    path('<int:einsatz_id>/<int:einsatzstelle>/info', views.neue_einheit, name='neue_information'),
    path('Benutzer/', include('django.contrib.auth.urls')),
]
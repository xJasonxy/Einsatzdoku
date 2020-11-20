from django.urls import path, include

from . import views

app_name = 'lagekarte'
urlpatterns = [
    path('<int:einsatz_id>/', views.lagekarte, name="lagekarte"),
    path('Benutzer/', include('django.contrib.auth.urls')),
]
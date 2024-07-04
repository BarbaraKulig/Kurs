# quotes_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quotes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Do obsługi rejestracji, logowania i resetowania hasła
]

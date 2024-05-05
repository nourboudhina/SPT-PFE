
from django.contrib import admin
from django.urls import path, include 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('account.urls')),
    path('accueil/', include('accueil.urls')),
    path('chat/', include('chat.urls')),
    path('planning/', include('planning.urls')),
    
    path("__reload__/", include("django_browser_reload.urls")),
]


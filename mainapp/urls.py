from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#MEDIA_URL gives me the server directory 
#MEDIA_ROOT gives me the file location in the server directory (uploadedFiles in our case)
#static() creates that static path to our file
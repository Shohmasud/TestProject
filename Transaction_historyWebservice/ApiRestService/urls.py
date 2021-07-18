from .views import SerializerfileName,SerializerResponse
from django.urls import path
urlpatterns = [
    path('api/v6/post/',  SerializerfileName.as_view()),
    path('api/v6/get/',  SerializerResponse.as_view()),
]

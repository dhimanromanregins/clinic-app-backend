from django.urls import path
from .views import *
urlpatterns = [
    path('leaves/', LeavesAPIView.as_view()),
]


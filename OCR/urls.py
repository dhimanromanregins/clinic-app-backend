from django.urls import path
from .views import ChildDocumentsAPIView

urlpatterns = [
    path('child-documents/', ChildDocumentsAPIView.as_view(), name='child-documents'),
]

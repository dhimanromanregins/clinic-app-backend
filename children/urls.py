from django.urls import path
from .views import *


urlpatterns = [
    path('children/', ChildListCreateView.as_view(), name='child-list-create'),
    path('api/children/<int:child_id>/', ChildDetailView.as_view(), name='child-detail'),
    path('children/<int:child_id>/documents/', DocumentsListView.as_view(), name='documents-list'),
]


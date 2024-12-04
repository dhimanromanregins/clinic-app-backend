from django.urls import path
from .views import *


urlpatterns = [
    path('children/', ChildListCreateView.as_view(), name='child-list-create'),
    path('api/children/', ChildCreateView.as_view(), name='child-list-create'),
    path('api/children/<int:child_id>/', ChildDetailView.as_view(), name='child-detail'),
    path('children/<int:child_id>/documents/', DocumentsListView.as_view(), name='documents-list'),

    path('api/documents/parent/<str:category>/', DocumentsByParentAndCategoryView.as_view(), name='documents_by_parent_and_category'),
    path('api/documents/child/<int:child_id>/<str:category>/', DocumentsByChildAndCategoryView.as_view(), name='documents_by_child_and_category'),
]


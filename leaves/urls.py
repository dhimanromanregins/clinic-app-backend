from django.urls import path
from .views import *
urlpatterns = [
    path('leaves/', LeavesAPIView.as_view()),
    path('api/sick-leave-request/', SickLeaveRequestAPIView.as_view(), name='sick-leave-request'),
    path('api/sick-leave-records/', SickLeaveRecordsByChildView.as_view(), name='sick-leave-records-by-child'),
    path('api/parent-sick-leave/', ParentSickLeaveCreateAPIView.as_view(), name='parent-sick-leave-create'),
    path('parent-sick-leave-history/', ParentSickLeaveHistoryList.as_view(), name='parent_sick_leave_history_list'),
    path('to-whom-it-may-concern/', ToWhomItMayConcernCreateView.as_view(), name='to-whom-it-may-concern-create'),
]


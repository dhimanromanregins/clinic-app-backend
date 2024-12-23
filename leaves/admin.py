from django.contrib import admin
from .models import Leaves,PrescriptionRequestView,SickLeaveRequestView,SickLeaveRecords,ParentSickLeave,ParentSickLeaveHistory,ToWhomItMayCocern,MedicalReportsRequestView

# Register your models here.

admin.site.register(Leaves)
admin.site.register(SickLeaveRequestView)
admin.site.register(SickLeaveRecords)
admin.site.register(ParentSickLeave)
admin.site.register(ParentSickLeaveHistory)
admin.site.register(ToWhomItMayCocern)
admin.site.register(MedicalReportsRequestView)
admin.site.register(PrescriptionRequestView)

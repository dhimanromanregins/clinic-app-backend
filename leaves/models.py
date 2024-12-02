from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from children.models import Child
from django.utils import timezone
# Create your models here.

class Leaves(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField(editable=False)
    reason = models.TextField()
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

        self.total_days = (self.end_date - self.start_date).days + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.type} ({self.start_date} to {self.end_date})"

    class Meta:
        verbose_name_plural = "leaves"


class SickLeaveRequestView(models.Model):
    children = models.ForeignKey(Child, on_delete=models.CASCADE)
    to = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)

    def __str__(self):
        return f"Sick leave record for {self.children.full_name}"


class SickLeaveRecords(models.Model):
    children = models.ForeignKey(Child, on_delete=models.CASCADE)
    document = models.FileField(upload_to='sick_leave_documents/')
    created_date = models.DateTimeField(auto_now_add=True)
    leave_request_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Sick leave record for {self.children.full_name}"


class ParentSickLeave(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    child_name = models.TextField()
    sent_to = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)

    def __str__(self):
        return f"Parent Sick leave record for {self.user.first_name}"

class ParentSickLeaveHistory(models.Model):
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.FileField(upload_to='sick_leave_documents/')
    created_date = models.DateTimeField(auto_now_add=True)
    leave_request_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Parent Sick leave history for {self.parent.first_name}"

class ToWhomItMayCocern(models.Model):
    concern = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    child_name = models.TextField()
    sent_to = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    additional_notes = models.TextField()

    def __str__(self):
        return f"{self.user.first_name}"




from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
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

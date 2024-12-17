from django.db import models
from doctors.models import Doctor
from accounts.models import CustomUser
from children.models import Child
# Create your models here.


class Booking(models.Model):
    STATUS = [
        ('YES', 'YES'),
        ('NO', 'NO')
        ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='use')
    children_names = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    patient_arrived = models.CharField(max_length=50,choices=STATUS,default='NO')
    slot_start = models.TimeField()
    slot_end = models.TimeField()
    date = models.DateField()

    class Meta:
        unique_together = ('doctor', 'slot_start', 'slot_end', 'date')

    def __str__(self):
        return f"{self.doctor.name} - {self.slot_start} to {self.slot_end} on {self.date}"

    def get_children_list(self):
        # This method can be used to retrieve the list of children names as a list
        return self.children_names.split(",") if self.children_names else []
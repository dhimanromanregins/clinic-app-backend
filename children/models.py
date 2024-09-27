from django.db import models
from accounts.models import CustomUser
# Create your models here.



class Child(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    class RelationChoices(models.TextChoices):
        MOTHER = 'MOTHER', 'Mother'
        FATHER = 'FATHER', 'Father'
        AUNTY = 'AUNTY', 'Aunty'
        UNCLE = 'UNCLE', 'Uncle'
        FRIEND = 'FRIEND', 'Friend'

    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    child_id_number = models.CharField(max_length=18, unique=True)
    relation = models.CharField(max_length=10, choices=RelationChoices.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.child_id_number})"


class Documents(models.Model):
    child = models.ForeignKey(Child, models.CASCADE, related_name='childern_document')
    Name = models.CharField(max_length=255)
    document = models.FileField()

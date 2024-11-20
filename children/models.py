from distutils.command.build import build

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

    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='children')
    full_name = models.CharField(max_length=255)
    child_id_number = models.CharField(max_length=18, unique=True)
    UAE_number = models.CharField(max_length=255, null=True, blank=True)
    relation = models.CharField(max_length=10, choices=RelationChoices.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    grade = models.CharField(max_length=255, null=True, blank=True)
    insurance = models.CharField(max_length=255, null=True, blank=True)
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.child_id_number})"

    class Meta:
        verbose_name_plural = "Children"


class Documents(models.Model):
    child = models.ForeignKey(Child, models.CASCADE, related_name='childern_document')
    Name = models.CharField(max_length=255)
    document = models.FileField()

    class Meta:
        verbose_name_plural = "Documents"


from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import post_save
from accounts.utils import send_expo_push_notification
from django.dispatch import receiver
from accounts.models import Notifications
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

    INSURANCE_CHOICES = [
        ('NAS', 'NAS'),
        ('METLIFE', 'METLIFE'),
        ('NEXTCARE', 'NEXTCARE'),
        ('GLOBEMED', 'GLOBEMED'),
        ('ADNIC', 'ADNIC'),
        ('OPEN_JET', 'OPEN JET'),
        ('DAMAN', 'DAMAN'),
        ('THIQA', 'THIQA'),
        ('AL_KHAZNA', 'AL KHAZNA'),
        ('AXA', 'AXA'),
        ('NEURON', 'NEURON'),
        ('MEDNET', 'MEDNET'),
        ('SUKOON', 'SUKOON'),
        ('WEALTH_INTL', 'Wealth International'),
        ('PENTACARE', 'Pentacare'),
        ('AL_MADALLAH', 'AL Madallah'),
        ('FMC_METLIFE', 'FMC - Metlife'),
        ('MAX_CARE', 'Max Care'),
        ('AFIYA_TPA', 'Afiya TPA'),
        ('NGI_HEALTHNET', 'NGI Healthnet'),
        ('IRIS', 'IRIS'),
        ('MSH', 'MSH'),
    ]

    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='children')
    full_name = models.CharField(max_length=255)
    child_id_number = models.CharField(max_length=18, unique=True, null=True, blank=True)
    UAE_number = models.CharField(max_length=255, null=True, blank=True,unique=True)
    relation = models.CharField(max_length=10, choices=RelationChoices.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    grade = models.CharField(max_length=255, null=True, blank=True)
    insurance = models.CharField(max_length=255,choices=INSURANCE_CHOICES, null=True, blank=True)
    insurance_number = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.child_id_number})"

    class Meta:
        verbose_name_plural = "Children"


class Documents(models.Model):
    CATEGORY_CHOICES = [
        ('medical_report', 'Medical Report'),
        ('sick_leave', 'Sick Leave'),
        ('parent_sick_leave', 'Parent Sick Leave'),
        ('prescription', 'Prescription'),
        ('lab_report', 'Lab Report'),
        ('To_whome_may_concern', 'To Whome May Concern'),
    ]
    parent = models.ForeignKey(CustomUser, models.CASCADE,null=True, blank=True)
    child = models.ForeignKey(Child, models.CASCADE, related_name='childern_document')
    Name = models.CharField(max_length=255)
    document = models.FileField()
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='medical_report',  # Default value
    )

    def __str__(self):
        return f"{self.child} ({self.document})"

    class Meta:
        verbose_name_plural = "Documents"

@receiver(post_save, sender=Documents)
def notify_document_added(sender, instance, created, **kwargs):
    if created:
        user = instance.child.parent
        device_token = user.device_token

        if device_token:
            message_payload = {
                "to": device_token,
                "title": "New Document Added",
                "body": f"A new document '{instance.Name}' has been added for child Name {instance.child.full_name}.",
            }
            response = send_expo_push_notification(message_payload)
            if response and response.get("data"):
                Notifications.objects.create(
                    user=user,
                    title=message_payload["title"],
                    body=message_payload["body"],
                )
                print(f"Notification saved for user: {user}")
            else:
                print(f"Failed to send notification. Response: {response}")
            print(response)
        else:
            print(f"No device token found for user: {user}")



class Vaccination(models.Model):
    AGE_GROUPS = [
        ('after_birth', 'After Birth'),
        ('end_2_month', 'End of 2 Months'),
        ('end_4_month', 'End of 4 Months'),
        ('end_6_month', 'End of 6 Months'),
        ('end_12_month', 'End of 12 Months'),
        ('end_18_month', 'End of 18 Months'),
        ('grade_a', 'Grade A'),
        ('grade_8', 'Grade 8'),
        ('grade_11', 'Grade 11'),
    ]

    VACCINATIONS = [
        ('BCG', 'BCG'),
        ('Hepatitis B', 'Hepatitis B'),
        ('Hexavalent', 'Hexavalent (DTaP, Hib, Hep B, IPV)'),
        ('PCV', 'PCV'),
        ('Rotavirus', 'Rotavirus'),
        ('NMR-1', 'NMR-1'),
        ('Varicella-1', 'Varicella-1'),
        ('bOPV', 'bOPV'),
        ('DTaP-Hib-IPV', 'DTaP-Hib-IPV'),
        ('MMR-2', 'MMR-2'),
        ('MMR-3', 'MMR-3'),
        ('Varicella-2', 'Varicella-2'),
        ('DTaP-IPV', 'DTaP-IPV'),
        ('HPV', 'HPV (Female)'),
        ('Tdap', 'Tdap'),
        ('MCV', 'MCV'),
    ]

    child = models.ForeignKey('Child', on_delete=models.CASCADE)
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS)
    vaccination_name = models.CharField(max_length=50, choices=VACCINATIONS)
    vaccination_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.child} - {self.get_age_group_display()} - {self.get_vaccination_name_display()}"


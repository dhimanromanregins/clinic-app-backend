from django.db import models
from datetime import timedelta, datetime

from accounts.models import CustomUser


# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.city}"


class DayOfWeek(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Week Days"

class WorkingPeriod(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='working_periods')
    day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE, related_name='working_periods')
    morning_start = models.TimeField(null=True, blank=True)
    morning_end = models.TimeField(null=True, blank=True)
    afternoon_start = models.TimeField(null=True, blank=True)
    afternoon_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return (f"Doctor: {self.doctor.name}, Day: {self.day_of_week.name}, "
                f"Morning: {self.morning_start} to {self.morning_end}, "
                f"Afternoon: {self.afternoon_start} to {self.afternoon_end}")
    class Meta:
        verbose_name_plural = "Working Periods"


class Language(models.Model):
    language = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language}"
    class Meta:
        verbose_name_plural = "Languages"

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="doctors")
    languages = models.ManyToManyField(Language, related_name="doctors")
    experience = models.CharField(max_length=255)
    about = models.TextField()
    hospital_name = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    registration_id = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='doctors_images/', null=True, blank=True)
    digital_consult = models.BooleanField(default=False)
    hospital_visit = models.BooleanField(default=False)
    price = models.BigIntegerField()
    is_available = models.BooleanField(default=True)


    

    def __str__(self):
        return f"{self.name}"
    
    @classmethod
    def get_total_doctors(cls):
        return cls.objects.count()

    def generate_slots_for_period(self, start_time, end_time):
        """
        Generates time slots for a specific period.
        """
        slots = []
        current_time = datetime.combine(datetime.today(), start_time)
        end_time = datetime.combine(datetime.today(), end_time)

        while current_time + timedelta(minutes=30) <= end_time:
            slot_start = current_time.time()
            slot_end = (current_time + timedelta(minutes=30)).time()
            slots.append((slot_start, slot_end))
            current_time += timedelta(minutes=30)

        print(slots, '---------')

        return slots

    def generate_slots_for_day(self, day_of_week):
        """
        Generates time slots for a specific day based on morning and afternoon periods.
        """
        slots = []
        working_periods = self.working_periods.filter(day_of_week=day_of_week)

        for period in working_periods:
            if period.morning_start and period.morning_end:
                slots.extend(self.generate_slots_for_period(period.morning_start, period.morning_end))

            if period.afternoon_start and period.afternoon_end:
                slots.extend(self.generate_slots_for_period(period.afternoon_start, period.afternoon_end))
        print(slots, '1111111111111111111111')
        return slots

    def generate_weekly_slots(self):
        weekly_slots = {}
        days_of_week = DayOfWeek.objects.all()

        for day in days_of_week:
            slots = self.generate_slots_for_day(day)
            if slots:
                weekly_slots[day.name] = slots

        return weekly_slots

    class Meta:
        verbose_name_plural = "Doctors"


class TeleDoctor(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    doctors_name = models.CharField(max_length=255, blank=True)  # Leave it blank initially
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=255, blank=True)  # Leave it blank initially

    def save(self, *args, **kwargs):
        # Dynamically set the doctor's name from the related Doctor object
        if self.doctor:
            self.doctors_name = self.doctor.name  # Assuming 'name' field exists in Doctor model

        # Dynamically set the parent's name from the related CustomUser object
        if self.user:
            self.parent_name = f'{self.user.first_name} {self.user.last_name}'  # Assuming these fields exist in CustomUser

        super().save(*args, **kwargs)

    def __str__(self):
        return f"TeleDoctor with {self.doctors_name} and parent {self.parent_name}"



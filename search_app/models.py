from django.db import models

# Create your models here.


class Participant(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.age} {self.sex}"

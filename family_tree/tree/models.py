from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    # Список вариантов для выбора гендера
    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDERS)
    birth_date = models.DateField(blank=True, null=True)
    mother = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children_from_mother'
    )
    father = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children_from_father'
    )
    creator_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='family_members'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
    birth_date = models.DateField()
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

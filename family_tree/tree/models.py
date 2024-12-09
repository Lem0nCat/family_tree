from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


class Generation(models.Model):
    """Модель для поколений"""
    generation_number = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    creator_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='gen'
    )

    def __str__(self):
        return f"Gen #{self.generation_number} - {self.creator_user}"


class Person(models.Model):
    """Модель для элементов дерева(людей)"""
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
    generation = models.ForeignKey(
        Generation,
        on_delete=models.PROTECT,
        related_name='person_gen'
    )
    creator_user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='family_members'
    )

    def __str__(self):
        return f"{self.generation} - {self.first_name} {self.last_name}"

    def clean(self):
        """Проверка данных модели"""
        # Проверка: Отец должен быть мужчиной
        if self.father and self.father.gender != 'male':
            raise ValidationError("Отец должен быть мужчиной.")

        # Проверка: Мать должна быть женщиной
        if self.mother and self.mother.gender != 'female':
            raise ValidationError("Мать должна быть женщиной.")

        # Проверка: Отец и мать не могут быть одним и тем же человеком
        if self.father and self.mother and self.father == self.mother:
            raise ValidationError("Отец и мать не могут быть одним и тем же человеком.")

        # Проверка: Отец и мать не могут быть из разных поколений
        if (self.father and self.mother
                and self.mother.generation.generation_number != self.father.generation.generation_number):
            raise ValidationError("Отец и мать должны быть из одного поколения")

        # Проверка: Ребенок должен быть на одно поколение старше своих родителей
        if self.mother and self.mother.generation and self.generation.generation_number != self.mother.generation.generation_number + 1:
            raise ValidationError("Мать должна быть на одно поколение старше ребенка.")

        if self.father and self.father.generation and self.generation.generation_number != self.father.generation.generation_number + 1:
            raise ValidationError("Отец должен быть на одно поколение старше ребенка.")

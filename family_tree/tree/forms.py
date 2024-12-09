from django import forms
from .models import Person


class PersonForm(forms.ModelForm):
    # Список вариантов для выбора гендера
    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию'
    }))
    gender = forms.ChoiceField(
        choices=GENDERS,
        label='Пол',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    birth_date = forms.DateField(label='Дата рождения',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': '01.01.0001'
        }),
        required=False
    )

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'gender', 'birth_date']

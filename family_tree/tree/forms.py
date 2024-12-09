from django import forms
from .models import Person


class PersonForm(forms.ModelForm):
    # Список вариантов для выбора гендера
    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию'
    }))
    gender = forms.ChoiceField(
        choices=GENDERS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',  # Указывает браузеру отображать выбор даты
            'placeholder': 'Выберите дату рождения'
        }),
        required=False
    )

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'gender', 'birth_date']

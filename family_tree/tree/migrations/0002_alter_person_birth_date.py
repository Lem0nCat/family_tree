# Generated by Django 5.1.4 on 2024-12-08 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
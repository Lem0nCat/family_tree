# Generated by Django 5.1.4 on 2024-12-09 02:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0004_generation_creator_user_alter_person_generation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children_from_father', to='tree.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children_from_mother', to='tree.person'),
        ),
    ]
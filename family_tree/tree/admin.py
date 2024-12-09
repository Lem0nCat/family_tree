from django.contrib import admin

from .models import Person, Generation

admin.site.register(Person)
admin.site.register(Generation)

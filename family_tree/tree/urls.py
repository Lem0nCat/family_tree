from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('tree/', views.family_tree, name='family_tree'),
    path('add/', views.add_person, name='add_person'),
    path('add/<int:person_id>/', views.add_person_with_parent, name='add_person_with_parent'),
    path('add_to_gen/<int:generation_number>/', views.add_person_to_gen, name='add_person_to_gen'),
    path('edit/<int:person_id>/', views.edit_person, name='edit_person'),
    path('delete/<int:person_id>/', views.delete_person, name='delete_person'),
]

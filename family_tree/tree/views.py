from traceback import print_tb

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

from .forms import PersonForm
from .models import Person


def index(request):
    return render(request, 'tree/index.html')


def family_tree(request):
    # Получаем всех людей с их поколениями
    all_people = Person.objects.select_related('generation').filter(creator_user=request.user)
    print(all_people)

    # Группируем людей по поколениям
    tree_levels = {}

    for person in all_people:
        generation_number = person.generation.generation_number
        if generation_number not in tree_levels:
            tree_levels[generation_number] = []
        tree_levels[generation_number].append(person)

    # Сортируем поколения в обратном порядке (младшие вверху)
    sorted_tree_levels = sorted(tree_levels.items(), key=lambda x: x[0], reverse=True)
    print(sorted_tree_levels)

    context = {
        'tree_levels': [level[1] for level in sorted_tree_levels]
        # Убираем ключ поколения, оставляем только список людей
    }

    return render(request, 'tree/family_tree.html', context)


def add_person(request, mother_id=None, father_id=None):
    mother = get_object_or_404(Person, id=mother_id) if mother_id else None
    father = get_object_or_404(Person, id=father_id) if father_id else None
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            if mother:
                person.mother = mother
            if father:
                person.father = father

            person.creator_user = request.user
            person.save()

            return redirect('family_tree')
    else:
        form = PersonForm()
    return render(request, 'tree/add_person.html', {'form': form, 'mother': mother, 'father': father})


def edit_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('family_tree')
    else:
        form = PersonForm(instance=person)
    return render(request, 'tree/edit_person.html', {'form': form})


def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        person.delete()
        return redirect('family_tree')
    return render(request, 'tree/delete_person.html', {'person': person})

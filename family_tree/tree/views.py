from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import PersonForm
from .models import Person, Generation


def index(request):
    return render(request, 'tree/index.html')


@login_required(login_url='users:login')
def family_tree(request):
    # Получаем всех людей с их поколениями и родителями
    all_people = Person.objects.select_related('generation', 'mother', 'father').filter(creator_user=request.user)

    # Группируем людей по поколениям
    tree_levels = {}

    if not all_people:
        tree_levels[1] = None

    for person in all_people:
        generation_number = person.generation.generation_number
        if generation_number not in tree_levels:
            tree_levels[generation_number] = []

        # Формируем структуру для отображения связей
        person_data = {
            'id': person.id,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'mother': f"{person.mother.first_name} {person.mother.last_name}" if person.mother else None,
            'father': f"{person.father.first_name} {person.father.last_name}" if person.father else None,
        }
        tree_levels[generation_number].append(person_data)

    # Сортируем поколения в обратном порядке (младшие вверху)
    sorted_tree_levels = sorted(tree_levels.items(), key=lambda x: x[0], reverse=True)

    return render(request, 'tree/family_tree.html', {'tree_levels': sorted_tree_levels})


@login_required(login_url='users:login')
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            new_person = form.save(commit=False)

            # Проверяем, указано ли поколение
            generation_number = request.POST.get('generation_number')
            if generation_number:
                generation, created = Generation.objects.get_or_create(
                    generation_number=generation_number
                )
                new_person.generation = generation

            # Сохраняем пользователя
            new_person.creator_user = request.user
            new_person.save()
            return redirect('family_tree')
    else:
        form = PersonForm()

    return render(request, 'tree/add_person.html', {'form': form})


@login_required(login_url='users:login')
def add_person_to_gen(request, generation_number):
    if generation_number > 1:
        previous_generation = Generation.objects.filter(generation_number=generation_number - 1,
                                                        creator_user=request.user).first()
    else:
        previous_generation = None

    if request.method == 'POST':
        # Находим или создаем поколение
        generation, _ = Generation.objects.get_or_create(
            generation_number=generation_number,
            creator_user=request.user
        )

        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.generation = generation
            person.creator_user = request.user

            # Установить родителей, если они были выбраны
            mother_id = request.POST.get('mother')
            father_id = request.POST.get('father')

            if mother_id:
                person.mother = Person.objects.get(id=mother_id)
            if father_id:
                person.father = Person.objects.get(id=father_id)

            person.save()
            return redirect('family_tree')
    else:
        form = PersonForm()

    # Получаем список возможных родителей из предыдущего поколения
    possible_mothers = Person.objects.filter(generation=previous_generation,
                                             gender='female') if previous_generation else []
    possible_fathers = Person.objects.filter(generation=previous_generation,
                                             gender='male') if previous_generation else []

    return render(request, 'tree/add_person.html', {
        'form': form,
        'generation_number': generation_number,
        'possible_mothers': possible_mothers,
        'possible_fathers': possible_fathers
    })


@login_required(login_url='users:login')
def add_person_with_parent(request, person_id):
    parent = get_object_or_404(Person, id=person_id)
    gen_num = parent.generation.generation_number

    if request.method == 'POST':
        next_gen, _ = Generation.objects.get_or_create(
            generation_number=(gen_num + 1),
            creator_user=request.user
        )

        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.generation = next_gen
            person.creator_user = request.user

            # Один родитель уже выбран, добавляем второго
            if parent.gender == 'male':
                person.father = parent
                mother_id = request.POST.get('mother')
                if mother_id:
                    person.mother = Person.objects.get(id=mother_id)
            else:
                person.mother = parent
                father_id = request.POST.get('father')
                if father_id:
                    person.father = Person.objects.get(id=father_id)

            person.save()
            return redirect('family_tree')
    else:
        form = PersonForm()

    # Получаем список второго родителя
    possible_mothers = Person.objects.filter(generation=parent.generation,
                                             gender='female') if parent.gender == 'male' else []
    possible_fathers = Person.objects.filter(generation=parent.generation,
                                             gender='male') if parent.gender == 'female' else []

    return render(request, 'tree/add_person_with_parents.html', {
        'form': form,
        'parent': parent,
        'possible_mothers': possible_mothers,
        'possible_fathers': possible_fathers
    })


@login_required(login_url='users:login')
def edit_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('family_tree')
    else:
        form = PersonForm(instance=person)
    return render(request, 'tree/edit_person.html', {'form': form, 'person': person})


@login_required(login_url='users:login')
def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    generation = person.generation
    person.delete()

    # Проверяем, осталось ли в поколении люди
    if not Person.objects.filter(generation=generation).exists():
        generation.delete()

    return redirect('family_tree')

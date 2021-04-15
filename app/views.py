from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    if request.GET['from-landing'] == 'original':
        counter_click['original'] += 1
        print(counter_click)
    elif request.GET['from-landing'] == 'test':
        counter_click['test'] += 1
        print(counter_click)
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    page = request.GET['ab-test-arg']
    if page == 'original':
        counter_show['original'] += 1
        print(counter_show)
        return render(request, 'landing.html')
    elif page == 'test':
        counter_show['test'] += 1
        print(counter_show)
        return render(request, 'landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    return render(request, 'stats.html', context={
        'test_conversion': counter_show['original'] / counter_click['original'],
        'original_conversion': counter_show['test'] / counter_click['test'],
    })

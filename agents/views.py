from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Agent, Bso, PolicyAgents
from main.models import Company, Type


@login_required(login_url='login')
def add_agent(request):
    # Добавление нового агента
    if request.user.admin:
        text = ''
        if request.method == 'POST':
            if len(Agent.objects.filter(name=request.POST.get('name'))) > 0:
                text = 'Агент с таким именем уже есть в системе'
            else:
                Agent(
                    name=request.POST.get('name'),
                    storage_time=request.POST.get('storage_time'),
                ).save()

                text = 'Агент добавлен'

        return render(request, 'agents/add_agent.html', context={'text': text})

    else:
        return render(request, 'agents/add_agent.html',
                      context={'text': 'Для регистрации обратитесь к администратору!'})


@login_required(login_url='login')
def issuance_bso(request):
    agents = Agent.objects.all()
    company = Company.objects.all()
    errors = {}
    text = ''
    text_errors = 0
    if request.method == 'POST':
        number = int(request.POST.get('number'))
        for i in range(0, int(request.POST.get('range'))):
            bso, created = Bso.objects.get_or_create(
                series=request.POST.get('series'),
                number=number,
                defaults={
                    'company': Company.objects.get(id=request.POST.get('company')),
                    'agent': Agent.objects.get(id=request.POST.get('agent')),
                    'date_at': datetime.today().date(),
                }
            )

            if created == False:
                errors[f'{bso.series} {bso.number}'] = bso.agent

            number += 1

        text = f'Добавлено {int(request.POST.get("range")) - len(errors)}'
        if len(errors) > 0:
            text_errors = f'Пропущено {len(errors)}'

    context = {
        'agents': agents,
        'company': company,
        'text': text,
        'text_errors': text_errors,
        'errors': errors,
    }
    return render(request, 'agents/issuance_bso.html', context=context)


@login_required(login_url='login')
def get_statistic(request):
    agents = Agent.objects.all()
    bso = Bso.objects.all()
    text_search = ''
    if 'agent' in request.GET and request.GET.get('agent') != 'all':
        bso = bso.filter(agent_id=request.GET.get('agent'))
    if 'search' in request.GET:
        bso = bso.filter(number__icontains=request.GET.get('search'))
        text_search = f'Найдено {len(bso)} БСО'

    context = {
        'agents': agents,
        'bso': bso,
        'text_search': text_search,
    }

    return render(request, 'agents/get_statistic.html', context)


@login_required(login_url='login')
def accept(request):
    pass

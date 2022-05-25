import csv
import datetime
from openpyxl import load_workbook

from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Agent, Bso, PolicyAgents
from main.models import Company, Type

from main.views import get_start_end_date


@login_required(login_url='login')
def issuance_bso(request):
    agents = Agent.objects.all()
    company = Company.objects.all()
    errors = {}
    text_bso = ''
    text_errors_bso = 0
    if request.method == 'POST':
        number = int(request.POST.get('number'))
        for i in range(0, int(request.POST.get('range'))):
            bso, created = Bso.objects.get_or_create(
                series=request.POST.get('series'),
                number=number,
                defaults={
                    'company': Company.objects.get(id=request.POST.get('company')),
                    'agent': Agent.objects.get(id=request.POST.get('agent')),
                    'date_at': datetime.datetime.today().date(),
                }
            )

            if created == False:
                errors[f'{bso.series} {bso.number}'] = bso.agent

            number += 1

        text_bso = f'Добавлено {int(request.POST.get("range")) - len(errors)}'
        if len(errors) > 0:
            text_errors_bso = f'Пропущено {len(errors)}'

    bso = Bso.objects.all()
    text_search = ''
    if 'agent' in request.GET and request.GET.get('agent') != 'all':
        bso = bso.filter(agent_id=request.GET.get('agent'))
    if 'search' in request.GET:
        bso = bso.filter(number__icontains=request.GET.get('search'))
        text_search = f'Найдено {len(bso)} БСО'

    # ссылка с параметрами для пагинации
    link = '?'
    for key, value in request.GET.items():
        if key == 'page':
            continue
        link = link + f'{key}={value}&'

    paginator = Paginator(bso, 15)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)

    context = {
        'agents': agents,
        'company': company,
        'text_bso': text_bso,
        'text_errors_bso': text_errors_bso,
        'errors': errors,
        'bso': page.object_list,
        'text_search': text_search,
        'page': page,
        'link': link,
        'paginator': paginator,
    }
    return render(request, 'agents/issuance_bso.html', context)


@login_required(login_url='login')
def receivable(request):
    text = ''
    text_errors = 0
    errors = []
    selected = {}
    text_agent = ''

    if request.method == 'POST':
        if 'status_for_change' in request.POST:
            policy_for_change = PolicyAgents.objects.get(id=request.POST.get('if_policy_for_change'))
            policy_for_change.status = request.POST.get('status_for_change')
            policy_for_change.save()

        elif 'name' in request.POST:
            agent, created = Agent.objects.get_or_create(
                name=request.POST.get('name'),
                defaults={
                    'storage_time': request.POST.get('storage_time')
                }
            )

            if created:
                text_agent = 'Агент добавлен'
            else:
                text_agent = 'Агент с таким именем уже есть в системе'

        else:
            wb = load_workbook(filename=request.FILES['file'])
            sheet = wb.worksheets[0]
            number = 0
            for row in range(2, sheet.max_row):
                if sheet[row][0].value is None:
                    continue
                if isinstance(sheet[row][6].value, str):
                    date_registration = f'{sheet[row][6].value[6:10]}-' \
                                        f'{sheet[row][6].value[3:5]}-' \
                                        f'{sheet[row][6].value[0:2]}'
                else:
                    date_registration = f'{sheet[row][6].value.year}-' \
                                        f'{sheet[row][6].value.month}-' \
                                        f'{sheet[row][6].value.day}'

                if isinstance(sheet[row][7].value, str):
                    date_start = f'{sheet[row][7].value[6:10]}-' \
                                        f'{sheet[row][7].value[3:5]}-' \
                                        f'{sheet[row][7].value[0:2]}'
                else:
                    date_start = f'{sheet[row][7].value.year}-' \
                                        f'{sheet[row][7].value.month}-' \
                                        f'{sheet[row][7].value.day}'

                if isinstance(sheet[row][8].value, str):
                    date_end = f'{sheet[row][8].value[6:10]}-' \
                                        f'{sheet[row][8].value[3:5]}-' \
                                        f'{sheet[row][8].value[0:2]}'
                else:
                    date_end = f'{sheet[row][8].value.year}-' \
                                        f'{sheet[row][8].value.month}-' \
                                        f'{sheet[row][8].value.day}'

                policy, created = PolicyAgents.objects.get_or_create(
                    policy=sheet[row][1].value,
                    defaults={
                        'agent': Agent.objects.get(id=request.POST.get('agent')),
                        'type': Type.objects.get_or_create(name=sheet[row][0].value)[0],
                        'type_client': sheet[row][2].value,
                        'client': sheet[row][3].value,
                        'agent_commission':
                            float(str(sheet[row][4].value).replace(',', '.').replace(' ', '')),
                        'agent_commission_rub': float((
                                float(str(sheet[row][4].value).replace(',', '.').replace(' ', '')) *
                                float(str(sheet[row][9].value).replace(',', '.').replace(' ', ''))
                        ) / 100),
                        'date_registration': date_registration,
                        'date_start': date_start,
                        'date_end': date_end,
                        'price': float(str(sheet[row][9].value).replace(',', '.').replace(' ', '')),
                        'type_pay': sheet[row][10].value,
                    }
                )

                if 'б' not in sheet[row][10].value.lower():
                    policy.status = 'receivable'
                    policy.save()

                if created:
                    number += 1

            text = f'Загруженно {number - len(errors)}'

            if len(errors) > 0:
                text_errors = f'Пропущенно {len(errors)}'

    if request.GET.get('date_start') == None and request.GET.get('date_end') == None:
        date_start, date_end = get_start_end_date()
        date_start = date_start.strftime("%Y-%m-%d")
        date_end = date_end.strftime("%Y-%m-%d")
    else:
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')

    agents = Agent.objects.all()

    if 'search' in request.GET:
        policy = PolicyAgents.objects.filter(
            Q(client__iregex=request.GET.get('search')) |
            Q(policy__iregex=request.GET.get('search'))
        )

    else:
        policy = PolicyAgents.objects.filter(
            date_registration__lt=date_end,
            date_registration__gte=date_start,
        )

        if 'status' in request.GET and request.GET.get('status') != 'all':
            selected['status'] = request.GET.get("status")
            policy = policy.filter(status=request.GET.get("status"))
        if 'agent' in request.GET and request.GET.get('agent') != 'all':
            selected['agent'] = int(request.GET.get("agent"))
            policy = policy.filter(agent_id=request.GET.get("agent"))

    # ссылка с параметрами для пагинации
    link = '?'
    for key, value in request.GET.items():
        if key == 'page':
            continue
        link = link + f'{key}={value}&'

    paginator = Paginator(policy, 15)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)

    context = {
        'agents': agents,
        'policy': page.object_list,
        'date_start': date_start,
        'date_end': date_end,
        'text': text,
        'text_errors': text_errors,
        'errors': errors,
        'selected': selected,
        'text_agent': text_agent,
        'page': page,
        'link': link,
        'paginator': paginator,
    }

    return render(request, 'agents/receivable.html', context)

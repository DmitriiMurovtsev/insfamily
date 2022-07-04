import datetime
import os

import openpyxl
from django.http import HttpResponse
from openpyxl import load_workbook

from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Agent, Bso, PolicyAgents, HistoryBso, StatusBso
from main.models import Company, Type

from main.views import get_start_end_date


@login_required(login_url='login')
def issuance_bso(request):
    agents = Agent.objects.all()
    company = Company.objects.all()
    status_bso = StatusBso.objects.all()
    bso_for_agents = Bso.objects.filter(clear=True)
    errors = {}
    selected = {}
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    text_bso = ''
    text_errors_bso = 0
    if request.method == 'POST':
        if 'add_status_bso' in request.POST:
            # Создание статуса бланка
            StatusBso.objects.get_or_create(name=request.POST['status_name'])

        if 'bso_in_agents' in request.POST:
            # Передача БСО со склада агенту
            for bso_id in request.POST:
                if 'check_bso' in bso_id:
                    bso_for_edit = Bso.objects.get(id=request.POST[bso_id])
                    bso_for_edit.agent = Agent.objects.get(id=request.POST['agent'])
                    bso_for_edit.clear = False
                    bso_for_edit.save()

                    status, created = StatusBso.objects.get_or_create(name='Выдан агенту')
                    new_history, created = HistoryBso.objects.get_or_create(
                        date_at=datetime.datetime.now().date(),
                        status=status,
                        bso=bso_for_edit,
                    )

        if 'add_new_bso' in request.POST:
            # Добавление новых БСО на склад вручную
            for i in range(int(request.POST['range'])):
                new_bso, created = Bso.objects.get_or_create(
                    series=request.POST['series'],
                    number=int(request.POST['number']) + i,
                    company_id=request.POST['company'],
                    defaults={
                        'date_add': request.POST['date_add'],
                    }
                )

                if not created:
                    errors[f'{new_bso.series} {new_bso.number}'] = 'Уже есть в системе'

                else:
                    status, created = StatusBso.objects.get_or_create(name='Чистый')
                    new_history, created = HistoryBso.objects.get_or_create(
                        date_at=datetime.datetime.now().date(),
                        status=status,
                        bso=new_bso,
                    )

                if len(errors) > 0:
                    # Выгрузка незагруженных БСО в xlsx
                    pass

        if 'add_new_bso_from_file' in request.POST:
            # Загрузка БСО из файла
            errors = {}
            wb = load_workbook(filename=request.FILES['file'])
            sheet = wb.worksheets[0]
            number = 0
            i = 2
            while True:
                if sheet[i][0].value is None or sheet[i][0].value == '':
                    break
                company_for_new_bso, created = Company.objects.get_or_create(name=sheet[i][2].value)
                new_bso, created = Bso.objects.get_or_create(
                    series=sheet[i][0].value,
                    number=sheet[i][1].value,
                    company=company_for_new_bso,
                    defaults={
                        'date_add': datetime.datetime.now().date(),
                    }
                )

                if not created:
                    errors[f'{new_bso.series} {new_bso.number}'] = 'Уже есть в системе'
                else:
                    status, created = StatusBso.objects.get_or_create(name='Чистый')
                    new_history, created = HistoryBso.objects.get_or_create(
                        date_at=datetime.datetime.now().date(),
                        status=status,
                        bso=new_bso,
                    )

                i += 1

            if len(errors) > 0:
                # Выгрузка незагруженных БСО в xlsx
                pass

    bso = Bso.objects.all()

    text_search = ''
    if 'search' in request.GET:
        bso = bso.filter(number__icontains=request.GET.get('search'))
        text_search = f'Найдено {len(bso)} БСО'

    else:
        if 'agent' in request.GET and request.GET.get('agent') != 'all':
            # Сортировка по агенту
            bso = bso.filter(agent_id=request.GET.get('agent'))
            selected['agent'] = int(request.GET.get('agent'))

        if 'status_bso' in request.GET:
            # Сортировка по статусу БСО
            if request.GET['status_bso'] != 'all':
                selected['status_bso'] = int(request.GET['status_bso'])
                status_for_filter = StatusBso.objects.get(id=request.GET['status_bso'])
                bso_list = []
                for b in bso:
                    # Выборка актуального статуса
                    old_history = HistoryBso.objects.filter(bso_id=b.id)[0]
                    for his in HistoryBso.objects.filter(bso_id=b.id):
                        if his.id > old_history.id:
                            old_history = his
                    if status_for_filter == old_history.status:
                        bso_list.append(b)
                bso = bso_list

    bso_list = []
    for b in bso:
        temp_dict = {}
        temp_dict['id'] = b.id
        temp_dict['company'] = b.company.name
        temp_dict['series'] = b.series
        temp_dict['number'] = b.number
        temp_dict['date_add'] = b.date_add

        old_history = HistoryBso.objects.filter(bso_id=b.id)[0]

        # Выборка актуального статуса
        for his in HistoryBso.objects.filter(bso_id=b.id):
            if his.id > old_history.id:
                old_history = his

        temp_dict['history_status'] = old_history.status
        temp_dict['history_date_at'] = old_history.date_at
        temp_dict['history'] = HistoryBso.objects.filter(bso_id=b.id)
        temp_dict['agent'] = b.agent
        bso_list.append(temp_dict)

    # ссылка с параметрами для пагинации
    link = '?'
    for key, value in request.GET.items():
        if key == 'page' or key == 'page_2':
            continue
        link = link + f'{key}={value}&'

    paginator = Paginator(bso_list, 15)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)

    paginator_2 = Paginator(bso_for_agents, 20)
    current_page_2 = request.GET.get('page_2', 1)
    page_2 = paginator_2.get_page(current_page_2)

    context = {
        'agents': agents,
        'status_bso': status_bso,
        'date_now': date_now,
        'selected': selected,
        'company': company,
        'text_bso': text_bso,
        'text_errors_bso': text_errors_bso,
        'errors': errors,
        'bso_list': page.object_list,
        'bso_for_agents': page_2.object_list,
        'text_search': text_search,
        'page': page,
        'page_2': page_2,
        'link': link,
        'paginator': paginator,
        'paginator_2': paginator_2,
    }
    return render(request, 'agents/issuance_bso.html', context)


@login_required(login_url='login')
def receivable(request):
    text = ''
    text_errors = 0
    errors = []
    selected = {}
    text_agent = ''
    type = Type.objects.all()

    if request.method == 'POST':
        # смена статуса по полису
        if 'status_for_change' in request.POST:
            policy_for_change = PolicyAgents.objects.get(id=request.POST.get('if_policy_for_change'))
            policy_for_change.status = request.POST.get('status_for_change')
            policy_for_change.save()

        elif 'name' in request.POST:
            # добавление агента
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
            # загрузка агентских продаж из файла
            wb = load_workbook(filename=request.FILES['file'])
            sheet = wb.worksheets[0]
            number = 0
            for row in range(2, sheet.max_row+1):
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

    if 'date_start' not in request.GET and 'date_end' not in request.GET:
        date_start, date_end = get_start_end_date()
        date_start = date_start.strftime("%Y-%m-%d")
        date_end = date_end.strftime("%Y-%m-%d")
    else:
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')

    agents = Agent.objects.all()

    if 'search' in request.GET:
        # поиск по страхователю или по номеру полиса
        policy = PolicyAgents.objects.filter(
            Q(client__iregex=request.GET.get('search')) |
            Q(policy__iregex=request.GET.get('search'))
        )

    else:
        # отбор полисов, оформленных за период (текущий месяц по умолчанию)
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

    # пагинация результата
    paginator = Paginator(policy, 15)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)

    context = {
        'agents': agents,
        'type': type,
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


@login_required(login_url='login')
def unload_receivable(request):
    # выгрузка агентских продаж в xlsx
    if request.user.admin:
        if request.method == 'POST':
            policy = PolicyAgents.objects.filter(
                date_registration__gte=request.POST['date_start'],
                date_registration__lt=request.POST['date_end'],
            )

            if request.POST['status'] != 'all':
                policy = policy.filter(status=request.POST['status'])
            if request.POST['agent'] != 'all':
                policy = policy.filter(agent_id=request.POST['agent'])
            if request.POST['type'] != 'all':
                policy = policy.filter(type_id=request.POST['type'])

            wb = openpyxl.Workbook()
            sheet = wb['Sheet']

            sheet['A1'] = '№'
            sheet['B1'] = 'Агент'
            sheet['C1'] = 'Тип полиса'
            sheet['D1'] = 'Полис'
            sheet['E1'] = 'Клиент'
            sheet['F1'] = 'Тип клиента'
            sheet['G1'] = 'Комиссия агента в %'
            sheet['H1'] = 'Комиссия агента в руб.'
            sheet['I1'] = 'Дата подписания договора'
            sheet['J1'] = 'Дата начала действия'
            sheet['K1'] = 'Дата окончания действия'
            sheet['L1'] = 'Общая премия'
            sheet['M1'] = 'Тип оплаты'
            sheet['N1'] = 'Статус полиса'

            wb.save('agents/file/receivable.xlsx')

            wb = openpyxl.load_workbook('agents/file/receivable.xlsx')
            sheet = wb['Sheet']

            str_number = 2
            for policy in policy:
                sheet[str_number][0].value = str_number - 1
                sheet[str_number][1].value = policy.agent.name
                sheet[str_number][2].value = policy.type.name
                sheet[str_number][3].value = policy.policy
                sheet[str_number][4].value = policy.client
                sheet[str_number][5].value = policy.type_client
                sheet[str_number][6].value = policy.agent_commission
                sheet[str_number][7].value = policy.agent_commission_rub
                sheet[str_number][8].value = policy.date_registration
                sheet[str_number][9].value = policy.date_start
                sheet[str_number][10].value = policy.date_end
                sheet[str_number][11].value = policy.price
                sheet[str_number][12].value = policy.type_pay
                if policy.status == 'receivable':
                    sheet[str_number][13].value = 'Дебиторка'
                elif policy.status == 'reconciliation':
                    sheet[str_number][13].value = 'Сверки'
                elif policy.status == 'accept':
                    sheet[str_number][13].value = 'Акцепт'

                str_number += 1

            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="receivable.xlsx"'

            wb.save(response)

            return response


@login_required(login_url='login')
def test_upload(request):
    if 'upload' in request.POST:
        headers = {}
        agents = Agent.objects.all()

        headers_for_upload = {
            'Полис': 'policy',
            'Тип полиса': 'type',
            'Страхователь': 'client',
            'Тип страхователя': 'type_client',
            'Дата подписания договора': 'date_at',
            'Начало': 'date_start',
            'Окончание': 'date_end',
            'Общая премия': 'sp',
            'Тип оплаты': 'type_pay',
            'Страховая компания': 'company',
            'Канал продаж': 'channel',
        }

        wb = openpyxl.load_workbook(filename=request.FILES['file'])
        sheet = wb.worksheets[0]

        col = 0
        step_upload = 1
        while True:
            try:
                if sheet[1][col].value is not None:
                    headers[col] = sheet[1][col].value
                else:
                    break
                col += 1
            except:
                break

        wb.save('agents/file/upload.xlsx')

        context = {
            'headers': headers,
            'agents': agents,
            'step_upload': step_upload,
            'headers_for_upload': headers_for_upload,
        }

        return render(request, 'agents/test_upload.html', context)

    if 'step_upload' in request.POST:
        wb = openpyxl.load_workbook('agents/file/upload.xlsx')
        sheet = wb.worksheets[0]

        number = 0
        errors = {}
        row = 2

        while True:
            if sheet[row][0].value is not None:
                if isinstance(sheet[row][int(request.POST["date_at"])].value, str):
                    date_registration = f'{sheet[row][int(request.POST["date_at"])].value[6:10]}-' \
                                        f'{sheet[row][int(request.POST["date_at"])].value[3:5]}-' \
                                        f'{sheet[row][int(request.POST["date_at"])].value[0:2]}'
                else:
                    date_registration = f'{sheet[row][int(request.POST["date_at"])].value.year}-' \
                                        f'{sheet[row][int(request.POST["date_at"])].value.month}-' \
                                        f'{sheet[row][int(request.POST["date_at"])].value.day}'

                if isinstance(sheet[row][int(request.POST["date_start"])].value, str):
                    date_start = f'{sheet[row][int(request.POST["date_start"])].value[6:10]}-' \
                                        f'{sheet[row][int(request.POST["date_start"])].value[3:5]}-' \
                                        f'{sheet[row][int(request.POST["date_start"])].value[0:2]}'
                else:
                    date_start = f'{sheet[row][int(request.POST["date_start"])].value.year}-' \
                                        f'{sheet[row][int(request.POST["date_start"])].value.month}-' \
                                        f'{sheet[row][int(request.POST["date_start"])].value.day}'

                if isinstance(sheet[row][int(request.POST["date_end"])].value, str):
                    date_end = f'{sheet[row][int(request.POST["date_end"])].value[6:10]}-' \
                                        f'{sheet[row][int(request.POST["date_end"])].value[3:5]}-' \
                                        f'{sheet[row][int(request.POST["date_end"])].value[0:2]}'
                else:
                    date_end = f'{sheet[row][int(request.POST["date_end"])].value.year}-' \
                                        f'{sheet[row][int(request.POST["date_end"])].value.month}-' \
                                        f'{sheet[row][int(request.POST["date_end"])].value.day}'
                policy, created = PolicyAgents.objects.get_or_create(
                    policy=sheet[row][int(request.POST["policy"])].value,
                    defaults={
                        'agent': Agent.objects.get(id=request.POST.get('agent')),
                        'type': Type.objects.get_or_create(name=sheet[row][int(request.POST["type"])].value)[0],
                        'type_client': sheet[row][int(request.POST["type_client"])].value,
                        'client': sheet[row][int(request.POST["client"])].value,
                        'date_registration': date_registration,
                        'date_start': date_start,
                        'date_end': date_end,
                        'price': float(str(sheet[row][int(request.POST["sp"])].value).replace(',', '.').replace(' ', '')),
                        'type_pay': sheet[row][int(request.POST["type_pay"])].value,
                        'agent_commission_rub': 0,
                        'agent_commission': 0,
                    }
                )

                if created:
                    number += 1
                    if 'б' not in sheet[row][int(request.POST["type_pay"])].value.lower():
                        policy.status = 'receivable'
                        policy.save()
                else:
                    errors[policy] = f'Полис {policy} уже есть в системе'

                row += 1

            else:
                break

        os.remove('agents/file/upload.xlsx')

        text = f'Загружено {number}'
        text_errors = f'Пропущенно {len(errors)}'

        context = {
            'errors': errors,
            'text': text,
            'text_errors': text_errors,
        }

        return render(request, 'agents/test_upload.html', context)

    context = {}
    return render(request, 'agents/test_upload.html', context)

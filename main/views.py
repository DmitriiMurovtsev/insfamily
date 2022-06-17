import datetime
import csv

import openpyxl
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from openpyxl import load_workbook

from .models import Policy, Client, Channel, Company, User, Type, MortgagePolicy, Bank, Commission
from .forms import UploadFileForm


def redirect_login(request):
    # Перенаправление с главной страницы
    return redirect('add_policy')


def get_start_end_date():
    # Получение первого и последнего дня текущего месяца
    now = datetime.datetime.now()
    date_start = datetime.datetime(now.year, now.month, 1).date()
    next_month = date_start + datetime.timedelta(35)
    date_end = datetime.datetime(next_month.year, next_month.month, 1).date()
    return date_start, date_end


@login_required(login_url='login')
def unload_files(request):
    # Выгрузка сверок в файл
    if request.user.admin:
        result = Policy.objects.filter(
            date_registration__lt=request.GET.get('date_end'),
            date_registration__gte=request.GET.get('date_start'),
            accept=False,
        )
        if request.GET.get('Менеджер') != 'all':
            result = result.filter(user=request.GET.get('Менеджер'))
        if request.GET.get('Канал продаж') != 'all':
            result = result.filter(channel=request.GET.get('Канал продаж'))
        if request.GET.get('Страховая компания') != 'all':
            result = result.filter(company=request.GET.get('Страховая компания'))
        if request.GET.get('Тип полиса') != 'all':
            result = result.filter(type=request.GET.get('Тип полиса'))

    wb = openpyxl.Workbook()
    sheet = wb['Sheet']

    sheet['A1'] = '№'
    sheet['B1'] = 'Клиент'
    sheet['C1'] = 'Страховая компания'
    sheet['D1'] = 'Канал продаж'
    sheet['E1'] = 'Тип полиса'
    sheet['F1'] = 'Серия'
    sheet['G1'] = 'Номер'
    sheet['H1'] = 'Банк'
    sheet['I1'] = 'Премия'
    sheet['J1'] = 'КВ'
    sheet['K1'] = 'Дата оформления'
    sheet['L1'] = 'Дата начала действия'
    sheet['M1'] = 'Дата окончания действия'

    wb.save('main/file/mortgage.xlsx')

    wb = openpyxl.load_workbook('main/file/mortgage.xlsx')
    sheet = wb['Sheet']

    str_number = 2
    for policy in result:
        sheet[str_number][0].value = str_number - 1
        sheet[str_number][1].value = f'{policy.client.last_name} ' \
                                     f'{policy.client.first_name} ' \
                                     f'{policy.client.middle_name}'
        sheet[str_number][2].value = policy.company.name
        sheet[str_number][3].value = policy.channel.name
        sheet[str_number][4].value = policy.type.name
        sheet[str_number][5].value = policy.series
        sheet[str_number][6].value = policy.number
        sheet[str_number][7].value = policy.bank
        sheet[str_number][8].value = policy.sp
        sheet[str_number][9].value = policy.commission
        sheet[str_number][10].value = policy.date_registration
        sheet[str_number][11].value = policy.date_start
        sheet[str_number][12].value = policy.date_end

        str_number += 1

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="receivable.xlsx"'

    wb.save(response)

    return response


@login_required(login_url='login')
def unload_accept(request):
    # Выгрузка акцептованных полисов в xlsx
    if request.user.admin:
        result = Policy.objects.filter(
            date_registration__lt=request.GET.get('date_end'),
            date_registration__gte=request.GET.get('date_start'),
            accept=True,
        )
        if request.GET.get('Менеджер') != 'all':
            result = result.filter(user=request.GET.get('Менеджер'))
        if request.GET.get('Канал продаж') != 'all':
            result = result.filter(channel=request.GET.get('Канал продаж'))
        if request.GET.get('Страховая компания') != 'all':
            result = result.filter(company=request.GET.get('Страховая компания'))
        if request.GET.get('Тип полиса') != 'all':
            result = result.filter(type=request.GET.get('Тип полиса'))

        wb = openpyxl.Workbook()
        sheet = wb['Sheet']

        sheet['A1'] = '№'
        sheet['B1'] = 'Клиент'
        sheet['C1'] = 'Страховая компания'
        sheet['D1'] = 'Канал продаж'
        sheet['E1'] = 'Тип полиса'
        sheet['F1'] = 'Серия'
        sheet['G1'] = 'Номер'
        sheet['H1'] = 'Банк'
        sheet['I1'] = 'Премия'
        sheet['J1'] = 'КВ'
        sheet['K1'] = 'Дата оформления'
        sheet['L1'] = 'Дата начала действия'
        sheet['M1'] = 'Дата окончания действия'

        wb.save('main/file/mortgage.xlsx')

        wb = openpyxl.load_workbook('main/file/mortgage.xlsx')
        sheet = wb['Sheet']

        str_number = 2
        for policy in result:
            sheet[str_number][0].value = str_number - 1
            sheet[str_number][1].value = f'{policy.client.last_name} ' \
                                         f'{policy.client.first_name} ' \
                                         f'{policy.client.middle_name}'
            sheet[str_number][2].value = policy.company.name
            sheet[str_number][3].value = policy.channel.name
            sheet[str_number][4].value = policy.type.name
            sheet[str_number][5].value = policy.series
            sheet[str_number][6].value = policy.number
            sheet[str_number][7].value = policy.bank
            sheet[str_number][8].value = policy.sp
            sheet[str_number][9].value = policy.commission
            sheet[str_number][10].value = policy.date_registration
            sheet[str_number][11].value = policy.date_start
            sheet[str_number][12].value = policy.date_end

            str_number += 1

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="receivable.xlsx"'

        wb.save(response)

        return response


@login_required(login_url='login')
def statistic(request):
    # просмотр статистики
    all_statistic = {}
    user_statistic = {}
    agent_statistic = {}
    all_sp = 0
    date_start, date_end = get_start_end_date()
    if request.user.admin:
        police_for_type = Policy.objects.filter(date_registration__lt=date_end,
                                                date_registration__gte=date_start)
        users = User.objects.filter(agent=False, admin=False)
        agents = User.objects.filter(agent=True)
        for user in users:
            temp_dict = {}
            policy_user = police_for_type.filter(user=user.id)
            temp_dict['sp'] = int(sum(policy.sp for policy in policy_user))
            temp_dict['count'] = len(policy_user)
            user_statistic[user] = temp_dict
        for agent in agents:
            temp_dict = {}
            policy_agent = Policy.objects.filter(user=agent.id)
            temp_dict['sp'] = int(sum(policy.sp for policy in policy_agent))
            temp_dict['count'] = len(policy_agent)
            agent_statistic[agent] = temp_dict
    else:
        police_for_type = Policy.objects.filter(
            user=request.user.id,
            date_registration__lt=date_end,
            date_registration__gte=date_start
        )
    types = Type.objects.all()
    for type in types:
        temp_dict = {}
        policy_type = police_for_type.filter(type=type.id)
        temp_dict['count'] = len(policy_type)
        temp_dict['sum_sp'] = int(sum(policy.sp for policy in policy_type))
        temp_dict['newbiz'] = len(policy_type.filter(status='newbiz'))
        temp_dict['prolongation'] = len(policy_type.filter(status='prolongation'))
        temp_dict['transition'] = len(policy_type.filter(status='transition'))
        all_statistic[type] = temp_dict
        all_sp += sum(policy.sp for policy in policy_type)

    context = {
        'all_statistic': all_statistic,
        'user_statistic': user_statistic,
        'agent_statistic': agent_statistic,
        'all_sp': all_sp,
    }
    return render(request, 'main/statistic.html', context)


@login_required(login_url='login')
def a_reporting(request):
    # Просмотр и выгрузка сверок
    if request.method == 'POST':
        if 'policy_id_for_delete' in request.POST and request.user.admin:
            Policy.objects.get(id=request.POST.get('policy_id_for_delete')).delete()

        if 'id_policy_for_accept' in request.POST:
            policy_for_accept = Policy.objects.get(id=request.POST.get('id_policy_for_accept'))
            policy_for_accept.accept = True
            policy_for_accept.save()

        if 'id_policy_for_edit' in request.POST:
            policy_for_edit = Policy.objects.get(id=request.POST.get('id_policy_for_edit'))

            full_name = request.POST['full_name_client']
            if f'{policy_for_edit.client.last_name} {policy_for_edit.client.first_name} ' \
               f'{policy_for_edit.client.middle_name}' != full_name:

                client_for_edit = policy_for_edit.client

                while full_name[-1] == ' ':
                    full_name = full_name[:-1]
                last_name = full_name.split()[0].capitalize()
                first_name = full_name.split()[1].capitalize()
                middle_name = ''
                if len(full_name.split()) > 2:
                    for name in full_name.split()[2:]:
                        middle_name = middle_name + name.capitalize() + " "
                    middle_name = middle_name[:-1]

                client_for_edit.last_name = last_name
                client_for_edit.first_name = first_name
                client_for_edit.middle_name = middle_name
                client_for_edit.save()

            policy_for_edit.type = Type.objects.get(id=request.POST.get('type'))
            policy_for_edit.status = request.POST.get('Тип_продажи')
            policy_for_edit.number = request.POST.get('number')
            policy_for_edit.series = request.POST.get('series')
            policy_for_edit.company = Company.objects.get(id=request.POST.get('company'))
            policy_for_edit.channel = Channel.objects.get(id=request.POST.get('channel'))
            policy_for_edit.sp = float(request.POST.get('sp').replace(',', '.'))
            policy_for_edit.commission = float(request.POST.get('commission').replace(',', '.'))
            policy_for_edit.date_registration = request.POST.get('date_registration')
            policy_for_edit.date_start = request.POST.get('date_start')
            policy_for_edit.date_end = request.POST.get('date_end')
            policy_for_edit.user = User.objects.get(id=request.POST.get('user'))
            policy_for_edit.save()

    selected = {}
    policy_list = []
    if request.GET.get('date_start') == None and request.GET.get('date_end') == None:
        date_start, date_end = get_start_end_date()
        date_start = date_start.strftime("%Y-%m-%d")
        date_end = date_end.strftime("%Y-%m-%d")
    else:
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
    if request.user.admin:
        users = User.objects.filter(admin=False, agent=False)
        result = Policy.objects.filter(accept=False)
    else:
        users = User.objects.filter(id=request.user.id)
        result = Policy.objects.filter(user_id=request.user.id, accept=False)
    company = Company.objects.all()
    channel = Channel.objects.all()
    type = Type.objects.all()

    if 'search' in request.GET:
        # поиск по страхователю или по номеру полиса
        selected['search'] = request.GET.get('search')
        result = result.filter(
            Q(client__last_name__iregex=request.GET.get('search')) |
            Q(client__first_name__iregex=request.GET.get('search')) |
            Q(client__middle_name__iregex=request.GET.get('search')) |
            Q(number__iregex=request.GET.get('search')) |
            Q(series__iregex=request.GET.get('search'))
        )
    else:
        result = result.filter(
            date_registration__lt=date_end,
            date_registration__gte=date_start
        )
        if 'Менеджер' in request.GET:
            if request.GET.get('Менеджер') != 'all':
                selected['manager'] = int(request.GET.get('Менеджер'))
                result = result.filter(user=request.GET.get('Менеджер'))
            if request.GET.get('Канал продаж') != 'all':
                selected['channel'] = int(request.GET.get('Канал продаж'))
                result = result.filter(channel=request.GET.get('Канал продаж'))
            if request.GET.get('Страховая компания') != 'all':
                selected['company'] = int(request.GET.get('Страховая компания'))
                result = result.filter(company=request.GET.get('Страховая компания'))
            if request.GET.get('Тип полиса') != 'all':
                selected['type'] = int(request.GET.get('Тип полиса'))
                result = result.filter(type=request.GET.get('Тип полиса'))

    if len(result) > 0:
        for policy in result:
            commission_rur = '{:.2f}'.format(policy.commission / 100 * policy.sp)
            temp_dict = {
                'status': policy.status,
                'type': policy.type,
                'series': policy.series,
                'number': policy.number,
                'company': policy.company,
                'channel': policy.channel,
                'sp': policy.sp,
                'commission': policy.commission,
                'commission_rur': commission_rur,
                'client': policy.client,
                'user': policy.user,
                'date_registration': policy.date_registration,
                'date_registration_for_edit': policy.date_registration.strftime("%Y-%m-%d"),
                'date_start': policy.date_start,
                'date_start_for_edit': policy.date_start.strftime("%Y-%m-%d"),
                'date_end': policy.date_end,
                'date_end_for_edit': policy.date_end.strftime("%Y-%m-%d"),
                'id': policy.id,
            }
            policy_list.append(temp_dict)

    # ссылка с параметрами для пагинации
    link = '?'
    for key, value in request.GET.items():
        if key == 'page':
            continue
        link = link + f'{key}={value}&'

    paginator = Paginator(policy_list, 15)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)

    data = {
        'users': users,
        'companies': company,
        'channels': channel,
        'types': type,
        'policy_list': page.object_list,
        'date_start': date_start,
        'date_end': date_end,
        'selected': selected,
        'page': page,
        'link': link,
        'paginator': paginator,
    }

    return render(request, 'main/reporting.html', data)


@login_required(login_url='login')
def addpolicy(request):
    # Добавление нового полиса
    error = ''
    errors_upload = {}
    text = ''
    text_upload = ''
    type = Type.objects.all()
    banks = Bank.objects.all()
    company = Company.objects.all()
    channel = Channel.objects.all()

    if request.method == 'POST':

        if 'upload' in request.POST:
            # загрузка продаж из файла
            wb = load_workbook(filename=request.FILES['file'])
            sheet = wb.worksheets[0]
            count = 0
            for row in range(2, sheet.max_row+1):
                # пропускаем пустую строчку
                if sheet[row][0].value is None:
                    continue

                status = '-'

                if sheet[row][0].value.lower() == 'новый бизнес':
                    status = 'newbiz'
                elif sheet[row][0].value.lower() == 'пролонгация':
                    status = 'prolongation'
                elif sheet[row][0].value.lower() == 'переход':
                    status = 'transition'
                elif sheet[row][0].value.lower() == 'аддендум':
                    status = 'addendum'

                if isinstance(sheet[row][7].value, str):
                    date_registration = f'{sheet[row][7].value[6:10]}-' \
                                        f'{sheet[row][7].value[3:5]}-' \
                                        f'{sheet[row][7].value[0:2]}'
                else:
                    date_registration = f'{sheet[row][7].value.year}-' \
                                        f'{sheet[row][7].value.month}-' \
                                        f'{sheet[row][7].value.day}'

                if isinstance(sheet[row][8].value, str):
                    date_start = f'{sheet[row][8].value[6:10]}-' \
                                        f'{sheet[row][8].value[3:5]}-' \
                                        f'{sheet[row][8].value[0:2]}'
                else:
                    date_start = f'{sheet[row][8].value.year}-' \
                                        f'{sheet[row][8].value.month}-' \
                                        f'{sheet[row][8].value.day}'

                if isinstance(sheet[row][9].value, str):
                    date_end = f'{sheet[row][9].value[6:10]}-' \
                                        f'{sheet[row][9].value[3:5]}-' \
                                        f'{sheet[row][9].value[0:2]}'
                else:
                    date_end = f'{sheet[row][9].value.year}-' \
                                        f'{sheet[row][9].value.month}-' \
                                        f'{sheet[row][9].value.day}'

                type_for_created, created = Type.objects.get_or_create(name=sheet[row][1].value)
                company_for_created, created = Company.objects.get_or_create(name=sheet[row][3].value)
                channel_for_created, created = Channel.objects.get_or_create(name=sheet[row][4].value)

                user = User.objects.get(
                    last_name=sheet[row][11].value.split()[0],
                    first_name=sheet[row][11].value.split()[1],
                )

                middle_name = ''
                if len(sheet[row][10].value.split()) == 3:
                    middle_name = sheet[row][10].value.split(" ")[2]
                elif len(sheet[row][10].value.split()) > 3:
                    middle_name = f'{sheet[row][10].value.split()[2]} {sheet[row][10].value.split()[3]}'

                client, created = Client.objects.get_or_create(
                    last_name=sheet[row][10].value.split()[0],
                    first_name=sheet[row][10].value.split()[1],
                    middle_name=middle_name,
                )

                if len(str(sheet[row][2].value).split()) == 2:
                    series = sheet[row][2].value.split()[0]
                    number = sheet[row][2].value.split()[1]
                else:
                    series = ''
                    number = sheet[row][2].value

                policy, created = Policy.objects.get_or_create(
                    series=series,
                    number=number,
                    defaults={
                        'status': status,
                        'type': type_for_created,
                        'company': company_for_created,
                        'channel': channel_for_created,
                        'sp': float(str(sheet[row][5].value).replace(' ', '').replace(',', '.')),
                        'commission': float(str(sheet[row][6].value).replace(' ', '').replace(',', '.')),
                        'date_registration': date_registration,
                        'date_start': date_start,
                        'date_end': date_end,
                        'user': user,
                        'client': client,
                    }
                )

                if created:
                    count += 1
                else:
                    errors_upload[f'{series} {number}'] = 'Полис уже есть в базе'

            text_upload = f'Загруженно {count} из {count + len(errors_upload)}'

            if len(errors_upload) > 0:
                wb_errors = openpyxl.Workbook()
                sheet = wb_errors['Sheet']

                sheet['A1'] = 'Номер'
                sheet['B1'] = 'БСО'
                sheet['C1'] = 'Ошибка'

                wb_errors.save(f'main/file/wb_errors.xlsx')

                wb_errors = openpyxl.load_workbook(f'main/file/wb_errors.xlsx')
                sheet = wb_errors['Sheet']

                str_number = 2
                count_policy = 1
                for policy, error in errors_upload.items():
                    sheet[str_number][0].value = count_policy
                    sheet[str_number][1].value = policy
                    sheet[str_number][2].value = error

                    str_number += 1

                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="wb_errors.xlsx"'

                wb_errors.save(response)

                return response

        else:
            full_name = request.POST['full_name']
            while full_name[-1] == ' ':
                full_name = full_name[:-1]
            last_name = full_name.split()[0].capitalize()
            first_name = full_name.split()[1].capitalize()
            middle_name = ''
            if len(full_name.split()) > 2:
                for name in full_name.split()[2:]:
                    middle_name = middle_name + name.capitalize() + " "
                middle_name = middle_name[:-1]

            client, created = Client.objects.get_or_create(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                birthday=request.POST.get('birthday'),
                defaults={
                    'phone': request.POST.get('phone'),
                    'email': request.POST.get('email')
                }
            )

            if request.POST.get('Тип продажи') == 'payment':
                # очередной взнос
                policy = Policy(
                    number=request.POST.get('number'),
                    series=request.POST.get('series'),
                    company_id=request.POST.get('Страховая_компания'),
                    user_id=request.user.id,
                    client_id=client.id,
                    channel_id=request.POST.get('Канал_продаж'),
                    type_id=request.POST.get('Тип_полиса'),
                    date_registration=request.POST.get('date_registration'),
                    date_start=request.POST.get('date_start'),
                    date_end=request.POST.get('date_end'),
                    commission=float(request.POST.get('commission').replace(',', '.')),
                    sp=float(request.POST.get('sp').replace(',', '.')),
                    status=request.POST.get('Тип продажи'),
                )
                policy.save()

                text = 'Запись успешно добавлена'
                if Type.objects.get(id=request.POST.get('Тип_полиса')).name == 'Ипотечный':
                    policy.bank = request.POST.get('bank')
                    policy.save()
                if request.POST.get('Оплата') == 'cash':
                    policy.type_pay = True
                    policy.save()
                if request.POST.get('credit') == 'credit':
                    policy.credit = True
                    policy.save()

                commission_objects = Commission.objects.filter(
                    type=policy.type,
                    channel=policy.channel,
                    company=policy.company,
                    date_start__lte=policy.date_registration,
                )

                if len(commission_objects) > 0:
                    if Type.objects.get(id=request.POST.get('Тип_полиса')).name == 'Ипотечный':
                        commission_objects = commission_objects.filter(bank=Bank.objects.get(name=policy.bank))

                    if len(commission_objects) > 0:
                        policy.commission = commission_objects.order_by('-date_start')[0].value
                        policy.save()

            else:
                # добавление нового полиса
                policy, created = Policy.objects.get_or_create(
                    number=request.POST.get('number'),
                    series=request.POST.get('series'),
                    company_id=request.POST.get('Страховая_компания'),
                    defaults={
                        'user_id': request.user.id,
                        'client_id': client.id,
                        'channel_id': request.POST.get('Канал_продаж'),
                        'type_id': request.POST.get('Тип_полиса'),
                        'date_registration': request.POST.get('date_registration'),
                        'date_start': request.POST.get('date_start'),
                        'date_end': request.POST.get('date_end'),
                        'commission': float(request.POST.get('commission').replace(',', '.')),
                        'sp': float(request.POST.get('sp').replace(',', '.')),
                        'status': request.POST.get('Тип продажи'),
                        }
                    )

                if created == False:
                    error = f'Полис с номером {request.POST.get("series")} {request.POST.get("number")} уже есть в базе'
                else:
                    text = 'Запись успешно добавлена'
                    if Type.objects.get(id=request.POST.get('Тип_полиса')).name == 'Ипотечный':
                        policy.bank = request.POST.get('bank')
                        policy.save()
                    if request.POST.get('Оплата') == 'cash':
                        policy.type_pay = True
                        policy.save()
                    if request.POST.get('credit') == 'credit':
                        policy.credit = True
                        policy.save()

                    commission_objects = Commission.objects.filter(
                        type=policy.type,
                        channel=policy.channel,
                        company=policy.company,
                        date_start__lte=policy.date_registration,
                    )

                    if len(commission_objects) > 0:
                        if Type.objects.get(id=request.POST.get('Тип_полиса')).name == 'Ипотечный':
                            commission_objects = commission_objects.filter(bank=Bank.objects.get(name=policy.bank))

                        if len(commission_objects) > 0:
                            policy.commission = commission_objects.order_by('-date_start')[0].value
                            policy.save()

    data = {
        'types': type,
        'companys': company,
        'channels': channel,
        'banks': banks,
        'error': error,
        'text': text,
        'text_upload': text_upload,
    }

    return render(request, 'main/osago.html', data)


@login_required(login_url='login')
def upload_policy(request):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            text = 'Загружено'

            with open('main/file/date.csv', 'wb') as file:
                for row in request.FILES['file'].chunks():
                    file.write(row)

            with open('main/file/date.csv', 'r', encoding='cp1251', newline='') as file_1:
                reader = csv.DictReader(file_1, delimiter=';')
                for row in reader:
                    pass

    context = {}

    return render(request, 'main/upload_policy.html', context)


@login_required(login_url='login')
def register_user(request):
    # Регистрация нового пользователя
    if request.user.admin:
        error = ''
        if request.method == 'POST':
            if len(User.objects.filter(username=request.POST.get('username'))) > 0:
                error = 'Этот логин уже используется'
            else:
                user = User.objects.create_user(
                    username=request.POST.get('username'),
                    password=request.POST.get('password'),
                    last_name=request.POST.get('last_name'),
                    first_name=request.POST.get('first_name'),
                    middle_name='',
                    agent=False,
                )
                if request.POST.get('middle_name'):
                    user.middle_name = request.POST.get('middle_name')
                    user.save()

        return render(request, 'registration/registration.html', context={'error': error})

    else:
        return render(request, 'registration/registration.html',
                      context={'error': 'Для регистрации обратитесь к администратору!'})


@login_required(login_url='login')
def policy_edit(request):
    text = ''
    if request.user.admin:
        policy = Policy.objects.get(id=request.GET.get('id'))
        channel = Channel.objects.all()
        company = Company.objects.all()
        date_start = policy.date_start.strftime("%Y-%m-%d")
        date_end = policy.date_end.strftime("%Y-%m-%d")
        sp = str(policy.sp).replace(',', '.')

        if request.method == 'POST':
            policy = Policy.objects.get(id=request.POST.get('id'))
            policy.number = request.POST.get('number')
            policy.series = request.POST.get('series')
            policy.company = Company.objects.get(id=request.POST.get('company'))
            policy.channel = Channel.objects.get(id=request.POST.get('channel'))
            policy.sp = float(request.POST.get('sp').replace(',', '.'))
            policy.date_start = request.POST.get('date_start')
            policy.date_end = request.POST.get('date_end')
            policy.save()

            sp = request.POST.get('sp')
            text = 'Сохранено'

        context = {
            'policy': policy,
            'text': text,
            'channel': channel,
            'company': company,
            'date_start': date_start,
            'date_end': date_end,
            'sp': sp,
        }

        return render(request, 'main/policy_edit_div.html', context)


@login_required(login_url='login')
def unload_mortgage(request):
    # Выгрузка статистики в файл xlsx
    if request.user.admin:
        date_end = datetime.datetime.strptime(f'{request.GET.get("year")}-{request.GET.get("month")}-01', '%Y-%m-%d')
        result = MortgagePolicy.objects.filter(date_end=date_end, date_at__gte=request.GET.get('date_at'))
        if request.GET.get('bank') != 'all':
            result = result.filter(bank_id=request.GET.get('bank'))

        wb = openpyxl.Workbook()
        sheet = wb['Sheet']

        sheet['A1'] = 'Банк'
        sheet['B1'] = 'Тип полиса'
        sheet['C1'] = 'Дата окончания'
        sheet['D1'] = 'Клиент'
        sheet['E1'] = 'Дата рождения'
        sheet['F1'] = 'Телефон'
        sheet['G1'] = 'Почта'

        wb.save('main/file/mortgage.xlsx')

        wb = openpyxl.load_workbook('main/file/mortgage.xlsx')
        sheet = wb['Sheet']

        str_number = 2
        for policy in result:
            sheet[str_number][0].value = policy.bank.name
            if policy.type_mortgage == 'all':
                sheet[str_number][1].value = 'Все риски'
            elif policy.type_mortgage == 'property':
                sheet[str_number][1].value = 'Имущество'
            elif policy.type_mortgage == 'life':
                sheet[str_number][1].value = 'Жизнь'
            sheet[str_number][2].value = policy.date_end
            sheet[str_number][3].value = f'{policy.client.last_name} ' \
                                         f'{policy.client.first_name} ' \
                                         f'{policy.client.middle_name}'
            sheet[str_number][4].value = policy.client.birthday
            sheet[str_number][5].value = policy.client.phone
            sheet[str_number][6].value = policy.client.email

            str_number += 1

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="mortgage.xlsx"'

        wb.save(response)

        return response


@login_required(login_url='login')
def upload_mortgage(request):
    # Загрузка заявок ипотечных заявок
    text = ''
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            text = 'Загружено'
            with open('main/file/mortgage.csv', 'wb') as file:
                for row in request.FILES['file'].chunks():
                    file.write(row)

            with open('main/file/mortgage.csv', 'r', encoding='cp1251', newline='') as file_1:
                reader = csv.DictReader(file_1, delimiter=';')
                for row in reader:
                    if len(row['Дата рождения']) > 0:
                        birthday = datetime.datetime.strptime(row['Дата рождения'], "%d.%m.%Y")
                    client, created = Client.objects.get_or_create(
                        first_name=row['Имя'],
                        middle_name=row['Отчество'],
                        last_name=row['Фамилия'],
                        birthday=birthday,
                        defaults={
                            'phone': row['Телефон'],
                            'email': row['Почта'],
                        }
                    )

                    bank, created = Bank.objects.get_or_create(name=row['Банк'])

                    MortgagePolicy.objects.get_or_create(
                        date_end=datetime.datetime.strptime(row['Дата окончания'], "%d.%m.%Y"),
                        bank=bank,
                        client=client,
                        defaults={
                            'user': request.user,
                        }
                    )

    context = {
        'form': form,
        'text': text,
    }

    return render(request, 'main/upload_mortgage.html', context)


@login_required(login_url='login')
def mortgage(request):
    text = ''
    users_statistic = {}
    if request.method == 'POST':
        client, created = Client.objects.get_or_create(
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            last_name=request.POST.get('last_name'),
            birthday=request.POST.get('birthday'),
            defaults={
                'phone': request.POST.get('phone'),
                'email': request.POST.get('email')
            }
        )

        date_end = datetime.datetime.strptime(f'{request.POST.get("year")}-{request.POST.get("month")}-01', '%Y-%m-%d')
        MortgagePolicy(bank_id=request.POST.get('bank'),
                       type_mortgage=request.POST['type_policy_mortgage'],
                       user_id=request.user.id,
                       client_id=client.id,
                       date_end=date_end).save()
        text = 'Полис добавлен'
    if request.user.admin:
        mortgage_policy = MortgagePolicy.objects.all()
        date_target = datetime.datetime.today().date()
        for i in range(1, 7):
            policyes = MortgagePolicy.objects.filter(date_at=date_target)
            if len(policyes) > 0:
                users_set = {policy.user for policy in policyes}
                temp_dict = {user: len(MortgagePolicy.objects.filter(user=user)) for user in users_set}
                users_statistic[date_target] = temp_dict
            date_target = date_target - datetime.timedelta(days=-1)
    else:
        mortgage_policy = MortgagePolicy.objects.filter(user_id=request.user.id)

    statistic_2022 = {}
    statistic_2022['all_count'] = len(mortgage_policy.filter(
        date_end__gte=datetime.datetime.strptime('2022-01-01', '%Y-%m-%d'),
        date_end__lt=datetime.datetime.strptime('2023-01-01', '%Y-%m-%d')))
    for i in range(1, 13):
        if i < 9:
            statistic_2022['0' + str(i)] = len(mortgage_policy.filter(
        date_end__gte=datetime.datetime.strptime(f'2022-{"0" + str(i)}-01', '%Y-%m-%d'),
        date_end__lt=datetime.datetime.strptime(f'2022-{"0" + str(i + 1)}-01', '%Y-%m-%d')))
        elif i == 9:
            statistic_2022['0' + str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2022-{"0" + str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2022-{str(i + 1)}-01', '%Y-%m-%d')))
        elif i == 10:
            statistic_2022[str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2022-{str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2022-{str(i + 1)}-01', '%Y-%m-%d')))
        elif i < 12:
            statistic_2022[str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2022-{str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2022-{str(i + 1)}-01', '%Y-%m-%d')))
        else:
            statistic_2022[str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2022-{str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2023-{"0" + str(i - 11)}-01', '%Y-%m-%d')))

    statistic_2023 = {}
    statistic_2023['all_count'] = len(mortgage_policy.filter(
        date_end__gte=datetime.datetime.strptime('2023-01-01', '%Y-%m-%d'),
        date_end__lt=datetime.datetime.strptime('2024-01-01', '%Y-%m-%d')))
    for i in range(1, 13):
        if i < 9:
            statistic_2023['0' + str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2023-{"0" + str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2023-{"0" + str(i + 1)}-01', '%Y-%m-%d')))
        elif i == 9:
            statistic_2023['0' + str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2023-{"0" + str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2023-{str(i + 1)}-01', '%Y-%m-%d')))
        elif i == 10:
            statistic_2023[str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2023-{str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2023-{str(i + 1)}-01', '%Y-%m-%d')))
        elif i < 12:
            statistic_2023[str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2023-{str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2023-{str(i + 1)}-01', '%Y-%m-%d')))
        else:
            statistic_2023[str(i)] = len(mortgage_policy.filter(
                date_end__gte=datetime.datetime.strptime(f'2023-{str(i)}-01', '%Y-%m-%d'),
                date_end__lt=datetime.datetime.strptime(f'2024-{"0" + str(i - 11)}-01', '%Y-%m-%d')))

    banks = Bank.objects.all()
    date_at = datetime.datetime.today().strftime("%Y-%m-%d")

    context = {
        'banks': banks,
        'date_at': date_at,
        'mortgage_policy': mortgage_policy,
        'statistic_2023': statistic_2023,
        'statistic_2022': statistic_2022,
        'text': text,
        'users_statistic': users_statistic,
    }

    return render(request, 'main/Mortgage.html', context)


@login_required(login_url='login')
def search_policy(request):
    selected = {}
    result = ''
    text = ''
    if request.method == 'POST':
        if request.POST.get('value') != '':
            if request.POST.get('target') == 'series':
                result = Policy.objects.filter(series__icontains=request.POST.get('value'))
            elif request.POST.get('target') == 'number':
                result = Policy.objects.filter(number__icontains=request.POST.get('value'))
            elif request.POST.get('target') == 'last_name':
                result = Policy.objects.filter(client__last_name__icontains=request.POST.get('value'))
            elif request.POST.get('target') == 'first_name':
                result = Policy.objects.filter(client__first_name__icontains=request.POST.get('value'))
            elif request.POST.get('target') == 'middle_name':
                result = Policy.objects.filter(client__middle_name__icontains=request.POST.get('value'))

            if request.user.admin == False:
                result = result.filter(user_id=request.user.id)

            selected['target'] = request.POST.get('target')
            selected['value'] = request.POST.get('value')

    context = {
        'result': result,
        'text': text,
        'selected': selected,
    }

    return render(request, 'main/search_policy.html', context)


@login_required(login_url='login')
def commission(request):
    if request.method == 'POST':
        if Type.objects.get(id=request.POST.get('type')).name == 'Ипотечный':
            commission, created = Commission.objects.get_or_create(
                channel_id=request.POST.get('id'),
                company_id=request.POST.get('company'),
                type_id=request.POST.get('type'),
                bank_id=request.POST.get('bank'),
                date_start=request.POST.get('date_start'),
                defaults={
                    'value': float(request.POST.get('value').replace(',', '.')),
                }
            )
        else:
            commission, created = Commission.objects.get_or_create(
                channel_id=request.POST.get('id'),
                company_id=request.POST.get('company'),
                type_id=request.POST.get('type'),
                date_start=request.POST.get('date_start'),
                defaults={
                    'value': float(request.POST.get('value').replace(',', '.')),
                }
            )

        if created == False:
            commission.value = float(request.POST.get('value').replace(',', '.'))
            commission.save()

        policyes = Policy.objects.filter(date_registration__gte=commission.date_start,
                                         channel=commission.channel,
                                         company=commission.company,
                                         type=commission.type,
                                         accept=False)

        if len(policyes) > 0:
            if commission.type.name == 'Ипотечный':
                policyes = policyes.filter(bank=commission.bank)

                if len(policyes) > 0:
                    for policy in policyes:
                        policy.commission = (Commission.objects.filter(
                            type=commission.type,
                            channel=commission.channel,
                            company=commission.company,
                            date_start__lte=policy.date_registration,
                            bank=commission.bank)).order_by('-date_start')[0].value
                        policy.save()
            else:
                for policy in policyes:
                    policy.commission = (Commission.objects.filter(
                        type=commission.type,
                        date_start__lte=policy.date_registration,
                        channel=commission.channel,
                        company=commission.company,
                    )).order_by('-date_start')[0].value
                    policy.save()

    channel = Channel.objects.all()
    commission = Commission.objects.all()
    company = Company.objects.all()
    bank = Bank.objects.all()
    type = Type.objects.all()
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")

    context = {
        'channel': channel,
        'company': company,
        'date_now': date_now,
        'commission': commission,
        'bank': bank,
        'type': type,
    }
    return render(request, 'main/commission.html', context)


@login_required(login_url='login')
def commission_delete(request):
    if request.user.admin:
        if request.method == 'POST':
            Commission.objects.get(id=request.POST.get('id')).delete()
            return HttpResponseRedirect('/commission')


@login_required(login_url='login')
def accept(request):
    # Просмотр и выгрузка проведенных полисов
    if request.method == 'POST' and request.user.admin and 'policy_id_for_return' in request.POST:
        policy_for_return = Policy.objects.get(id=request.POST.get('policy_id_for_return'))
        policy_for_return.accept = False
        policy_for_return.save()

    selected = {}
    policy_list = []
    if request.GET.get('date_start') == None and request.GET.get('date_end') == None:
        date_start, date_end = get_start_end_date()
        date_start = date_start.strftime("%Y-%m-%d")
        date_end = date_end.strftime("%Y-%m-%d")
    else:
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
    if request.user.admin:
        users = User.objects.all()
        result = Policy.objects.filter(accept=True)
    else:
        users = User.objects.filter(id=request.user.id)
        result = Policy.objects.filter(user_id=request.user.id, accept=True)
    company = Company.objects.all()
    channel = Channel.objects.all()
    type = Type.objects.all()

    if 'search' in request.GET:
        # поиск по страхователю или по номеру полиса
        selected['search'] = request.GET.get('search')
        result = result.filter(
            Q(client__last_name__iregex=request.GET.get('search')) |
            Q(client__first_name__iregex=request.GET.get('search')) |
            Q(client__middle_name__iregex=request.GET.get('search')) |
            Q(number__iregex=request.GET.get('search')) |
            Q(series__iregex=request.GET.get('search'))
        )
    else:
        result = result.filter(
            date_registration__lt=date_end,
            date_registration__gte=date_start
        )
        if 'Менеджер' in request.GET:
            if request.GET.get('Менеджер') != 'all':
                selected['manager'] = int(request.GET.get('Менеджер'))
                result = result.filter(user=request.GET.get('Менеджер'))
            if request.GET.get('Канал продаж') != 'all':
                selected['channel'] = int(request.GET.get('Канал продаж'))
                result = result.filter(channel=request.GET.get('Канал продаж'))
            if request.GET.get('Страховая компания') != 'all':
                selected['company'] = int(request.GET.get('Страховая компания'))
                result = result.filter(company=request.GET.get('Страховая компания'))
            if request.GET.get('Тип полиса') != 'all':
                selected['type'] = int(request.GET.get('Тип полиса'))
                result = result.filter(type=request.GET.get('Тип полиса'))

    if len(result) > 0:
        for policy in result:
            commission_rur = '{:.2f}'.format(policy.commission / 100 * policy.sp)
            temp_dict = {
                'status': policy.status,
                'type': policy.type,
                'series': policy.series,
                'number': policy.number,
                'company': policy.company,
                'channel': policy.channel,
                'sp': policy.sp,
                'commission': policy.commission,
                'commission_rur': commission_rur,
                'client': policy.client,
                'user': policy.user,
                'date_registration': policy.date_registration,
                'date_registration_for_edit': policy.date_registration.strftime("%Y-%m-%d"),
                'date_start': policy.date_start,
                'date_start_for_edit': policy.date_start.strftime("%Y-%m-%d"),
                'date_end': policy.date_end,
                'date_end_for_edit': policy.date_end.strftime("%Y-%m-%d"),
                'id': policy.id,
            }
            policy_list.append(temp_dict)

    # ссылка с параметрами для пагинации
    link = '?'
    for key, value in request.GET.items():
        if key == 'page':
            continue
        link = link + f'{key}={value}&'

    paginator = Paginator(policy_list, 15)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)

    data = {
        'users': users,
        'companies': company,
        'channels': channel,
        'types': type,
        'policy_list': page.object_list,
        'paginator': paginator,
        'page': page,
        'date_start': date_start,
        'date_end': date_end,
        'selected': selected,
        'link': link,
    }
    return render(request, 'main/accept.html', data)


@login_required(login_url='login')
def add_type_channel_company(request):
    # Добавление страховой компании, канала продаж и типа полиса
    text_company = ''
    text_channel = ''
    text_bank = ''
    text_type = ''

    if request.method == 'POST':
        if 'new_channel' in request.POST:
            new_channel, created = Channel.objects.get_or_create(name=request.POST['new_channel'])

            if created:
                text_channel = 'Новый канал продаж добавлен'
            else:
                text_channel = 'Такой канал продаж уже существует'

        if 'new_type' in request.POST:
            new_type, created = Type.objects.get_or_create(name=request.POST['new_type'])

            if created:
                text_type = 'Новый тип полиса добавлен'
            else:
                text_type = 'Такой тип полиса уже существует'

        if 'new_company' in request.POST:
            new_company, created = Company.objects.get_or_create(name=request.POST['new_company'])

            if created:
                text_company = 'Новая страховая компания добавлена'
            else:
                text_company = 'Такая страховая компания уже существует'

        if 'new_bank' in request.POST:
            new_bank, created = Bank.objects.get_or_create(name=request.POST['new_bank'])

            if created:
                text_bank = 'Новый банк добавлен'
            else:
                text_bank = 'Такой банк уже существует'

    channel = Channel.objects.all()
    type = Type.objects.all()
    company = Company.objects.all()
    bank = Bank.objects.all()

    context = {
        'text_company': text_company,
        'text_channel': text_channel,
        'text_bank': text_bank,
        'text_type': text_type,
        'channel': channel,
        'type': type,
        'bank': bank,
        'company': company,
    }

    return render(request, 'main/add_type_channel_company.html', context)

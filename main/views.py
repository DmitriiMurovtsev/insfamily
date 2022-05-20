import datetime
import csv
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Policy, Client, Channel, Company, User, Type, Bso, MortgagePolicy, Bank, Commission
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
    else:
        result = Policy.objects.filter(
            user=request.user.id,
            date_registration__lt=request.GET.get('date_end'),
            date_registration__gte=request.GET.get('date_start')
        )
        if request.GET.get('Канал продаж') != 'all':
            result = result.filter(channel=request.GET.get('Канал продаж'))
        if request.GET.get('Страховая компания') != 'all':
            result = result.filter(company=request.GET.get('Страховая компания'))
        if request.GET.get('Тип полиса') != 'all':
            result = result.filter(type=request.GET.get('Тип полиса'))

    result_list = [
        [
            policy.type.name,
            policy.bank,
            policy.series,
            policy.number,
            policy.company.name,
            policy.sp,
            policy.commission,
            policy.channel,
            policy.date_registration,
            policy.date_start,
            policy.date_end,
            f'{policy.client.last_name} {policy.client.first_name} {policy.client.middle_name}',
            f'{policy.user.last_name} {policy.user.first_name}',
        ]
        for policy in result
    ]

    with open('./report/reporting.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                'Тип полиса',
                'Банк',
                'Серия',
                'Номер',
                'Страховая компания',
                'Премия',
                'КВ',
                'Канал продаж',
                'Дата оформления',
                'Дата начала действия',
                'Дата окончания действия',
                'Клиент',
                'Менеджер',
            )
        )
        writer.writerows(result_list)

    with open('./report/reporting.csv', 'r', encoding='cp1251', newline='') as file:
        file_data = file.read()
        f = file_data.encode(encoding='cp1251')

    response = HttpResponse(f, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporting.csv"'
    return response


@login_required(login_url='login')
def unload_accept(request):
    # Выгрузка сверок в файл
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
    else:
        result = Policy.objects.filter(
            user=request.user.id,
            date_registration__lt=request.GET.get('date_end'),
            date_registration__gte=request.GET.get('date_start')
        )
        if request.GET.get('Канал продаж') != 'all':
            result = result.filter(channel=request.GET.get('Канал продаж'))
        if request.GET.get('Страховая компания') != 'all':
            result = result.filter(company=request.GET.get('Страховая компания'))
        if request.GET.get('Тип полиса') != 'all':
            result = result.filter(type=request.GET.get('Тип полиса'))

    result_list = [
        [
            policy.type.name,
            policy.bank,
            policy.series,
            policy.number,
            policy.company.name,
            policy.sp,
            policy.commission,
            policy.channel,
            policy.date_registration,
            policy.date_start,
            policy.date_end,
            f'{policy.client.last_name} {policy.client.first_name} {policy.client.middle_name}',
            f'{policy.user.last_name} {policy.user.first_name}',
        ]
        for policy in result
    ]

    with open('./report/reporting.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                'Тип полиса',
                'Банк',
                'Серия',
                'Номер',
                'Страховая компания',
                'Премия',
                'КВ',
                'Канал продаж',
                'Дата оформления',
                'Дата начала действия',
                'Дата окончания действия',
                'Клиент',
                'Менеджер',
            )
        )
        writer.writerows(result_list)

    with open('./report/reporting.csv', 'r', encoding='cp1251', newline='') as file:
        file_data = file.read()
        f = file_data.encode(encoding='cp1251')

    response = HttpResponse(f, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporting.csv"'
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
            policy_user = Policy.objects.filter(user=user.id)
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
        if 'id_policy_for_accept' in request.POST:
            policy_for_accept = Policy.objects.get(id=request.POST.get('id_policy_for_accept'))
            policy_for_accept.accept = True
            policy_for_accept.save()
        else:
            policy_for_edit = Policy.objects.get(id=request.POST.get('id_policy_for_edit'))
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
    text = ''
    type = Type.objects.all()
    banks = Bank.objects.all()
    company = Company.objects.all()
    channel = Channel.objects.all()
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
                'commission': request.POST.get('commission'),
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
                date_start__lte=policy.date_registration,
            )

            if len(commission_objects) > 0:
                if Type.objects.get(id=request.POST.get('Тип_полиса')).name == 'Ипотечный':
                    commission_objects = commission_objects.objects.filter(bank=Bank.objects.get(name=policy.bank))

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
                if request.POST.get('agent') == '1':
                    user.agent = True
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
            policy.sp = request.POST.get('sp')
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
    # Выгрузка статистики в файл csv
    if request.user.admin:
        date_end = datetime.datetime.strptime(f'{request.GET.get("year")}-{request.GET.get("month")}-01', '%Y-%m-%d')
        result = MortgagePolicy.objects.filter(date_end=date_end, date_at__gte=request.GET.get('date_at'))
        if request.GET.get('bank') != 'all':
            result = result.filter(bank_id=request.GET.get('bank'))

    result_list = [[policy.bank, policy.date_end, policy.client, policy.client.birthday, policy.client.phone,
                    policy.client.email] for policy in result]

    with open('./report/reporting_mortgage.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                'Банк',
                'Дата окончания',
                'Клиент',
                'Дата рождения',
                'Телефон',
                'Почта',
            )
        )
        writer.writerows(result_list)

    with open('./report/reporting_mortgage.csv', 'r', encoding='cp1251', newline='') as file:
        file_data = file.read()
        f = file_data.encode(encoding='cp1251')

    response = HttpResponse(f, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporting.csv"'
    return response


@login_required(login_url='login')
def upload_mortgage(request):
    # Загрузка заявок ипотечных заявок
    text = ',e'
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
                       user_id=request.user.id,
                       client_id=client.id,
                       date_end=date_end).save()
        text = 'Полис добавлен'
    if request.user.admin:
        mortgage_policy = MortgagePolicy.objects.all()
        users = User.objects.filter(admin=False, agent=False)
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
    context = {
        'banks': banks,
        'mortgage_policy': mortgage_policy,
        'statistic_2023': statistic_2023,
        'statistic_2022': statistic_2022,
        'text': text,
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
                            date_start__lte=policy.date_registration,
                            bank=commission.bank)).order_by('-date_start')[0].value
                        policy.save()
            else:
                for policy in policyes:
                    policy.commission = (Commission.objects.filter(
                        type=commission.type,
                        date_start__lte=policy.date_registration,
                        channel=commission.channel)).order_by('-date_start')[0].value
                    policy.save()

    channel = Channel.objects.all()
    commission = Commission.objects.all()
    bank = Bank.objects.all()
    type = Type.objects.all()

    context = {
        'channel': channel,
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
    selected = {}
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

    # ссылка с параметрами для пагинации
    link = '?'
    for key, value in request.GET.items():
        if key == 'page':
            continue
        link = link + f'{key}={value}&'

    paginator = Paginator(result, 3)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)

    data = {
        'users': users,
        'companies': company,
        'channels': channel,
        'types': type,
        'result': page.object_list,
        'paginator': paginator,
        'page': page,
        'date_start': date_start,
        'date_end': date_end,
        'selected': selected,
        'link': link,
    }
    return render(request, 'main/accept.html', data)


@login_required(login_url='login')
def motivation(request):
    # Программа мотивации сотрудников
    context = {
        'text': 'В разработке'
    }
    return render(request, 'main/motivation.html', context)


@login_required(login_url='login')
def bonuses(request):
    # Программа мотивации сотрудников
    context = {
        'text': 'В разработке'
    }
    return render(request, 'main/motivation.html', context)


# Агенты


@login_required(login_url='login')
def bso_stock(request):
    # БСО в наличии у агента
    text = 'В разработке'
    context = {'text': text}
    return render(request, 'main/bso_stock.html', context)


@login_required(login_url='login')
def bso_delete(request):
    if request.user.admin:
        if request.method == 'POST':
            Bso.objects.get(id=request.POST.get('id')).delete()
            return HttpResponseRedirect('/bso_agent')


@login_required(login_url='login')
def bso_agent(request):
    # Статистика по агентам по выданным БСО
    selected = {}
    if request.user.admin:
        agents = User.objects.filter(agent=True)
        company = Company.objects.all()
        bso = Bso.objects.all()

        if request.method == 'POST':
            bso_up = Bso.objects.get(id=request.POST.get('id'))
            bso_up.status = request.POST.get('status_up')
            bso_up.save()

        if request.method == 'GET':
            if request.GET.get('agent'):
                if request.GET.get('agent') != 'all':
                    selected['agent'] = int(request.GET.get('agent'))
                if request.GET.get('company') != 'all':
                    selected['company'] = int(request.GET.get('company'))
                selected['status'] = request.GET.get('status')
                bso = Bso.objects.all()
                if request.GET.get('agent') != 'all':
                    bso = bso.filter(user_id=request.GET.get('agent'))
                if request.GET.get('company') != 'all':
                    bso = bso.filter(company_id=request.GET.get('company'))
                if request.GET.get('status') != 'all':
                    bso = bso.filter(status=request.GET.get('status'))

        context = {
            'agents': agents,
            'company': company,
            'bso': bso,
            'selected': selected,
        }
        return render(request, 'main/bso_agent.html', context)


@login_required(login_url='login')
def bso_add(request):
    # Выдача БСО агентам
    text = ''
    if request.user.admin:
        agents = User.objects.filter(agent=True)
        company = Company.objects.all()
        bso = Bso.objects.all()
        if request.method == 'POST':
            bso_new = Bso.objects.filter(series=request.POST.get('series'), number=request.POST.get('number'))
            if len(bso_new) > 0:
                text = f'БСО {request.POST.get("series")} {request.POST.get("number")} уже есть в системе'
                context = {
                    'agents': agents,
                    'company': company,
                    'text': text,
                }
            else:
                Bso(user_id=request.POST.get('agent'),
                    series=request.POST.get('series'),
                    number=request.POST.get('number'),
                    company_id=request.POST.get('company'),
                    ).save()
                text = f'сохранено'
        context = {
            'agents': agents,
            'company': company,
            'text': text,
            'bso': bso
        }
        return render(request, 'main/bso_agent.html', context)


@login_required(login_url='login')
def debitor(request):
    text = 'В разработке'

    context = {
        'text': text,
    }

    return render(request, 'main/debitor.html', context)

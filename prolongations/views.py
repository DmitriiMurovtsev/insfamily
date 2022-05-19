import datetime
import locale

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
import csv

from .forms import UploadFileForm

from .models import Status, PolicyBase, NameBase
from main.models import Client, Type, Company


# Установка родной локации для вывода кириллицей
locale.setlocale(locale.LC_ALL, "ru_RU")


@login_required(login_url='login')
def upload_policy(request):
    # Изменение статуса полиса
    if request.user.agent == False and request.user.admin == True or request.user.username == 'OSamohvalova':
        if request.method == 'POST':
            policy_up = PolicyBase.objects.get(id=request.POST.get('policy'))
            policy_up.status = Status.objects.get(id=request.POST.get('status'))
            policy_up.save()

        return HttpResponseRedirect('/prolongations/status_change')


@login_required(login_url='login')
def status_change(request):
    # Статистика по пролонгации
    if request.user.agent == False and request.user.admin == True or request.user.username == 'APuchkova':
        text = ''
        form = UploadFileForm()
        status = Status.objects.all()
        policy_base = PolicyBase.objects.filter(status__name='В работе').order_by('date_end')

        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                text = 'Загружено'
                with open('prolongations/file/date.csv', 'wb') as file:
                    for row in request.FILES['file'].chunks():
                        file.write(row)

                with open('prolongations/file/date.csv', 'r', encoding='cp1251', newline='') as file_1:
                    reader = csv.DictReader(file_1, delimiter=';')
                    for row in reader:
                        client, created = Client.objects.get_or_create(
                            first_name=row['Имя'],
                            middle_name=row['Отчество'],
                            last_name=row['Фамилия'],
                            birthday=datetime.datetime.strptime(row['Дата рождения'], "%d.%m.%Y"),
                            defaults={
                                'phone': row['Телефон'],
                                'email': row['Почта'],
                            }
                        )

                        name, created = NameBase.objects.get_or_create(
                            name=row['Название базы']
                        )

                        company, created = Company.objects.get_or_create(
                            name=row['Компания']
                        )

                        type, created = Type.objects.get_or_create(
                            name=row['Тип полиса']
                        )

                        PolicyBase.objects.get_or_create(
                            bso=row['БСО'],
                            defaults={
                                'type': type,
                                'company': company,
                                'status_id': Status.objects.get(name='В работе').id,
                                'client': client,
                                'sp': row['СП'].replace(',', '.'),
                                'channel': row['Канал продаж'],
                                'date_end': datetime.datetime.strptime(row['Дата окончания'], "%d.%m.%Y"),
                                'manager': row['Менеджер прошлого года'],
                                'object': row['Объект страхования'],
                                'name': name,
                            }
                        )

        paginator = Paginator(policy_base, 20)
        current_page = request.GET.get('page', 1)
        page = paginator.get_page(current_page)

        context = {
            'text': text,
            'form': form,
            'page': page,
            'policy_base': page.object_list,
            'paginator': paginator,
            'status': status,
        }

        return render(request, 'prolongations/status_change.html', context)


@login_required(login_url='login')
def get_statistic(request):
    # Статистика по пролонгации
    if request.user.agent == False and request.user.admin == True or request.user.username == 'APuchkova':
        status_statistic = {}
        month_statistic = {}
        status_all = Status.objects.all()
        types = Type.objects.all()
        policy_d = PolicyBase.objects.exclude(status__name='Оформлен')
        policy_d = policy_d.exclude(status__name='В работе')
        months = {
            datetime.datetime.strptime(policy.date_end[0:10], "%Y-%m-%d").month: datetime.datetime.strptime(
                policy.date_end[0:10], "%Y-%m-%d").strftime("%B")
            for policy in PolicyBase.objects.all()
        }
        for month_number, month in months.items():
            date_start = datetime.date(datetime.datetime.today().year, month_number, 1)
            if month_number != 12:
                date_end = datetime.date(datetime.datetime.today().year, month_number+1, 1) - datetime.timedelta(days=1)
            else:
                date_end = datetime.date(datetime.datetime.today().year, month_number, 31)
            type_statistic = {}
            for type in types:
                policy_type = PolicyBase.objects.filter(type=type, date_end__range=(date_start, date_end))
                if len(policy_type) > 0:
                    temp_dict = {}
                    count = len(policy_type)
                    count_r = len(policy_type.filter(status__name='В работе'))
                    count_p = len(policy_type.filter(status__name='Оформлен'))
                    count_d = count - count_p - count_r
                    temp_dict['count'] = count
                    temp_dict['count_r'] = count_r
                    temp_dict['percent_count_r'] = f'{format(float((count_r / count) * 100), ".1f")}%'
                    temp_dict['count_p'] = count_p
                    temp_dict['percent_count_p'] = f'{format(float((count_p / count) * 100), ".1f")}%'
                    temp_dict['count_d'] = count_d
                    temp_dict['percent_count_d'] = f'{format(float((count_d / count) * 100), ".1f")}%'
                    type_statistic[type] = temp_dict
            month_statistic[month] = type_statistic

        for status in status_all:
            if status.name == 'Оформлен' or status.name == 'В работе':
                continue
            policy_status = PolicyBase.objects.filter(status=status)
            if len(policy_status) > 0:
                count = len(policy_status)
                status_statistic[status] = count

        paginator = Paginator(policy_d, 10)
        current_page = request.GET.get('page', 1)
        page = paginator.get_page(current_page)

        context = {
            'month_statistic': month_statistic,
            'status_statistic': status_statistic,
            'page': page,
            'policy_base': page.object_list,
            'paginator': paginator,
        }

    return render(request, 'prolongations/statistic.html', context)

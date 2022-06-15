import datetime
import locale
import csv

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from openpyxl import load_workbook

from .forms import UploadFileForm

from .models import Status, PolicyBase, NameBase
from main.models import Client, Type, Company


# Установка родной локации для вывода кириллицей
locale.setlocale(locale.LC_ALL, "")


@login_required(login_url='login')
def upload_policy(request):
    # Изменение статуса полиса
    if request.user.agent == False and request.user.admin == True or request.user.username == 'APuchkova':
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

        if 'search' in request.GET:
            policy_base = policy_base.filter(
                Q(client__first_name__iregex=request.GET.get('search')) |
                Q(client__middle_name__iregex=request.GET.get('search')) |
                Q(client__last_name__iregex=request.GET.get('search'))
            )

        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                wb = load_workbook(filename=request.FILES['file'])
                sheet = wb.worksheets[0]

                for row in range(2, sheet.max_row + 1):
                    # пропускаем пустую строчку
                    if sheet[row][0].value is None:
                        continue

                    type_policy, created = Type.objects.get_or_create(name=sheet[row][10].value)
                    name_base, created = NameBase.objects.get_or_create(name=sheet[row][11].value)
                    company_policy, created = Company.objects.get_or_create(name=sheet[row][4].value)

                    if len(sheet[row][0].value.split()) > 3:
                        middle_name = f'{sheet[row][0].value.split()[2]} {sheet[row][0].value.split()[3]}'
                    elif len(sheet[row][0].value.split()) == 3:
                        middle_name = sheet[row][0].value.split()[2]
                    else:
                        middle_name = ''

                    client_policy, created = Client.objects.get_or_create(
                        first_name=sheet[row][0].value.split()[1],
                        last_name=sheet[row][0].value.split()[0],
                        middle_name=middle_name,
                        phone=sheet[row][1].value,
                        defaults={
                            'email': sheet[row][2].value,
                        }
                    )

                    status_policy = Status.objects.get(name='В работе')
                    bso_policy = sheet[row][5].value
                    sp_policy = float(str(sheet[row][8].value).replace(',', '.'))
                    channel_policy = sheet[row][3].value
                    object_policy = sheet[row][7].value
                    manager_policy = sheet[row][9].value
                    date_end = sheet[row][6].value

                    PolicyBase.objects.get_or_create(
                        bso=bso_policy,
                        company=company_policy,
                        defaults={
                            'type': type_policy,
                            'name': name_base,
                            'client': client_policy,
                            'status': status_policy,
                            'sp': sp_policy,
                            'channel': channel_policy,
                            'manager': manager_policy,
                            'object': object_policy,
                            'date_end': date_end,
                        }
                    )

        policy_base = PolicyBase.objects.filter(status__name='В работе').order_by('date_end')

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
                date_end = datetime.date(datetime.datetime.today().year, month_number+1, 1)
            else:
                date_end = datetime.date(datetime.datetime.today().year, 1, 1)
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

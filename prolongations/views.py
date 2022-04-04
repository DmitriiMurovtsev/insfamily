from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import csv

from .forms import UploadFileForm

from .models import Status, PolicyOnProlongation


@login_required(login_url='login')
def upload_policy(request):
    # Загрузка полисов в базу
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            text = 'Загружен'
            print(request.FILES['file'])

    context = {
        'text': text,
    }

    return render(request, 'prolongations/status_change.html', context)


@login_required(login_url='login')
def status_change(request):
    # Изменение статусов и Статистика по пролонгации
    text = ''
    form = UploadFileForm()
    datas = {}

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            text = 'Загружен'
            with open('prolongations/file/date.csv', 'wb') as file:
                for row in request.FILES['file'].chunks():
                    file.write(row)

            with open('prolongations/file/date.csv', 'r') as file_1:
                reader = csv.DictReader(file_1, delimiter=';')
                for rows in reader:
                    datas['name'] = rows['фио']
                    datas['phone'] = rows['телефон']

    context = {
        'text': text,
        'form': form,
        'datas': datas,
    }

    return render(request, 'prolongations/status_change.html', context)



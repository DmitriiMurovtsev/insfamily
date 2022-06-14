from django.shortcuts import render
from .models import Script, Step, Answer, Stage


def create_script(request):
    if request.method == 'POST':
        Script(name=request.POST['script_name']).save()

    scripts = Script.objects.all()

    return render(request, 'dscript/create_script.html', context={'scripts': scripts})


def show_script(request):
    if request.method == 'POST':
        Step(
            name=request.POST['step_name'],
            script_id=request.POST['script_id'],
        ).save()

    script = Script.objects.get(id=request.GET['script_id'])
    steps = Step.objects.filter(script_id=script.id)

    context = {
        'script': script,
        'steps': steps,
    }

    return render(request, 'dscript/show_script.html', context)


def show_step(request):
    answer_text_for_read = ''
    if request.method == 'POST':
        if 'link_answer_name' in request.POST:
            # Создаёт переход к определённому шагу в скрипте
            answer = Answer(
                name=request.POST['link_answer_name'],
                text=request.POST['link_stage_text'],
            )

            answer.save()

            answer.stage.add(request.POST['stage_id'])
            answer.link = True
            answer.save()

        if 'stage_name_for_create' in request.POST:
            # Создаёт новый шаг скрипта
            count_ = Stage.objects.filter(step=request.POST['step_id']).order_by('-count')[0].count

            Stage(
                step_id=request.POST['step_id'],
                name=request.POST['stage_name_for_create'],
                count=count_ + 1,
                text='Новый шаг',
            ).save()

        if 'answer_text_for_read' in request.POST:
            # Сохраняет текст отработки возражений для вывода
            answer_text_for_read = Answer.objects.get(id=request.POST['answer_text_for_read']).text

        if 'stage_name' in request.POST:
            # Создание или редактирование шага скрипта
            if 'stage_id_for_edit' not in request.POST:
                Stage(
                    step_id=request.POST['step_id'],
                    name=request.POST['stage_name'],
                    count=1,
                    text=request.POST['stage_text'],
                    ).save()
            else:
                stage_for_edit = Stage.objects.get(id=request.POST['stage_id_for_edit'])
                stage_for_edit.name = request.POST['stage_name']
                stage_for_edit.text = request.POST['stage_text']
                stage_for_edit.save()

        if 'answer_name' in request.POST:
            # Создание ответа и добавление его к шагу скрипта
            answer = Answer(
                name=request.POST['answer_name'],
                text=request.POST['answer_text'],
            )

            answer.save()

            answer.stage.add(request.POST['stage_id'])

            if request.POST['type_answer'] == 'positive':
                answer.positive = True
                answer.save()
            elif request.POST['type_answer'] == 'neutral':
                answer.neutral = True
                answer.save()
            elif request.POST['type_answer'] == 'negative':
                answer.negative = True
                answer.save()

    step = Step.objects.get(id=request.GET['step_id'])
    answers = Answer.objects.all()
    stages = Stage.objects.filter(step=request.GET['step_id'])

    if len(stages) == 0:
        context = {
            'step': step,
            'stages': stages,
            'answers': answers,
            'answers_for_stage': '',
        }

        return render(request, 'dscript/show_step.html', context)

    if 'stage_id' in request.GET:
        stage = Stage.objects.get(id=request.GET['stage_id'])
    else:
        stage = Stage.objects.get(step=request.GET['step_id'], count=1)

    answers_for_stage = Answer.objects.filter(stage=stage)

    context = {
        'step': step,
        'stage': stage,
        'stages': stages,
        'answers': answers,
        'answers_for_stage': answers_for_stage,
        'answer_text_for_read': answer_text_for_read,
    }

    return render(request, 'dscript/show_step.html', context)

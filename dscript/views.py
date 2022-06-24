from django.shortcuts import render
from .models import Script, Step, Answer, Stage


def create_script(request):
    if request.method == 'POST':
        if 'script_name_for_delete' in request.POST:
            script_for_delete = Script.objects.get(id=request.POST['script_name_for_delete'])
            script_for_delete.delete()
        else:
            Script(name=request.POST['script_name']).save()

    scripts = Script.objects.all()

    return render(request, 'dscript/create_script.html', context={'scripts': scripts})


def show_script(request):
    if request.method == 'POST':
        if 'step_name_for_delete' in request.POST:
            step_for_delete = Step.objects.get(id=request.POST['step_name_for_delete'])
            step_for_delete.delete()
        else:
            new_step = Step(
                name=request.POST['step_name'],
                script_id=request.POST['script_id'],
            )
            new_step.save()

    script = Script.objects.get(id=request.GET['script_id'])
    steps = Step.objects.filter(script_id=script.id)

    context = {
        'script': script,
        'steps': steps,
    }

    return render(request, 'dscript/show_script.html', context)


def show_step(request):
    answer_text_for_read = ''
    stage_id_deleted = ''
    if request.method == 'POST':
        if 'answer_for_delete' in request.POST:
            answer_for_delete = Answer.objects.get(id=request.POST['answer_for_delete'])
            answer_for_delete.delete()

        if 'stage_for_delete' in request.POST:
            stage_for_delete = Stage.objects.get(id=request.POST['stage_for_delete'])
            if stage_for_delete.count == 1:
                stage_for_delete.name = 'Начало скрипта'
                stage_for_delete.text = ''
                stage_for_delete.save()
            else:
                stage_id_deleted = stage_for_delete.id
                answers_for_deleted = Answer.objects.filter(text__iregex=f'stage_id={stage_id_deleted}')
                stage_for_delete.delete()
                for answer in answers_for_deleted:
                    answer_for_delete = Answer.objects.get(id=answer.id)
                    answer_for_delete.delete()

        if 'stage_name_for_create' in request.POST:
            # Создаёт новый шаг скрипта
            count_ = Stage.objects.filter(step=request.POST['step_id']).order_by('-count')[0].count

            Stage(
                step_id=request.POST['step_id'],
                name=request.POST['stage_name_for_create'],
                count=count_ + 1,
                text=request.POST['stage_text_for_create'],
            ).save()

        if 'stage_name' in request.POST:
            # Создание или редактирование этапа скрипта
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

            if 'type_answer' in request.POST:
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
    script_id = step.script.id

    if len(stages) == 0:
        context = {
            'step': step,
            'stages': stages,
            'answers': answers,
            'script_id': script_id,
            'answers_for_stage': '',
        }

        return render(request, 'dscript/show_step.html', context)

    if 'stage_id' in request.GET:
        if stage_id_deleted != '' and request.GET['stage_id'] == stage_id_deleted:
            stage = Stage.objects.get(step=request.GET['step_id'], count=1)
        else:
            stage = Stage.objects.get(id=request.GET['stage_id'])
    else:
        stage = Stage.objects.get(step=request.GET['step_id'], count=1)

    answers_for_stage = Answer.objects.filter(stage=stage)

    context = {
        'step': step,
        'stage': stage,
        'stages': stages,
        'answers': answers,
        'script_id': script_id,
        'answers_for_stage': answers_for_stage,
        'answer_text_for_read': answer_text_for_read,
    }

    return render(request, 'dscript/show_step.html', context)

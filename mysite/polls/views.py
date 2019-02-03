from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from datetime import date
from itertools import chain

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def add_question(request):
    Question.objects.create(question_text = request.POST['question_txt'], 
                                pub_date = date.today())
    return HttpResponseRedirect(reverse('polls:index'))

def delete_question(request):
    if request.POST.getlist('question_id'):
        selected_question = [ Question.objects.get(pk=q_id) for q_id in request.POST.getlist('question_id')]
        for sel_q in selected_question:
            sel_q.delete()
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        context = {'latest_question_list': latest_question_list,
                    'error_message': "You didn't select a question.",}
        return render(request, 'polls/index.html', context)
        
def view_edit(request):
    if request.POST.getlist('question_id'):
        selected_question = [ Question.objects.get(pk=q_id) for q_id in request.POST.getlist('question_id')]
        context = {"sel_question_list": selected_question,}
        return render(request, 'polls/edit_question.html', context)
    else:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        context = {'latest_question_list': latest_question_list,
                    'error_message': "You didn't select a question.",}
        return render(request, 'polls/index.html', context)
        
def edit_question(request):
    for key in request.POST:
            if 'question' in key:
                q_id = int(key.split("_")[2])
                selected_question = Question.objects.get( pk=q_id )
                selected_question.question_text = request.POST[ key ]
                selected_question.save()
    return HttpResponseRedirect(reverse('polls:index'))

def show_table_question(request):
    question_fields = Question._meta.fields
    question_list = Question.objects.values_list().all()
    context = {"question_fields": question_fields,
            "question_list": question_list,}
    return render(request, 'polls/table_question.html',context)

def show_table_choice(request, question_id):
    choice_fields = Choice._meta.fields
    choice_list = Choice.objects.filter(question_id=question_id).values_list()
    print(list(set(chain.from_iterable(
    (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
    for field in Choice._meta.get_fields()
    # For complete backwards compatibility, you may want to exclude
    # GenericForeignKey from the results.
    if not (field.many_to_one and field.related_model is None)
    ))))
    context = {"choice_fields": choice_fields,
            "choice_list": choice_list,}
    return render(request, 'polls/table_choice.html',context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        
def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question,
            "action":"Add"}
    return render(request, 'polls/add_edit_choice.html', context)        

def edit_delete_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if (request.POST['action']) == "Delete":
            selected_choice.delete()
            return render(request, 'polls/detail.html', {'question': question,})
        elif (request.POST['action']) == "Edit":
            context = {'question': question,
                "sel_choice_obj": selected_choice,
                "action":"Edit"}
            return render(request, 'polls/add_edit_choice.html', context)

def save_choice(request, question_id):
    if ("save_edit" in request.POST):
        selected_choice = Choice.objects.get(pk=request.POST['choice_id'])
        selected_choice.choice_text = request.POST['choice_txt']
        selected_choice.save()
    elif ("save_add" in request.POST):
        question = get_object_or_404(Question, pk=question_id)
        question.choice_set.create(choice_text = request.POST['choice_txt'])

    return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
"""
def index(request): 
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
        #辞書 templateのlastest_question_listの部分に、ここに書かれているlatest_question_listを入れている？
    }
    return render(request, 'polls/index.html', context)

"""


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        #まだpublishedされていないquesitonを排除
        return Question.objects.filter(pub_date__lte=timezone.now())
    

"""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
"""

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

"""
def results(request, question_id):
    response = "You're looking at the results of question {}." .format(question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        #POSTデータにchoiceがなかったら、KeyErrorを送出する
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        #ここの引数はURLにquestion.idが入ってるからその分？
# Create your views here.

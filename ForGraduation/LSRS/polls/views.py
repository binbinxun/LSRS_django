from django.http import HttpResponse
from .models import Question
from django.http import Http404
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


from django.shortcuts import render
from django.template import loader
# Create your views here.
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist  ")
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

def vote(request, question_id):

    return HttpResponse("You're voting on question %s." % question_id)
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context={
        "latest_question_list":latest_question_list
    }
    return render(request,"polls/index.html",context)

# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

from .forms import QuestionForm


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""
			Return the last five published questions (not including those set to be
			published in the future)
		"""
		return Question.objects.filter(
					pub_date__lte =  timezone.now()
				).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""
			excludes questions that not are published yet
		"""
		return Question.objects.filter( pub_date__lte = timezone.now )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': p,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
	return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def new(request):
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			print "SI ES válido !! "
			question = Question(
				question_text=form.cleaned_data['question_text'],
				pub_date=form.cleaned_data['pub_date'],
			)
			question.save()
			return HttpResponseRedirect(reverse('polls:index'))
		else:
			print "-- >> NO es VALIDO"
	# if a GET (or any other method) we'll create a blank form
	else:
		print "NO ES UN ( POST )"
		form = QuestionForm()
	return render(request, 'polls/new.html', {'form': form})


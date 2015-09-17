# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

from .forms import QuestionForm, ChoiceForm

from django.views.generic.edit import UpdateView


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
		# además del form dinámico, recibo una lista de opciones a crear asociadas a la question.
		# Lo primero es ver si existe la question.

		form = QuestionForm(request.POST)
		# ahora creo los hijos.
		votesValid = False
		for i in request.POST['choices'].split(","):
			if i:
				votesValid = True
				"""ch = Choice(
						question = form.field.pk,
						choice_text = i.strip(),
						votes = 0,
					)
				"""
		if not votesValid:
			form.add_error(None, 'Insert valid Votes')
			votesValid = False

		if form.is_valid() and votesValid:
			#Primero valido la lista recibida
			q = form.save()
			print q.pk
		else:
			if not votesValid:
				form.add_error(None, 'Insert valid Votes')
			return render(request, 'polls/new.html', {'form': form})

		return HttpResponseRedirect(reverse('polls:index'))
	# if a GET (or any other method) we'll create a blank form
	else:
		form = QuestionForm()
	return render(request, 'polls/new.html', {'form': form})


class UpdateView(UpdateView):
	model = Question
	fields = ["question_text"]
	template_name = 'polls/update.html'

	def post(self, *args, **kwargs):
		self.success_url = reverse_lazy('polls:detail', args=(kwargs['pk'],))
		return super(UpdateView, self).post(*args, **kwargs)


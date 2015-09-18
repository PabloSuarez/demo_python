# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.forms.models import inlineformset_factory

from .models import Question, Choice
from .forms import QuestionForm
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


class UpdateView(UpdateView):
	model = Question
	fields = ["question_text"]
	template_name = 'polls/update.html'

	def post(self, *args, **kwargs):
		self.success_url = reverse_lazy('polls:detail', args=(kwargs['pk'],))
		return super(UpdateView, self).post(*args, **kwargs)


def new(request):
	question = Question()
	ChoiceInlineFormSet = inlineformset_factory(Question, Choice, form=QuestionForm, extra=2, can_delete=False)

	if request.method == 'POST':
		questionForm = QuestionForm(request.POST, request.FILES, instance=question, prefix="main")
		choiceInlineFormSet = ChoiceInlineFormSet(request.POST, request.FILES, instance=question, prefix="nested")

		if questionForm.is_valid() and choiceInlineFormSet.is_valid():
			questionForm.save()
			choiceInlineFormSet.save()
		else:
			return render(request, 'polls/new.html', {'questionForm': questionForm, 'formset': choiceInlineFormSet})
	else:
		questionForm = QuestionForm(instance=question, prefix="main")
		choiceInlineFormSet = ChoiceInlineFormSet(instance=question, prefix="nested")
	return render(request, 'polls/new.html', {'questionForm': questionForm, 'formset': choiceInlineFormSet})

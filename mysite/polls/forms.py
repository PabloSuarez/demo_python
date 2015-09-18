from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = "__all__"
		exclude = ["votes",]


class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = "__all__"

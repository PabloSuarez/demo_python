from django import forms
import datetime

class QuestionForm(forms.Form):
	question_text = forms.CharField(max_length=100, required=True, initial="")
	pub_date = forms.DateField(initial="")

from django import forms
from .models import Case
import datetime


class DetailForm(forms.Form):
	param_name = forms.CharField()
	param_value = forms.IntegerField()
	param_period = forms.DateField()


class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()


class CaseForm(forms.Form):
	Case_Name = forms.CharField( max_length=50, label="Название кейса")
	Case_Comment = forms.CharField(max_length=150, label="Комментарий к кейсу")


class CreateJobForm(forms.Form):
	Case_Name = forms.CharField(max_length=100, label="Предприятие")
	Case_Comment = forms.CharField(max_length=300, label="Описание")
	Case_Header = forms.CharField(max_length=50, label="Заголовок")
	Case_Params = forms.CharField(max_length=100, label="Параметры")
	Params_Period = forms.IntegerField(min_value=1900, max_value=datetime.datetime.now().year, label="Даты")


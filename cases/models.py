from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import datetime

#Класс для обзорной информации предприятия/региона
class Case(models.Model):
    Case_Name = models.CharField('Название кейса', max_length=50)
    Case_Comment = models.TextField('Коментарий')
    Is_Pattern = models.BooleanField('Шаблон', default=False)
    Is_Pattern_For_Teacher = models.BooleanField('Шаблон для преподавателя', default=False)
    Is_Ready = models.BooleanField('Готов к использованию', default=False)

    Case_Title = models.TextField('Наименование;ИНН')
    Case_Location = models.TextField('Год основания, месторасположения')
    Case_Type_of_activity = models.TextField('Основные виды деятельности')
    Case_Production = models.TextField('Выпускаемая продукция')

    #Is_Analitical = models.BooleanField('Задание созданное студентом', default=False)

    def __str__(self):
        return self.Case_Name

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'

#Класс для создания экономических параметров
class CaseParametr(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    Param_Name = models.CharField('Название параметра', max_length=200)
    Param_Comment = models.TextField('Коментарий')
    Name_Variable = models.CharField('Имя переменной', max_length=20, blank=True, null=True)
    Formula = models.TextField('Формула для вычисления этого параметра', blank=True, null=True)

    # Функция для вывода формулы и времени её вычислений
    def CalcInFormula(self, user):
        for date in self.dateparam_set.all():
            self.getResultInFormula(date, user)

    # Функция для преобразования текста формулы в числовое
    def replaceParam(self, dateparam, user):
        formula = self.Formula
        for param in self.case.caseparam_set.all():
            if param.Name_Variable:
                print(param.Name_Variable, dateparam.Param_Period.year)
                formula = formula.replace(param.Name_Variable, str(
                    param.dateparam_set.get(Param_Period=dateparam.Param_Period).getValue(user)))
        return formula

    # Функция для получения результата формулы
    def getResultInFormula(self, dateparam, user):
        if self.Formula:
            Is_Prep = user.groups.filter(name="Преподаватель").exists()
            formula = self.replaceParam(dateparam, user)
            result = None
            try:
                result = round(eval(formula), 2)
                if Is_Prep:
                    dateparam.Param_Value = result
                else:
                    dateparam.Param_UserValue = result
                dateparam.save()
            except Exception as e:
                pass
            return round(result, 2)
        return None

    def __str__(self):
        return self.Param_Name

    class Meta:
        verbose_name = 'Параметр кейса'
        verbose_name_plural = 'Параметры кейсов'





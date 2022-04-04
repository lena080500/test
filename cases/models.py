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

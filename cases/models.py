from django.db import models
#from django.contrib.auth.models import User
from django.db.models import Q
import datetime


#Класс для обзорной информации предприятия/региона
class Case(models.Model):
    Case_Name = models.CharField('Название кейса', max_length=50)
    Case_Comment = models.TextField('Коментарий')
    #Is_Pattern = models.BooleanField('Шаблон', default=False)
    #Is_Pattern_For_Teacher = models.BooleanField('Шаблон для преподавателя', default=False)
    #Is_Ready = models.BooleanField('Готов к использованию', default=False)
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
            #Is_Prepod = user.groups.filter(name="Преподаватель").exists()
            formula = self.replaceParam(dateparam, user)
            result = None
            try:
                result = round(eval(formula), 2)
                '''if Is_Prepod:
                    dateparam.Param_Value = result
                else:'''
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


#Класс для даты создания кейса и его данных
class DateParametr(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    CaseParametr = models.ForeignKey(CaseParametr, on_delete=models.CASCADE)
    Param_UserValue = models.FloatField('Введенное значение пользователем', default=0)
    Param_Period = models.DateField('Период сбора данных')
    Param_Formula = models.CharField('Формула', max_length=200, default='')

    #Получить значение введённого параметра пользователем
    def getValue(self, user):
        '''if user.groups.filter(name="Преподаватель").exists():
            return self.Param_Value'''
        return self.Param_UserValue

    #Проверка правильности введённости аргументов
    def GetCheckTrueArgument(self):
        MyCase = self.Case
        #CaseOfPrepod = MyCase.jobparam_set.last().job_set.last().CaseOfPrepod
        CaseOfPrepod = MyCase.jobparam_set.last().CaseOfPrepod

        nameParam = self.CaseParam.Param_Name
        '''TrueCaseParam = CaseOfPrepod.caseparam_set.filter(NameParam=nameParam).last()
        TrueDateParam = TrueCaseParam.dateparam_set.filter(Param_Period=self.Param_Period)'''
        TrueCaseParam = CaseOfPrepod.caseparam_set.filter(NameParam=nameParam).last()
        TrueDateParam = TrueCaseParam.dateparam_set.filter(Param_Period=self.Param_Period)

        return TrueDateParam.Param_Value == self.Param_UserValue

    def __str__(self):
        return self.CaseParametr.Param_Name + " " + str(self.Param_Period.year)

    class Meta:
        verbose_name = 'Период сбора данных'
        verbose_name_plural = 'Периоды сбора данных'


# Параметр работы, содержит в себе ссылку на кейс, так же содержит в себе имя работы которое
# отображается только у студента
class JobParametr(models.Model):
    Case = models.ForeignKey(Case, on_delete=models.CASCADE)

    Param_Name = models.CharField('Наименование', max_length=50)
    Param_Help = models.CharField('Коментарий', max_length=1000)
    Param_TrueValue = models.BooleanField()
    Param_Period = models.DateField('Дата создания')

    def __str__(self):
        return self.Param_Name

    class Meta:
        verbose_name = 'Рабочий параметр'
        verbose_name_plural = 'Рабочие параметры'


# Работа - содержит в себе начала создания этой работы, содержит ссылку на пользователя который ее создал
# благодоря этому мы можем сделать права доступа на кейс, то есть другой пользователь (кроме преподавателя) не сможет посмотреть его
class Job(models.Model):
    Job_Parametr = models.ForeignKey(JobParametr, on_delete=models.CASCADE)
    #User = models.ForeignKey(User, on_delete=models.PROTECT)
    Job_Title = models.CharField('Название работы', max_length=50)
    Starting_Date = models.DateTimeField('Дата начала работы')
    Job_Status = models.BooleanField('Статус выполнения работы')
    Job_is_evaluated = models.BooleanField('Работа оценена', default=False)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return self.Job_Title


# Файлы которые заагружает преподаватель к кейсу, доументация и прочее
class UserFile(models.Model):
    Job = models.ForeignKey(Job, on_delete=models.CASCADE)
    #User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    File = models.FileField(upload_to='files/', max_length=100)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.File.name


'''class GroupStud(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название группы')
    users = models.ManyToManyField(User, verbose_name='Студенты')

    class Meta:
        verbose_name = 'Группа студентов'
        verbose_name_plural = 'Группы студентов'

    def __str__(self):
        return self.name'''

import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from cases.FormTable import CreateJobForm
from cases.models import Job, Case, CaseParametr, DateParametr, JobParametr


# Создание полноценного кейса с параметрами и разделами
@login_required
def createcase(request):
    #if request.user.groups.filter(name="Преподаватель").exists():
    if request.user.exists():
        if request.method == "POST":
            form = CreateJobForm(request.POST)
            if form.is_valid:
                case = Case(Case_Name=request.POST.get("Case_Name"), Case_Comment=request.POST.get("Case_Comment"),
                            Is_Pattern=True)
                case.save()
                Jobparametr = JobParametr.objects.create(Case=Case.objects.last(), Param_Name=case.Case_Name,
                                                   Param_Help=case.Case_Comment, Param_TrueValue=False,
                                                   Param_Period=datetime.datetime.now())
                Jobparametr.save()
                job = Job.objects.create(Job_Param=Jobparametr.objects.last(), User=request.user,
                                         Job_Title=Jobparametr.Param_Name, Starting_Date=datetime.datetime.now(),
                                         Job_Status=False)
                job.save()
                '''section = Section.objects.create(Name_Section=request.POST.get("Case_Header"), case=Case.objects.last())
                section.save()

                choice = Choice.objects.get(description=request.POST.get("selected"))'''

                '''parametr = CaseParam.objects.create(case=Case.objects.last(), section=Section.objects.last(),
                                                 choice=choice, Param_Name=request.POST.get("Case_Header"),
                                                 Param_Help='...', Param_TrueValue=False)'''
                parametr = CaseParametr.objects.create(case=Case.objects.last(),
                                                       Param_Name=request.POST.get("Case_Header"),
                                                       Param_Help='...', Param_TrueValue=False)
                parametr.save()
                i = 0
                for Param in request.POST.getlist('Param'):
                    '''Caseparam = CaseParametr.objects.create(case=Case.objects.last(), section=Section.objects.last(), 
                    choice=choice, Param_Name=Param,
                    Param_Help=request.POST.getlist('Param_Comment')[i],
                    Param_TrueValue=False)'''
                    Caseparam = CaseParametr.objects.create(case=Case.objects.last(),
                                                         Param_Name=Param,
                                                         Param_Help=request.POST.getlist('Param_Comment')[i],
                                                         Param_TrueValue=False)
                    Caseparam.save()
                    i = i + 1
                    for Period in request.POST.getlist('Period'):
                        date = datetime.date(int(Period), 1, 1)
                        Dateparam = DateParametr.objects.create(Case=Case.objects.last(),
                                                             CaseParam=CaseParametr.objects.last(), Param_UserValue=0,
                                                             Param_Value=0, Param_Period=date)
                        Dateparam.save()
                #return render(request, 'cases/cases.html', {'case': Case, 'choices': Choice.objects.all()})
                return render(request, 'cases/createcases.html', {'case': Case})
        '''else:
            sections = Choice.objects.all()
            form = CreateJobForm()
            return render(request, 'cases/createcases.html', {'form': form, 'sections': sections})'''
    else:
        return HttpResponseRedirect('/')


@login_required
def edit(request, case_id):
    #choices = Choice.objects.all()
    case = Case.objects.get(id=case_id)
    if case.jobparam_set.last().job_set.last().User == request.user:
        dateparams = DateParametr.objects.all().filter(Case_id=case.id)
        if request.method == "POST":
            for param in dateparams.all():
                param.Param_Value = request.POST.get("DateParam_" + str(param.id))
                param.save()
            for Param in CaseParametr.objects.filter(case_id=case.id).all():
                nameparam = request.POST.get("Param_" + str(Param.id))
                if nameparam:
                    Param.Param_Name = request.POST.get("Param_" + str(Param.id))
                    Param.save()
            return HttpResponseRedirect('/cases')
        #return render(request, 'cases/edit.html', {'case': case, 'choices': choices})
        return render(request, 'cases/editcases.html', {'case': case})
    else:
        return HttpResponseRedirect('/')


'''@login_required
def case_param(request):
    #if request.user.groups.filter(name="Преподаватель").exists():
    if request.user.exists():
        form = CaseParametr()
        return render(request, 'cases/createtablecases.html', {'form': form})
    return HttpResponseRedirect('/')'''

# Таблица со всеми параметрами кейса
@login_required
def allparamcases(request):
    #if request.user.groups.filter(name="Преподаватель").exists():
    if request.user.exists():
        caseParametrs = CaseParametr.objects.filter(case__Is_Pattern=True)
        for paramofcase in caseParametrs:
            if request.GET.get(str(paramofcase.id)) != None:
                paramofcase.delete()
        return render(request, 'cases/allparametrcases.html', {'caseParametrs': caseParametrs})
    return HttpResponseRedirect('/')


# Таблица со всеми параметрами параметров кейса
@login_required
def alldateparams(request):
    #if request.user.groups.filter(name="Преподаватель").exists():
    if request.user.exists():
        dateParametrs = DateParametr.objects.filter(Case__Is_Pattern=True)
        for dateparam in dateParametrs:
            if request.GET.get(str(dateparam.id)) != None:
                dateparam.delete()
                return render(request, 'cases/alldateparametrs.html', {'dateParametrs': dateParametrs})
        return render(request, 'cases/alldateparametrs.html', {'dateParametrs': dateParametrs})
    return HttpResponseRedirect('/')


'''# Редактирование параметров кейса (преподаватель), то есть преподаватель изменяет правильные значения которые будут
# использовваться в сравнении результатов студента
@login_required
def edit(request, case_id):'''

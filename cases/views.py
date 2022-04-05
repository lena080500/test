from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from cases.models import Job, Case, CaseParametr, DateParametr


@login_required
def index(request, case_id):
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

@login_required
def case_param(request):
    #if request.user.groups.filter(name="Преподаватель").exists():
    if request.user.exists():
        form = CaseParametr()
        return render(request, 'cases/create.html', {'form': form})
    return HttpResponseRedirect('/')

'''# Редактирование параметров кейса (преподаватель), то есть преподаватель изменяет правильные значения которые будут
# использовваться в сравнении результатов студента
@login_required
def edit(request, case_id):'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from cases.models import Job, Case, CaseParametr


@login_required
def index(request):
    if request.method == "POST":
        if request.POST.get('save'):
            job_name = request.POST.get("Job_Title")
            job_comment = request.POST.get("Job_Comment")
            Oldcase_id = request.POST.get("case")
            user = request.user
            Job.copy(job_name, job_comment, Oldcase_id, user, request)
        jobs = request.user.job_set.all()
        for job in jobs:
            if request.POST.get(str(job.Job_Param.Case.id)) != None:
                deletecase = Case.objects.get(id=job.Job_Param.Case.id)
                deletecase.delete()

    Job_list = Job.objects.all()
    #My_Jobs = Job.objects.filter(User_id=request.user.id)
    return render(request, 'cases/cases.html', {'Job_list': Job_list})

# Редактирование параметров кейса (преподаватель), то есть преподаватель изменяет правильные значения которые будут
# использовваться в сравнении результатов студента
@login_required
def edit(request, case_id):
    choices = Choice.objects.all()
    case = Case.objects.get(id=case_id)
    if case.jobparam_set.last().job_set.last().User == request.user:
        dateparams = DateParam.objects.all().filter(Case_id=case.id)
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
        return render(request, 'cases/edit.html', {'case': case, 'choices': choices})
    else:
        return HttpResponseRedirect('/')
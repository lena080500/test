from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Case, CaseParametr, Job


# Представление отображает задания которые делают студенты, статистика по каждой работе
@login_required
def students(request):
    if request.user.groups.filter(name="Преподаватель").exists():
        users = Group.objects.get(name="Студент").user_set.all()
        if request.method == 'POST':
            for user in users:
                if user.groups.filter(name='Студент').exists():
                    if user.job_set.count() == 0:
                        #Job.copy('ПАО ЧТПЗ', 'Оценка уровня экономической безопасности компании', 191, user, request)
        return render(request, 'cases/students.html', {'users': users, 'groups': GroupUser.objects.all()})
    return HttpResponseRedirect('/')
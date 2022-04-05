from django.contrib import admin
from .models import Case, CaseParametr, DateParametr, JobParametr, Job

admin.site.register(Case)
admin.site.register(CaseParametr)
admin.site.register(DateParametr)
admin.site.register(JobParametr)
admin.site.register(Job)

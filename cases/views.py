from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import Case, CaseParametr, Job, GroupStud


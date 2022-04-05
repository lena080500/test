from django.urls import path
from .import views

app_name = 'cases'

urlpatterns = [
    path('createcase/', views.createcase, name='createcase'),
    path('editcases/<int:case_id>', views.edit, name='editcases'),
    path('alldateparametrs/', views.alldateparams, name='alldateparametrs'),
]
from django.urls import path
from .import views

app_name = 'cases'

urlpatterns = [
    path('', views.index, name='index'),
    #path('editcases/<int:case_id>', views.edit, name = 'edit'),
]
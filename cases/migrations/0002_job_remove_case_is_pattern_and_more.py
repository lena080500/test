# Generated by Django 4.0.3 on 2022-04-05 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Job_Title', models.CharField(max_length=50, verbose_name='Название работы')),
                ('Starting_Date', models.DateTimeField(verbose_name='Дата начала работы')),
                ('Job_Status', models.BooleanField(verbose_name='Статус выполнения работы')),
                ('Job_is_evaluated', models.BooleanField(default=False, verbose_name='Работа оценена')),
            ],
            options={
                'verbose_name': 'Работа',
                'verbose_name_plural': 'Работы',
            },
        ),
        migrations.RemoveField(
            model_name='case',
            name='Is_Pattern',
        ),
        migrations.RemoveField(
            model_name='case',
            name='Is_Pattern_For_Teacher',
        ),
        migrations.RemoveField(
            model_name='case',
            name='Is_Ready',
        ),
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('File', models.FileField(upload_to='files/')),
                ('Job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.job')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='JobParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Param_Name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('Param_Help', models.CharField(max_length=1000, verbose_name='Коментарий')),
                ('Param_TrueValue', models.BooleanField()),
                ('Param_Period', models.DateField(verbose_name='Дата создания')),
                ('Case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case')),
            ],
            options={
                'verbose_name': 'Рабочий параметр',
                'verbose_name_plural': 'Рабочие параметры',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='Job_Param',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.jobparam'),
        ),
        migrations.CreateModel(
            name='DateParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Param_UserValue', models.FloatField(default=0, verbose_name='Введенное значение пользователем')),
                ('Param_Period', models.DateField(verbose_name='Период сбора данных')),
                ('Param_Formula', models.CharField(default='', max_length=200, verbose_name='Формула')),
                ('CaseParametr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.caseparametr')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case')),
            ],
            options={
                'verbose_name': 'Период сбора данных',
                'verbose_name_plural': 'Периоды сбора данных',
            },
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-05 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_job_remove_case_is_pattern_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DateParam',
            new_name='DateParametr',
        ),
        migrations.RenameModel(
            old_name='JobParam',
            new_name='JobParametr',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='Job_Param',
            new_name='Job_Parametr',
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-29 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Applicant', '0008_resume'),
        ('job_app', '0006_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='applicants',
            field=models.ManyToManyField(blank=True, related_name='applied_jobs', to='Applicant.applicant'),
        ),
        migrations.DeleteModel(
            name='Application',
        ),
    ]

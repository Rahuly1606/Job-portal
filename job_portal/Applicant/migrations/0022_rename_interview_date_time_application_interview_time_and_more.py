# Generated by Django 5.1.1 on 2024-11-05 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Applicant', '0021_alter_application_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='interview_date_time',
            new_name='interview_time',
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('review', 'Review'), ('Pending', 'Pending'), ('interview', 'Interview'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='review', max_length=10),
        ),
    ]

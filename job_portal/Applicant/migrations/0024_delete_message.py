# Generated by Django 5.1.1 on 2024-11-06 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Applicant', '0023_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
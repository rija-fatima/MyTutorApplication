# Generated by Django 2.1.5 on 2020-03-21 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytutor', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teachers',
        ),
    ]

# Generated by Django 2.1.5 on 2020-03-21 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytutor', '0006_courseteacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profiles/avatar.png', upload_to='profiles/'),
        ),
    ]
# Generated by Django 2.1.5 on 2020-03-21 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mytutor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mytutor.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mytutor.User')),
            ],
        ),
    ]

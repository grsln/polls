# Generated by Django 2.2.10 on 2021-01-20 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answerchoice',
            name='choice',
        ),
        migrations.AddField(
            model_name='answerchoice',
            name='choice',
            field=models.ManyToManyField(to='polls_api.Choice'),
        ),
    ]

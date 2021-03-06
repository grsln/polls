# Generated by Django 2.2.10 on 2021-01-20 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Ответ вариантами',
                'verbose_name_plural': 'Ответы вариантами',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Тема опроса')),
                ('start_date', models.DateTimeField(verbose_name='Начало опроса')),
                ('end_date', models.DateTimeField(verbose_name='Конец опроса')),
                ('description', models.CharField(max_length=200, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
            },
        ),
        migrations.CreateModel(
            name='UserPolls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(verbose_name='UserID')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls_api.Poll')),
            ],
            options={
                'verbose_name': 'Опросы пользователя',
                'verbose_name_plural': 'Опросы пользователей',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='Вопрос')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Text'), (2, 'One variant'), (3, 'Many variants')], verbose_name='Тип вопроса')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls_api.Poll')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=200, verbose_name='Вариант')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='polls_api.Question')),
            ],
            options={
                'verbose_name': 'Вариант',
                'verbose_name_plural': 'Варианты',
            },
        ),
        migrations.CreateModel(
            name='AnswerText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Тест ответа')),
                ('answer_choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='texts', to='polls_api.AnswerChoice')),
            ],
            options={
                'verbose_name': 'Ответ текстом',
                'verbose_name_plural': 'Ответы текстом',
            },
        ),
        migrations.AddField(
            model_name='answerchoice',
            name='choice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls_api.Choice'),
        ),
        migrations.AddField(
            model_name='answerchoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls_api.Question'),
        ),
        migrations.AddField(
            model_name='answerchoice',
            name='userpoll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls_api.UserPolls'),
        ),
    ]

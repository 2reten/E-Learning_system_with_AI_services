# Generated by Django 5.0 on 2023-12-17 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_question_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='author',
        ),
    ]

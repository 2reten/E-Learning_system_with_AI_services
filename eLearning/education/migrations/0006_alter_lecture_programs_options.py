# Generated by Django 4.2.8 on 2024-01-05 07:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("education", "0005_lecture_programs_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lecture_programs",
            options={"verbose_name_plural": "Lecture Programs"},
        ),
    ]
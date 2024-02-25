# Generated by Django 4.1 on 2023-09-16 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("eduapp", "0008_quiz_quizanswer_quizquestion_result_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentExamAssociation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_allowed", models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name="quiz",
            name="students",
            field=models.ManyToManyField(
                related_name="exams",
                through="eduapp.StudentExamAssociation",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="studentexamassociation",
            name="exam",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="eduapp.quiz"
            ),
        ),
        migrations.AddField(
            model_name="studentexamassociation",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]

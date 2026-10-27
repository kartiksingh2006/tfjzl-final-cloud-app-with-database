# Initial database schema for the online course exam application.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Instructor', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('bio', models.TextField(blank=True)),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course_instructor_profile', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='Learner', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course_learner_profile', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='Course', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=200)),
            ('description', models.TextField(blank=True)),
            ('instructors', models.ManyToManyField(blank=True, related_name='courses', to='onlinecourse.instructor')),
        ], options={'ordering': ['name']}),
        migrations.CreateModel(name='Lesson', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('title', models.CharField(max_length=200)),
            ('content', models.TextField(blank=True)),
            ('order', models.PositiveIntegerField(default=1)),
            ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='onlinecourse.course')),
        ], options={'ordering': ['order', 'id']}),
        migrations.CreateModel(name='Enrollment', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('date_enrolled', models.DateTimeField(auto_now_add=True)),
            ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='onlinecourse.course')),
            ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='onlinecourse.learner')),
        ], options={'ordering': ['-date_enrolled'], 'unique_together': {('student', 'course')}}),
        migrations.CreateModel(name='Question', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('question_text', models.CharField(max_length=1000)),
            ('order', models.PositiveIntegerField(default=1)),
            ('grade', models.PositiveIntegerField(default=1, help_text='Points awarded for a correct answer.')),
            ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='onlinecourse.course')),
        ], options={'ordering': ['order', 'id']}),
        migrations.CreateModel(name='Choice', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('choice_text', models.CharField(max_length=500)),
            ('is_correct', models.BooleanField(default=False)),
            ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='onlinecourse.question')),
        ]),
        migrations.CreateModel(name='Submission', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('score', models.PositiveIntegerField(default=0)),
            ('total', models.PositiveIntegerField(default=0)),
            ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ('choices', models.ManyToManyField(blank=True, related_name='submissions', to='onlinecourse.choice')),
            ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='onlinecourse.enrollment')),
        ], options={'ordering': ['-submitted_at']}),
    ]

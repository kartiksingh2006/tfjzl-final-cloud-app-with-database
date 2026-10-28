from django.conf import settings
from django.db import models


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_instructor_profile')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_username()


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_learner_profile')

    def __str__(self):
        return self.user.get_username()


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructors = models.ManyToManyField(Instructor, related_name='courses', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.course.name} — {self.title}'


class Enrollment(models.Model):
    student = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-date_enrolled']

    def __str__(self):
        return f'{self.student} - {self.course.name}'


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=1000)
    order = models.PositiveIntegerField(default=1)
    grade = models.PositiveIntegerField(default=1, help_text='Points awarded for a correct answer.')

    class Meta:
        ordering = ['order', 'id']

    def is_get_score(self, selected_ids):
        correct_ids = set(self.choices.filter(is_correct=True).values_list('id', flat=True))
        selected_ids = {int(choice_id) for choice_id in selected_ids}
        return self.grade if correct_ids == selected_ids else 0

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions', blank=True)
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'Submission {self.id} for enrollment {self.enrollment.id}'

from django.conf import settings
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
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

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=1000)
    order = models.PositiveIntegerField(default=1)
    grade = models.PositiveIntegerField(default=1, help_text='Points awarded for a correct answer.')
    class Meta:
        ordering = ['order', 'id']
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.text

class Submission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_submissions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions', blank=True)
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-submitted_at']
    def __str__(self):
        return f'{self.student} — {self.course} ({self.score}/{self.total})'

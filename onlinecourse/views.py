from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from .models import Choice, Course, Submission

def course_list(request):
    return render(request, 'onlinecourse/course_list.html', {'courses': Course.objects.all()})

def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related('lessons', 'questions__choices'), pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

@login_required
@transaction.atomic
def submit(request, course_id):
    if request.method != 'POST':
        return redirect('onlinecourse:course_details', course_id=course_id)
    course = get_object_or_404(Course.objects.prefetch_related('questions__choices'), pk=course_id)
    questions = list(course.questions.all())
    if not questions:
        messages.error(request, 'This course does not have an exam yet.')
        return redirect('onlinecourse:course_details', course_id=course.id)
    selected_choices, score = [], 0
    total = sum(question.grade for question in questions)
    for question in questions:
        choice_id = request.POST.get(f'question_{question.id}')
        if not choice_id:
            continue
        choice = Choice.objects.filter(pk=choice_id, question=question).first()
        if choice is None:
            continue
        selected_choices.append(choice)
        if choice.is_correct:
            score += question.grade
    submission = Submission.objects.create(student=request.user, course=course, score=score, total=total)
    submission.choices.set(selected_choices)
    return redirect('onlinecourse:show_exam_result', submission_id=submission.id)

@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission.objects.select_related('course', 'student').prefetch_related('choices'), pk=submission_id)
    if submission.student_id != request.user.id and not request.user.is_staff:
        raise Http404('Submission not found.')
    selected_by_question = {choice.question_id: choice for choice in submission.choices.all()}
    result_rows = []
    for question in submission.course.questions.prefetch_related('choices').all():
        selected = selected_by_question.get(question.id)
        correct_choice = next((choice for choice in question.choices.all() if choice.is_correct), None)
        result_rows.append({'question': question, 'selected': selected, 'correct_choice': correct_choice, 'is_correct': bool(selected and selected.is_correct)})
    percentage = round((submission.score / submission.total) * 100) if submission.total else 0
    return render(request, 'onlinecourse/exam_result.html', {'submission': submission, 'result_rows': result_rows, 'percentage': percentage, 'passed': percentage >= 60})

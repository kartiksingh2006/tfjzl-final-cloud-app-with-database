from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Course, Enrollment, Learner, Submission


def course_list(request):
    return render(request, 'onlinecourse/course_list.html', {'courses': Course.objects.all()})


def course_details(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related('lessons', 'questions__choices'),
        pk=course_id,
    )
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

    learner, _ = Learner.objects.get_or_create(user=request.user)
    enrollment, _ = Enrollment.objects.get_or_create(student=learner, course=course)

    selected_choices = []
    score = 0
    total = sum(question.grade for question in questions)

    for question in questions:
        selected_ids = request.POST.getlist(f'question_{question.id}')
        valid_choices = list(Choice.objects.filter(question=question, id__in=selected_ids))
        selected_choices.extend(valid_choices)
        score += question.is_get_score([choice.id for choice in valid_choices])

    submission = Submission.objects.create(enrollment=enrollment, score=score, total=total)
    submission.choices.set(selected_choices)
    return redirect(
        'onlinecourse:show_exam_result',
        course_id=course.id,
        submission_id=submission.id,
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related('enrollment__student__user', 'enrollment__course')
        .prefetch_related('choices'),
        pk=submission_id,
        enrollment__course_id=course_id,
    )
    if submission.enrollment.student.user_id != request.user.id and not request.user.is_staff:
        raise Http404('Submission not found.')

    course = submission.enrollment.course
    selected_by_question = {choice.question_id: choice for choice in submission.choices.all()}

    result_rows = []
    total_score = 0
    possible_score = 0
    for question in course.questions.prefetch_related('choices').all():
        selected = selected_by_question.get(question.id)
        selected_ids = [selected.id] if selected else []
        grade = question.is_get_score(selected_ids)
        possible = question.grade

        total_score += grade
        possible_score += possible

        correct_choice = next((choice for choice in question.choices.all() if choice.is_correct), None)
        result_rows.append({
            'question': question,
            'selected': selected,
            'selected_ids': selected_ids,
            'correct_choice': correct_choice,
            'is_correct': grade > 0,
            'grade': grade,
            'possible': possible,
        })

    percentage = round((total_score / possible_score) * 100) if possible_score else 0
    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'submission': submission,
        'course': course,
        'result_rows': result_rows,
        'score': total_score,
        'total': possible_score,
        'total_score': total_score,
        'possible_score': possible_score,
        'percentage': percentage,
        'passed': percentage >= 60,
    })

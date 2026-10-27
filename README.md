# Django Online Course Exam — Final Cloud App with Database

This repository contains a Django online course app with course lessons and a multiple-choice practice exam, implementing **Option 1: AI-Graded Submission** deliverables.

## Rubric deliverables

- **Models:** [onlinecourse/models.py](onlinecourse/models.py) — `Question`, `Choice`, `Submission`
- **Admin:** [onlinecourse/admin.py](onlinecourse/admin.py) — seven imported classes plus `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, `LessonAdmin`
- **Admin screenshot:** `docs/screenshots/03-admin-site.png` (capture locally after setup; instructions below)
- **Course page:** [course_details_bootstrap.html](onlinecourse/templates/onlinecourse/course_details_bootstrap.html) — Bootstrap course details, lessons, questions, choices
- **Views:** [onlinecourse/views.py](onlinecourse/views.py) — `submit` and `show_exam_result`
- **Routes:** [onlinecourse/urls.py](onlinecourse/urls.py) — URLs for submit and result
- **Final result screenshot:** `docs/screenshots/07-final.png` (capture locally after a successful mock exam; instructions below)

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/admin/> and sign in. Create a course under **OnlineCourse → Courses**, add lessons, then add questions and at least two choices per question. Mark one choice per question as correct. Go to <http://127.0.0.1:8000/> and open the course. Sign in before submitting the exam.

## Capture rubric screenshots

Use real screenshots from your running app, not placeholders.

1. **03-admin-site:** at `/admin/`, show both the **Authentication and Authorization** and **OnlineCourse** sections in the same screenshot. Use Windows `Win + Shift + S` to save as `docs/screenshots/03-admin-site.png`.
2. **07-final:** answer enough questions correctly for at least 60%, submit the exam, and capture the page showing **Congratulations!**, the score, and detailed results. Save as `docs/screenshots/07-final.png`.

Add these PNGs with git and push them to this repository before submitting the assignment.

## Implementation notes

The exam totals the point value (`grade`) for all course questions. A submitted choice is accepted only if it belongs to the question it answers. A submission result is visible only to its student or staff. A score of 60% or higher passes.

This is a local learning project. The included development secret key and `DEBUG=True` are not production settings. Before deployment, use environment-based secrets, configure allowed hosts and HTTPS, disable debug, and review Django's deployment checklist.

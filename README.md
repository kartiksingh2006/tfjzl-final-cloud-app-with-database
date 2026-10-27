# Django Online Course Exam — Final Cloud App with Database

This repository contains a Django online course app with course lessons and a multiple-choice practice exam, implementing **Option 1: AI-Graded Submission** deliverables.

## Rubric deliverables

- **Models:** [onlinecourse/models.py](onlinecourse/models.py) — `Question`, `Choice`, and `Submission`
- **Admin:** [onlinecourse/admin.py](onlinecourse/admin.py) — seven imported model classes plus `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, and `LessonAdmin`
- **Admin screenshot:** `docs/screenshots/03-admin-site.png` (capture locally; instructions below)
- **Course page:** [course_details_bootstrap.html](onlinecourse/templates/onlinecourse/course_details_bootstrap.html) — Bootstrap course details, lessons, questions, and choices
- **Views:** [onlinecourse/views.py](onlinecourse/views.py) — `submit` and `show_exam_result`
- **Routes:** [onlinecourse/urls.py](onlinecourse/urls.py) — submission and result routes
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

A committed initial migration is included, so `makemigrations` is not needed for a fresh checkout.

Open <http://127.0.0.1:8000/admin/> and sign in. Create a course under **OnlineCourse → Courses**, add lessons, then add questions and at least two choices per question. Mark exactly one choice per question as correct. Open <http://127.0.0.1:8000/> and select the course. Sign in before submitting the exam.

## Capture required screenshots

Use real screenshots from the running app, not placeholders.

1. **03-admin-site:** Visit `/admin/` and make sure both the **Authentication and Authorization** and **OnlineCourse** sections are visible in one screenshot. Save as `docs/screenshots/03-admin-site.png` (Windows: `Win + Shift + S`).
2. **07-final:** Sign in on the site, answer enough questions correctly to score at least 60%, and submit. Capture the result page showing **Congratulations!**, the score, and detailed results. Save as `docs/screenshots/07-final.png`.

Add the two PNG files to the repository before submitting the assignment. See [docs/screenshots/README.md](docs/screenshots/README.md).

## Implementation notes

The maximum score is the sum of question `grade` values. A selected choice is accepted only when it belongs to the question being answered. Results are visible only to the submitting student or staff users. A score of 60% or higher passes.

The development secret key and `DEBUG=True` are not suitable for production. Before deployment, use an environment-based secret, configure allowed hosts and HTTPS, disable debug, and follow Django's deployment checklist.

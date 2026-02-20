# Dynamic Django Portfolio

Production-ready dynamic portfolio built with Django 5, Django Templates, Django Admin, Tailwind CSS, CKEditor, and PostgreSQL-ready settings.

## Features

- Full admin-managed content for site profile, about, skills, experience, education, services, projects, testimonials, blog, and contact messages
- Published-only visibility for projects and blog posts
- Project JSON API endpoints (read-only, no DRF)
- SEO-ready templates with per-page meta/OG tags
- Dark mode toggle with localStorage
- Sitemap and robots routes
- Whitenoise static serving support for production
- Seed command for demo content
- Tests for project list, project detail, and contact submission

## Project structure

- `projects/` Django project settings and URL routing
- `core/` shared models (site settings, profile data, sections), context processor, seed command
- `portfolio/` home/about/projects pages + project API
- `blog/` blog list/detail pages
- `contact/` contact form + message storage
- `templates/` Django templates and reusable partials
- `static/` Tailwind source/build and JS theme toggle

## Setup (development)

1. Create and activate venv

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. Install Python dependencies

```bash
pip install -r requirements.txt
```

3. Copy environment file

```bash
copy .env.example .env
# or cp .env.example .env
```

4. Install Tailwind CLI tooling

```bash
npm install
```

5. Build CSS once (or use watch command in another terminal)

```bash
npm run build:css
# optional during development:
npm run watch:css
```

6. Run migrations + create superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

7. Seed demo content

```bash
python manage.py seed_portfolio
```

8. Run server

```bash
python manage.py runserver
```

## URLs

- `/` Home
- `/about/` About
- `/projects/` Project list
- `/projects/<slug>/` Project detail
- `/blog/` Blog list
- `/blog/<slug>/` Blog detail
- `/contact/` Contact form
- `/api/projects/` Project list JSON
- `/api/projects/<slug>/` Project detail JSON
- `/sitemap.xml`
- `/robots.txt`

## Production notes

- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS`
- Set `DATABASE_URL` to PostgreSQL
- Run `python manage.py collectstatic`
- Serve app with gunicorn/uvicorn and reverse proxy
- Whitenoise serves static files via `CompressedManifestStaticFilesStorage`

## Admin usage

All website sections are editable in Django Admin:

- Site settings + social links
- About section
- Skills and categories
- Experience
- Education
- Services
- Projects + inline gallery images + tags
- Testimonials
- Blog posts + tags
- Contact messages

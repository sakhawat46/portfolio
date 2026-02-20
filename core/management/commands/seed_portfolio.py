import random
from datetime import date

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import BlogPost, BlogTag
from contact.models import ContactMessage
from core.models import (
    AboutSection,
    Education,
    Experience,
    Service,
    SiteSettings,
    Skill,
    SkillCategory,
    SocialLink,
    Testimonial,
)
from portfolio.models import Project, ProjectImage, ProjectTag


class Command(BaseCommand):
    help = "Seed portfolio sample content."

    def handle(self, *args, **options):
        settings_obj, _ = SiteSettings.objects.get_or_create(
            site_name="Alex Carter Portfolio",
            defaults={
                "tagline": "Full-Stack Django Engineer",
                "short_bio": "I build robust web applications with Django and PostgreSQL.",
                "email": "alex@example.com",
                "phone": "+1-555-501-2201",
                "location": "San Francisco, CA",
                "default_meta_description": "Production-ready Django portfolio website.",
            },
        )

        SocialLink.objects.get_or_create(settings=settings_obj, name="GitHub", defaults={"url": "https://github.com/example", "order": 1})
        SocialLink.objects.get_or_create(settings=settings_obj, name="LinkedIn", defaults={"url": "https://linkedin.com/in/example", "order": 2})

        AboutSection.objects.get_or_create(
            title="About Me",
            defaults={"content": "<p>I ship clean, scalable products and lead engineering initiatives.</p>"},
        )

        backend, _ = SkillCategory.objects.get_or_create(name="Backend", defaults={"order": 1})
        frontend, _ = SkillCategory.objects.get_or_create(name="Frontend", defaults={"order": 2})

        for category, entries in [
            (backend, [("Django", 95), ("PostgreSQL", 90), ("Redis", 80)]),
            (frontend, [("Tailwind CSS", 88), ("JavaScript", 86), ("HTMX", 78)]),
        ]:
            for idx, (name, level) in enumerate(entries, start=1):
                Skill.objects.get_or_create(category=category, name=name, defaults={"level": level, "order": idx})

        Experience.objects.get_or_create(
            company="Nimbus Labs",
            role="Senior Django Engineer",
            start_date=date(2021, 5, 1),
            defaults={"responsibilities": "Architected backend services\nMentored engineers\nImproved CI/CD", "order": 1},
        )
        Education.objects.get_or_create(
            institution="State University",
            degree="BSc Computer Science",
            start_date=date(2014, 1, 1),
            end_date=date(2018, 1, 1),
            defaults={"description": "Focused on software engineering and databases.", "order": 1},
        )

        for idx, title in enumerate(["Web Development", "API Architecture", "Technical Consulting"], start=1):
            Service.objects.get_or_create(title=title, defaults={"description": f"Professional {title.lower()} service.", "order": idx})

        for idx, person in enumerate(["Olivia Stone", "Michael Reed"], start=1):
            Testimonial.objects.get_or_create(
                name=person,
                defaults={"role": "Product Manager", "company": "Acme Inc", "quote": "Outstanding delivery and communication.", "featured": True, "order": idx},
            )

        tags = [ProjectTag.objects.get_or_create(name=t)[0] for t in ["Django", "PostgreSQL", "Tailwind", "Docker"]]

        for idx in range(1, 7):
            project, _ = Project.objects.get_or_create(
                title=f"Portfolio Project {idx}",
                defaults={
                    "description": f"<p>Project {idx} solves a real business problem with Django.</p>",
                    "featured": idx <= 3,
                    "order": idx,
                    "status": Project.Status.PUBLISHED,
                    "published_at": timezone.now(),
                    "live_url": "https://example.com",
                    "github_url": "https://github.com/example/repo",
                },
            )
            project.tech_stack.set(random.sample(tags, k=min(2, len(tags))))
            ProjectImage.objects.get_or_create(project=project, caption="Dashboard", defaults={"order": 1})

        blog_tags = [BlogTag.objects.get_or_create(name=t)[0] for t in ["Django", "Career", "Engineering"]]
        for idx in range(1, 4):
            post, _ = BlogPost.objects.get_or_create(
                title=f"Engineering Note {idx}",
                defaults={
                    "content": "<p>Practical lessons from shipping Django in production.</p>",
                    "status": BlogPost.Status.PUBLISHED,
                    "published_at": timezone.now(),
                    "meta_description": "A practical engineering article.",
                },
            )
            post.tags.set(blog_tags[:2])

        ContactMessage.objects.get_or_create(
            email="visitor@example.com",
            subject="Project Inquiry",
            defaults={"name": "Sample Visitor", "message": "I would like to work with you."},
        )

        self.stdout.write(self.style.SUCCESS("Portfolio demo content seeded successfully."))

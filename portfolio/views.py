from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from blog.models import BlogPost
from core.models import AboutSection, Education, Experience, Service, SkillCategory, Testimonial

from .models import Project


class HomeView(TemplateView):
    template_name = "portfolio/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "featured_projects": Project.objects.published().filter(featured=True)[:6],
                "latest_posts": BlogPost.objects.published()[:3],
                "testimonials": Testimonial.objects.filter(featured=True)[:6],
                "services": Service.objects.all(),
                "meta_title": "Home",
                "meta_description": "Professional portfolio showcasing projects and experience.",
            }
        )
        return context


class AboutView(TemplateView):
    template_name = "portfolio/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "about": AboutSection.objects.first(),
                "skill_categories": SkillCategory.objects.prefetch_related("skills"),
                "experiences": Experience.objects.all(),
                "educations": Education.objects.all(),
                "meta_title": "About",
                "meta_description": "About my background, skills, and experience.",
            }
        )
        return context


class ProjectListView(ListView):
    model = Project
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"
    paginate_by = 6

    def get_queryset(self):
        return Project.objects.published().prefetch_related("tech_stack")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_title"] = "Projects"
        context["meta_description"] = "Browse published projects and case studies."
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.published().prefetch_related("tech_stack", "gallery_images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["meta_title"] = project.meta_title or project.title
        context["meta_description"] = project.meta_description or project.title
        context["og_type"] = "article"
        return context


def project_api_list(request):
    projects = Project.objects.published().prefetch_related("tech_stack")
    data = [
        {
            "title": p.title,
            "slug": p.slug,
            "description": p.meta_description,
            "featured": p.featured,
            "published_at": p.published_at,
            "live_url": p.live_url,
            "github_url": p.github_url,
            "tags": [tag.name for tag in p.tech_stack.all()],
        }
        for p in projects
    ]
    return JsonResponse({"count": len(data), "results": data})


def project_api_detail(request, slug):
    project = get_object_or_404(Project.objects.published().prefetch_related("tech_stack", "gallery_images"), slug=slug)
    data = {
        "title": project.title,
        "slug": project.slug,
        "description": project.description,
        "featured": project.featured,
        "published_at": project.published_at,
        "live_url": project.live_url,
        "github_url": project.github_url,
        "tags": [tag.name for tag in project.tech_stack.all()],
        "gallery": [
            {
                "caption": image.caption,
                "image": image.image.url if image.image else "",
            }
            for image in project.gallery_images.all()
        ],
    }
    return JsonResponse(data)

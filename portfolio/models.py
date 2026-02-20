from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from core.fields import RichTextField
from core.models import TimeStampedModel


class ProjectTag(TimeStampedModel):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Project.Status.PUBLISHED, published_at__lte=timezone.now())


class Project(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    featured_image = models.ImageField(upload_to="projects/featured/", blank=True, null=True)
    description = RichTextField()
    tech_stack = models.ManyToManyField(ProjectTag, blank=True, related_name="projects")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)

    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ["order", "-published_at", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="projects/gallery/", blank=True, null=True)
    caption = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Gallery image for {self.project.title}"

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from core.fields import RichTextField
from core.models import TimeStampedModel


class BlogTag(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=BlogPost.Status.PUBLISHED, published_at__lte=timezone.now())


class BlogPost(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    cover_image = models.ImageField(upload_to="blog/covers/", blank=True, null=True)
    content = RichTextField()
    tags = models.ManyToManyField(BlogTag, blank=True, related_name="posts")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=200, blank=True)

    objects = BlogPostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

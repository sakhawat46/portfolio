from django.core.exceptions import ValidationError
from django.db import models

from .fields import RichTextField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(TimeStampedModel):
    site_name = models.CharField(max_length=120)
    tagline = models.CharField(max_length=220, blank=True)
    short_bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to="site/profile/", blank=True, null=True)
    resume_pdf = models.FileField(upload_to="site/resume/", blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)
    copyright_text = models.CharField(max_length=180, blank=True)
    default_meta_description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.site_name or "Site settings"

    def clean(self):
        if self.pk:
            return
        if SiteSettings.objects.exists():
            raise ValidationError("Only one SiteSettings instance is allowed.")


class SocialLink(TimeStampedModel):
    settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name="social_links")
    name = models.CharField(max_length=40)
    url = models.URLField()
    icon_class = models.CharField(max_length=60, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class AboutSection(TimeStampedModel):
    title = models.CharField(max_length=120, default="About Me")
    content = RichTextField()

    def __str__(self):
        return self.title


class SkillCategory(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.name


class Skill(TimeStampedModel):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=80)
    level = models.PositiveSmallIntegerField(default=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category__order", "order", "name"]
        unique_together = ("category", "name")

    def __str__(self):
        return f"{self.name} ({self.level}%)"


class Experience(TimeStampedModel):
    company = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    responsibilities = models.TextField(help_text="Use line breaks for bullet points.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-start_date", "order"]

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Education(TimeStampedModel):
    institution = models.CharField(max_length=160)
    degree = models.CharField(max_length=160)
    field_of_study = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-start_date", "order"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Service(TimeStampedModel):
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=60, blank=True, help_text="Example: heroicons or custom icon class.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    quote = models.TextField()
    avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

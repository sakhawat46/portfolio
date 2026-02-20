from django.contrib import admin

from .admin_utils import SingletonModelAdminMixin
from .models import (
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


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdminMixin, admin.ModelAdmin):
    list_display = ("site_name", "email", "phone", "location", "updated_at")
    inlines = [SocialLinkInline]


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    search_fields = ("name",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "order")
    list_filter = ("category",)
    list_editable = ("level", "order")
    search_fields = ("name", "category__name")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("company", "role", "start_date", "end_date", "order")
    list_filter = ("start_date", "end_date")
    list_editable = ("order",)
    search_fields = ("company", "role", "responsibilities")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institution", "degree", "start_date", "end_date", "order")
    list_filter = ("start_date", "end_date")
    list_editable = ("order",)
    search_fields = ("institution", "degree", "field_of_study")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    search_fields = ("title", "description")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "company", "featured", "order")
    list_filter = ("featured",)
    list_editable = ("featured", "order")
    search_fields = ("name", "role", "company", "quote")

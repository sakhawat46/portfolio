from django.contrib import admin

from .models import Project, ProjectImage, ProjectTag


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "featured", "order", "published_at")
    list_filter = ("status", "featured", "published_at", "tech_stack")
    search_fields = ("title", "description", "meta_title", "meta_description")
    list_editable = ("featured", "order")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    filter_horizontal = ("tech_stack",)
    date_hierarchy = "published_at"

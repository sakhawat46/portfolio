from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path("projects/<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("api/projects/", views.project_api_list, name="project_api_list"),
    path("api/projects/<slug:slug>/", views.project_api_detail, name="project_api_detail"),
]

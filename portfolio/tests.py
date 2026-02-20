from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Project


class ProjectViewsTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Demo Project",
            description="<p>Demo</p>",
            status=Project.Status.PUBLISHED,
            published_at=timezone.now(),
        )

    def test_project_list(self):
        response = self.client.get(reverse("portfolio:project_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demo Project")

    def test_project_detail(self):
        response = self.client.get(reverse("portfolio:project_detail", kwargs={"slug": self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demo Project")

from django.views.generic import DetailView, ListView

from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return BlogPost.objects.published().prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_title"] = "Blog"
        context["meta_description"] = "Insights about Django, architecture, and product engineering."
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.published().prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context["meta_title"] = post.meta_title or post.title
        context["meta_description"] = post.meta_description or post.title
        context["og_type"] = "article"
        return context

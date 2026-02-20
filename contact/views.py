from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactMessageForm


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactMessageForm
    success_url = reverse_lazy("contact:success")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_title"] = "Contact"
        context["meta_description"] = "Send a project inquiry or collaboration request."
        return context


class ContactSuccessView(TemplateView):
    template_name = "contact/success.html"

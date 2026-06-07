from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page to verify Module 1 project setup."""
    template_name = 'home.html'

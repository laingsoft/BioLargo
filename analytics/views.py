from django.shortcuts import render
from .tools_settings import TOOLS


def analytics_page(request):
    return render(request, 'analytics/analytics.html', {'tools': TOOLS})

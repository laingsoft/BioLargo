from django.shortcuts import render


def analytics_page(request):
    return render(request, 'analytics/analytics.html', {})

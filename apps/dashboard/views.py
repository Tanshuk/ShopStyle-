from django.shortcuts import render
def dashboard_home_view(request):
    return render(request, 'placeholder.html', {'title': 'Admin Dashboard'})
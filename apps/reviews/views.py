from django.shortcuts import render
def review_list_view(request):
    return render(request, 'placeholder.html', {'title': 'Reviews'})
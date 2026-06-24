from django.shortcuts import render


def home_view(request):
    """
    Home page view.
    Context is populated further in Step 4 (Products) when we have real data.
    """
    context = {
        'page_title': 'Home',
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    return render(request, 'core/about.html', {'page_title': 'About Us'})


def contact_view(request):
    return render(request, 'core/contact.html', {'page_title': 'Contact'})


def placeholder_view(request):
    """
    Temporary view used for pages not yet implemented.
    Replace each one as we build each step.
    """
    return render(request, 'placeholder.html')
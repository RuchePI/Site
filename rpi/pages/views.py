from django.shortcuts import render


def home(request):
    """
    Display the home page with the last data.
    """
    return render(request, 'home.html')

from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Render the index page.
    """
    return render(request, 'frontend/index.html')


def seqfetch(request):
    """
    Render the sequence fetch page.
    """
    return render(request, 'frontend/seq_fetch.html')
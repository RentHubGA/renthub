from django.shortcuts import render

from .forms import ReviewForm
# Create your views here.

def home(request):
    return render(request, 'home.html')

def reviewform(request):
    review_form = ReviewForm
    return render(request, 'review_form.html', {
        'review_form': review_form
    })
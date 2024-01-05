from django.shortcuts import render
from django.http import HttpResponse


posts = [
  {
    'author': 'Samin',
    'title': 'Comback',
    'content': 'all',
    'date-posted': 'August',
  },
  {
    'author': 'Sarker',
    'title': 'Yes',
    'content': 'everything',
    'date-posted': 'june',
  }
]

def home(request):
  context = {
    'posts': posts,
  }
  return render(request, 'core/home.html', context)


def about(request):
  return render(request, 'core/about.html')
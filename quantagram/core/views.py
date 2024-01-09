from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import FoodSearchForm, SearchForm
import requests
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


def budget(request):
  return render(request, 'core/budget.html')


def meal(request):
  if request.method == 'POST':
    form = FoodSearchForm(request.POST)
    if form.is_valid():
      food_name = form.cleaned_data['food_name']
      food_info = get_food_information(food_query=food_name)

      context = {
        'form': form,
        'food_info': food_info,
      }

      return render(request, 'core/meal.html', context)
  else:
      form = FoodSearchForm()

  context = {'form': form}
  return render(request, 'core/meal.html', context)


def search(request):
  if request.method == "POST":
    form = SearchForm(request.POST)

    if form.is_valid():
      name = form.cleaned_data['query']
      results = Post.objects.filter(author__username__icontains=name)

      context = {
        'form': form,
        'results': results,
      }
      
      return render(request, 'core/search.html', context)
  else:
      form = SearchForm()

  context = {'form': form}
  return render(request, 'core/search.html', context)



def get_food_information(food_query):
    base_url = "https://www.themealdb.com/api/json/v1/1/search.php?s="
    url = f"{base_url}{food_query}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


class PostListView(ListView):
  model = Post
  template_name = 'core/home.html'
  context_object_name = 'posts'
  ordering = ['-date_posted']
  paginate_by = 3

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Add the top 3 most recent posts to the context
    recent_posts = Post.objects.order_by('-date_posted')[:3]
    context['recent_posts'] = recent_posts

    return context

class PostDetailView(DetailView):
  model = Post
  template_name = 'core/detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'content']
  template_name = 'core/create.html'

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content']
  template_name = 'core/create.html'

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'core/delete.html'
  success_url = '/'

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
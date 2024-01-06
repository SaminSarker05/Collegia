from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

def home(request):
  context = {
    'posts': Post.objects.all()
  }
  return render(request, 'core/home.html', context)

def about(request):
  return render(request, 'core/about.html')

class PostListView(ListView):
  model = Post
  template_name = 'core/home.html'
  context_object_name = 'posts'
  ordering = ['-date_posted']


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


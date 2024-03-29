from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from core.models import Post

def register(request):
  if request.method == "POST":
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account created. You can now login')
      return redirect('login')

  else:
    form = UserRegisterForm() 
  return render(request, 'users/register.html', {'form':form})

@login_required
def settings(request):
  if request.method == "POST":
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid:
      u_form.save()
      p_form.save()
      messages.success(request, f'Account updated')
      return redirect('settings')

  
  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'p_form':p_form,
    'u_form':u_form,
  }
  return render(request, 'users/settings.html', context)


@login_required
def profile(request):
  context = {
    'posts': Post.objects.filter(author__username__icontains=request.user)
  }
  return render(request, 'users/profile.html', context)

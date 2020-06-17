from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *

@login_required(login_url='login')
def home(request):

    return render(request, 'app/dashboard.html')

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				
				group = Group.objects.get(name='Instructor')
				user.groups.add(group)
				
				Staff.objects.create(
					user=user,
					name=user.username,
				)
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'app/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')
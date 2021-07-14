from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm, ProfileImageUpdateForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")
            return redirect("user-login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

@login_required
def userprofile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST,
                                   instance=request.user)
        propic_form = ProfileImageUpdateForm(request.POST,
                                             request.FILES,
                                             instance=request.user.profile)
        if user_form.is_valid() and propic_form.is_valid():
            user_form.save()
            propic_form.save()
            messages.success(request, "Account information is successfully updated!")
            return redirect("user-profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        propic_form = ProfileImageUpdateForm(instance=request.user.profile)

    context = {
        "user_form":user_form,
        "propic_form":propic_form
    }

    return render(request, "users/profile.html", context)
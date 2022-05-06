from django.contrib.auth import authenticate, logout, login
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.models import User
from communicationSystem.views import list_group
from django.contrib import messages
from myApp.models import Profile
import re


def home_student(request):
    groups = list_group(request.user)

    params = {"groups": groups}
    return render(request, 'nav/home_students.html', params)


def home_staff(request):
    groups = list_group(request.user)

    messages.add_message(request, messages.INFO, "Search for enrollment year to query results.")

    branches = Profile.objects.values("branch").distinct()
    branches_dict = get_branches(branches)

    params = {"search": "false", "branches": branches_dict, "groups": groups}
    return render(request, 'nav/home_professors.html', params)


def search(request):
    if request.method == "POST":
        year = request.POST.get("year")
        roll_no = request.POST.get("rollNo")

        if len(year) != 0:
            year = year + " - " + str(int(year) + 4)

            branches = Profile.objects.filter(batch=year).values("branch").distinct()
            branches_dict = get_branches(branches)

            groups = list_group(request.user)

            params = {"search": year, "branches": branches_dict, "groups": groups}
            return render(request, "nav/home_professors.html", params)

        elif len(roll_no) != 0:
            return redirect('ShowTable', slug=str(roll_no))

    return HttpResponse("404")


def branch_n_year(request, slug1, slug2):
    groups = list_group(request.user)

    students = Profile.objects.filter(batch=slug1, branch=slug2).order_by('user__username')

    params = {"students": students, "groups": groups}
    return render(request, 'myApp/adminSide.html', params)


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("rollNo")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Username or Password")
            return redirect("SignIn")

        login(request, user)

        if user.is_staff:
            return redirect('HomeStaff')

        return redirect('HomeStudent')

    return render(request, 'nav/signIn.html')


def sign_up(request):
    if request.method == "POST":
        bvp_id = request.POST.get("bvpId")
        username = request.POST.get("rollNo")
        first_name = request.POST.get("fName")
        last_name = request.POST.get("lName")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPass")

        if bvp_id is None or username is None or first_name is None or last_name is None or password is None or confirm_password is None:
            return HttpResponse("Error")

        if not re.search('bvp.edu.in', bvp_id):
            return HttpResponse("Error")

        if password != confirm_password:
            return HttpResponse("Error")

        user = User.objects.create_user(username, bvp_id, password)
        user.first_name = first_name.capitalize()
        user.last_name = last_name.capitalize()
        user.save()

        return redirect('SignIn')

    return render(request, 'nav/signUp.html')


def sign_out(request):
    logout(request)

    return redirect('Main')


# Utility functions

def get_branches(branches):
    branches_dict = {"CSE": [], "IT": [], "ECE": [], "EEE": []}

    for i in range(len(branches)):
        if re.search("(CSE-[0-9])", branches[i]['branch']):
            branches_dict["CSE"].append(branches[i]['branch'])

        elif re.search("(IT-[0-9])", branches[i]['branch']):
            branches_dict["IT"].append(branches[i]['branch'])

        elif re.search("(ECE-[0-9])", branches[i]['branch']):
            branches_dict["ECE"].append(branches[i]['branch'])

        elif re.search("(EEE-[0-9])", branches[i]['branch']):
            branches_dict["EEE"].append(branches[i]['branch'])

    return branches_dict

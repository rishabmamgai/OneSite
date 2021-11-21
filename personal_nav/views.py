from django.contrib.auth import authenticate, logout, login
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.models import User, Group
from communicationSystem.views import list_group
from personal_nav.templatetags import extras1
from django.contrib import messages
from myApp.models import Profile
import re


def home_student(request):
    groups = list_group(request.user)
    params = {"groups": groups}

    return render(request, 'nav/home_students.html', params)


def home_staff(request):
    messages.add_message(request, messages.INFO, "Search for enrollment year to query results.")
    branches = Profile.objects.values("branch").distinct()
    branches_dict = get_branches(branches)

    groups = query_groups(request.user)
    params = {"search": "false", "branches": branches_dict, "groups": groups}

    return render(request, 'nav/home_professors.html', params)


def search(request):
    if request.method == "POST":
        year = request.POST.get("year")
        rollNo = request.POST.get("rollNo")

        if len(year) != 0:
            print(1)
            year = year + " - " + str(int(year) + 4)

            branches = Profile.objects.filter(batch=year).values("branch").distinct()
            branches_dict = get_branches(branches)

            groups = query_groups(request.user)

            params = {"search": year, "branches": branches_dict, "groups": groups}

            return render(request, "nav/home_professors.html", params)

        elif len(rollNo) != 0:
            return redirect('showTable', slug=str(rollNo))

    return HttpResponse("404")


def branch_n_year(request, slug1, slug2):
    students = Profile.objects.filter(batch=slug1, branch=slug2).order_by('user__username')

    groups = query_groups(request.user)
    myArgs = {"students": students, "groups": groups}

    return render(request, 'myApp/adminSide.html', myArgs)


def signIn(request):
    if request.method == "POST":
        username = request.POST.get("rollNo")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Username or Password")
            return redirect("signIn")

        login(request, user)

        if user.is_staff:
            return redirect('HomeStaff')

        return redirect('HomeStudent')

    return render(request, 'nav/signIn.html')


def signUp(request):
    if request.method == "POST":
        BVPid = request.POST.get("bvpId")
        username = request.POST.get("rollNo")
        fname = request.POST.get("fName")
        lname = request.POST.get("lName")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPass")

        if BVPid == None or username == None or fname == None or lname == None or password == None or confirm_password == None:
            return HttpResponse("Error")

        if not re.search('bvp.edu.in', BVPid):
            return HttpResponse("Error")

        if password != confirm_password:
            return HttpResponse("Error")

        user = User.objects.create_user(username, BVPid, password)
        user.first_name = fname.capitalize()
        user.last_name = lname.capitalize()
        user.save()

        return redirect('signIn')

    return render(request, 'nav/signUp.html')


def signOut(request):
    logout(request)

    return redirect('Main')


# Utility functions

def query_groups(user):
    """
        Queries groups in which user is a member
    """

    groups = list_group(user)
    return groups


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

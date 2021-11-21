from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.models import User, Group
from django.core.serializers import serialize
from .models import Assignment, Submission
from django.conf import settings
from myApp.models import Profile
import os


def create_group(request):
    """
        Professors can create groups with a branch for a specific batch and post assignments.
        Students can submit and view their submissions.
    """

    if request.method == "POST":
        group_name = request.POST.get('group_name')
        branch = request.POST.get('branch')
        batch = request.POST.get('batch')

        group = Group()
        group.name = group_name
        group.save()

        group = Group.objects.get(name=group_name)
        profiles = Profile.objects.filter(branch=branch, batch=f"{batch} - {int(batch)+4}")

        admin = request.user
        admin.groups.add(group)
        group.save()
        
        members = [admin]
        for profile in profiles:
            user = profile.user
            user.groups.add(group)
            user.save()
            members.append(user)

        params = {"groupName": group_name, "members": members}

        return render(request, 'communicationSystem/group.html', params)


def get_group(request, slug):
    """
        View group users, posted assignments and submissions.
    """

    groups = list_group(request.user)
    members = User.objects.filter(groups__name=slug)
    assignments = Assignment.objects.filter(group__name=slug)
    submissions = Submission.objects.filter(submittedBy=request.user.username, assignment__in=assignments)

    js_dict = serialize("json", assignments)
    params = {"groupName": slug, "members": members, "assignments": assignments, "js_dict": js_dict,
              "submissions": submissions, "groups": groups}

    return render(request, 'communicationSystem/group.html', params)


def submit_assign(request, slug1):
    """
        Submit assignment.
    """
    if request.method == "POST":
        submitted_by = request.user.username
        assignment_topic = slug1
        submission = request.FILES["assigned_work"]

        assignment = Assignment.objects.filter(topic=assignment_topic)

        submit = Submission(assignment=assignment[0], submission=submission, submittedBy=submitted_by)
        submit.save()

    return redirect(request.GET["next"])


def display_submitted_assign(request, slug):
    """
        View submitted assignments to students.
    """

    file_loc = os.getcwd() + settings.MEDIA_URL + "communicationSystem/assignmentsSubmitted/" + slug
    file_loc = file_loc.replace('/', '\\').replace('\\', r'\\')

    with open(file_loc, 'rb') as pdfFile:
        response = HttpResponse(pdfFile.read(), content_type='application/pdf')
        response['Content_Disposition'] = f'filename={file_loc}'

    return response


# Utility function

def list_group(user):
    groups = user.groups.all()
    return groups

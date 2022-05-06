from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.models import User, Group
from .models import Assignment, Submission
from myApp.models import Profile


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
    members = User.objects.filter(groups__name=slug).order_by('username')

    assignments = Assignment.objects.filter(group__name=slug)
    submitted_assignments = []

    for assignment in assignments:
        submission = Submission.objects.filter(assignment=assignment, submittedBy=request.user.username)

        if len(submission) != 0:
            submitted_assignments.append({"assign": assignment, "sub": submission[0]})

        else:
            submitted_assignments.append({"assign": assignment, "sub": "not submitted"})

    params = {"groupName": slug, "assignments": submitted_assignments, "groups": groups, "members": members}

    return render(request, 'communicationSystem/group.html', params)


def create_assignment(request, slug):
    """
        Creates assignment.
    """

    if request.method == "POST":
        topic = request.POST.get('topic')
        due_date = request.POST.get('dueDate')
        description = request.POST.get('description')
        file = request.POST.get('file')

        group = Group.objects.filter(name=slug)
        assign = Assignment(group=group[0], topic=topic, dueDate=due_date, description=description, file=file)
        assign.save()

        return redirect('GetGroup', slug=slug)


def submit_assign(request, slug, slug1):
    """
        Submit assignment.
    """

    if request.method == "POST":
        file = request.FILES['assignFile']

        assignment = Assignment.objects.filter(topic=slug1, group__name=slug)
        submission = Submission.objects.filter(assignment=assignment[0], submittedBy=request.user.username)

        if len(submission) != 0:
            submission.delete()

        Submission(assignment=assignment[0], submission=file, submittedBy=request.user.username).save()

    return redirect('GetGroup', slug=slug)


def view_assignments(request, slug, slug1):
    """
        Professors can check the submissions done for the assignments.
    """

    groups = list_group(request.user)
    submissions = Submission.objects.filter(assignment__group__name=slug, assignment__topic=slug1).order_by('submittedBy')

    # Find students who submitted
    students_submitted = set()

    for submission in submissions:
        students_submitted.add(submission.submittedBy)

    # Find students who have not submitted
    members = User.objects.filter(groups__name=slug).order_by('username')
    not_submitted = []

    for member in members:
        if member.username not in students_submitted and not member.is_superuser:
            not_submitted.append(member.username)

    count_submissions = Submission.objects.filter(assignment__group__name=slug, assignment__topic=slug1).values('submittedBy').distinct().count()
    count_members = User.objects.filter(groups__name=slug).count()
    super_users = User.objects.filter(groups__name=slug, is_superuser=True).count()

    params = {"groupName": slug, "groups": groups, "submissions": submissions, "not_submitted": not_submitted,
              "count_submitted": count_submissions, "count_not_submitted": count_members-count_submissions - super_users}

    return render(request, 'communicationSystem/viewSubmissions.html', params)


def display_submitted_assign(request, slug):
    """
        View submitted assignments to students.
    """

    file_path = Submission.objects.filter(id=slug)[0].submission.path

    with open(file_path, 'rb') as pdfFile:
        response = HttpResponse(pdfFile.read(), content_type='application/pdf')
        response['Content_Disposition'] = f'filename={file_path}'

    return response


# Utility function

def list_group(user):
    groups = user.groups.all()
    return groups

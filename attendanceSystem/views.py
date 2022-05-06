from django.http import HttpResponse, JsonResponse
from communicationSystem.views import list_group
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Attendance
from datetime import datetime
import pyqrcode


def show_attendance(request, slug):
    groups = list_group(request.user)

    roll_no = ("00"+str(slug)) if (len(str(slug)) == 9) else ("0"+str(slug))
    attendance = Attendance.objects.filter(rollNo=roll_no)

    dates_attended = {}
    for obj in attendance:
        month = int(obj.date.split("-")[1])
        date = int(obj.date.split("-")[2])

        if month not in dates_attended.keys():
            dates_attended[month] = []

        dates_attended.get(month).append(date)

    params = {"attendance": dates_attended, "groups": groups}
    return render(request, "attendanceSystem/attendance.html", params)


def generate_qr(request):
    groups = list_group(request.user)

    if request.user.is_authenticated:
        roll_no = request.user.username

        date_time = str(datetime.today())
        date = date_time.split()[0]

        encoding_data = f"{roll_no} {date}"

    else:
        return HttpResponse("Error")

    # Generate QR code
    url = pyqrcode.create(encoding_data)

    # Create and save the png file
    url.png(f"D:\\Django_projects\\Ex1\\personal_nav\\static\\attendanceSystem\\{roll_no}.png", scale=6)

    student = User.objects.filter(username=request.user.username)[0]
    name = student.first_name + " " + student.last_name

    params = {"studentName": name, "date": datetime.today(), "groups": groups}

    return render(request, "attendanceSystem/qr-code.html", params)


def scanner(request):
    groups = list_group(request.user)

    params = {"groups": groups}
    return render(request, "attendanceSystem/scanner.html", params)


def scanner_results(request):
    attendees = request.GET.get("results")

    return JsonResponse({"students": len(attendees), "status": 200})

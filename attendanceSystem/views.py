from django.http import HttpResponse, JsonResponse
from communicationSystem.views import list_group
from django.shortcuts import render
from .models import Attendance
from datetime import datetime
import pyqrcode


def show_attendance(request, slug):
    groups = list_group(request.user)

    attendance = Attendance.objects.filter(rollNo="00"+str(slug))

    print(attendance[3].date)
    return HttpResponse("in")


def generate_qr(request):
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

    return render(request, "attendanceSystem/qr-code.html")


def scanner(request):
    groups = list_group(request.user)

    params = {"groups": groups}
    return render(request, "attendanceSystem/scanner.html", params)


def scanner_results(request):
    attendees = request.GET.get("results")
    print(attendees)

    return JsonResponse({"students": len(attendees), "status": 200})

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime
from .models import Attendance
from pyqrcode import QRCode
from pyzbar import pyzbar
import pyqrcode
import cv2, png


def showattendance(request, slug):
    attendance = Attendance.objects.filter(rollNo="00"+str(slug))
    print(attendance[3].date)
    return HttpResponse("in")


def generate_qr(request):
    # String which represents the QR code
    if request.user.is_authenticated:
        rollNo = request.user.username

        date_time = str(datetime.today())
        date = date_time.split()[0]

        encoding_data = f"{rollNo} {date}"

    else:
        return HttpResponse("Error")

    # Generate QR code
    url = pyqrcode.create(encoding_data)

    # Create and save the png file naming "myqr.png"
    url.png(f"D:\\Django_projects\\Ex1\\personal_nav\\static\\attendanceSystem\\{rollNo}.png", scale=6)

    return render(request, "attendanceSystem/qr-code.html")


def scanner(request):
    flag = main()

    if flag == 0:
        qrcode_data = ""
        with open(r"D:\Django_projects\Ex1\personal_nav\attendanceSystem\barcode_result.txt", "r") as query:
            qrcode_data = query.readlines()

        rollNo = qrcode_data[0].split()[0]
        date = qrcode_data[0].split()[1]

        date_time = str(datetime.today())
        today = date_time.split()[0]
        print(rollNo, date)
        if date == today:
            Attendance(rollNo=rollNo, date=date).save()
            return redirect('Scanner')

        else:
            print(rollNo, date)
            return HttpResponse("Error")

    else:
        return HttpResponse("Done")


def main():
    # 1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    # 2
    flag = 0
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        if cv2.waitKey(1) == 8:
            flag = 1
            break
    # 3
    camera.release()
    cv2.destroyAllWindows()

    return flag


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        # 1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        # 3
        with open(r"D:\Django_projects\Ex1\personal_nav\attendanceSystem\barcode_result.txt", mode='w') as file:
            file.write(barcode_info)

    return frame

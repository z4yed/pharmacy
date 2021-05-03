import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from attendance.models import Attendance
from employee.models import Employee


class AddAttendanceView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        employees = Employee.objects.filter(is_active=True)

        context = {
            'employees': employees,
        }

        return render(request, 'attendance/add_attendance.html', context)

    def post(self, request):
        data = request.POST
        employee_id = data.get('employee_id')
        employee_obj = Employee.objects.get(id=employee_id)

        date = data.get('date')
        date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17

        sign_in_time = data.get('sign_in')

        obj = Attendance(employee=employee_obj, date=date, sign_in_time=sign_in_time)
        obj.signed_in = True
        obj.save()

        messages.success(request, 'Attendance Recorded Successfully. ')
        return redirect('attendance:attendance_list')


class AttendanceListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        attendances = Attendance.objects.filter(is_active=True)

        context = {
            'attendances': attendances,
        }

        return render(request, 'attendance/attendance_list.html', context)


class UpdateAttendanceView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, attendance_id):
        obj = Attendance.objects.get(id=attendance_id)

        sign_out_time = request.POST.get('sign_out')
        obj.signed_out = True
        obj.sign_out_time = sign_out_time
        obj.save()

        messages.success(request, "Signed Out Successfully. ")
        return redirect('attendance:attendance_list')


class RemoveAttendanceView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, attendance_id):
        obj = Attendance.objects.get(id=attendance_id)
        obj.is_active = False
        obj.save()

        messages.success(request, 'Attendance Removed Successfully. ')
        return redirect('attendance:attendance_list')


class AttendanceFilterView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = dict()
        employees = Employee.objects.filter(is_active=True)
        context['employees'] = employees
        return render(request, 'attendance/filtered_attendance.html', context)

    def post(self, request):
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date:
            from_date = datetime.datetime.strptime(from_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17
        if to_date:
            to_date = datetime.datetime.strptime(to_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2020-12-17

        employee_id = request.POST.get('employee_id')
        employee_obj = Employee.objects.get(id=employee_id)

        attendances = Attendance.objects.filter(employee=employee_obj, is_active=True)
        if from_date:
            attendances = attendances.filter(date__gte=from_date)
        if to_date:
            attendances = attendances.filter(date__lte=to_date)

        employees = Employee.objects.filter(is_active=True)

        total_seconds = 0
        for attendance in attendances:
            total_seconds += attendance.get_duration_in_seconds

        hour = total_seconds // 3600
        seconds_left = total_seconds % 3600
        minute = seconds_left // 60
        second = seconds_left % 60

        hour = f"0{int(abs(hour))}" if hour < 10 else f"{int(abs(hour))}"
        minute = f"0{int(abs(minute))}" if minute < 10 else f"{int(abs(minute))}"
        second = f"0{int(abs(second))}" if second < 10 else f"{int(abs(second))}"

        total_duration = f"{hour}:{minute}:{second}"

        context = {
            'attendances': attendances,
            'employees': employees,
            'total_duration' : total_duration,
        }

        return render(request, 'attendance/filtered_attendance.html', context)
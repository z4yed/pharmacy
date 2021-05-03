import datetime

from django.db import models


class Attendance(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    sign_in_time = models.TimeField(null=True, blank=True)
    sign_out_time = models.TimeField(null=True, blank=True)

    signed_in = models.BooleanField(default=False)
    signed_out = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.employee.first_name

    @property
    def get_duration_in_seconds(self):
        if self.signed_out:
            in_hour = self.sign_in_time.hour
            in_minute = self.sign_in_time.minute
            in_seconds = self.sign_in_time.second

            out_hour = self.sign_out_time.hour
            out_minute = self.sign_out_time.minute
            out_second = self.sign_out_time.second

            in_time = "{}:{}:{}".format(in_hour, in_minute, in_seconds)
            out_time = "{}:{}:{}".format(out_hour, out_minute, out_second)
            in_time = datetime.datetime.strptime(in_time, "%H:%M:%S")  # '14:33:12'
            out_time = datetime.datetime.strptime(out_time, "%H:%M:%S")
            diff = out_time - in_time

            total_seconds = diff.total_seconds()

            return total_seconds
        else:
            return 0

    @property
    def total_stay_time(self):
        if not self.signed_out:
            return "--"
        else:
            total_seconds = self.get_duration_in_seconds
            # converting_total_seconds to HH:MM:SS and return as String
            hour = total_seconds // 3600
            seconds_left = total_seconds % 3600
            minute = seconds_left // 60
            second = seconds_left % 60

            hour = f"0{int(abs(hour))}" if hour < 10 else f"{int(abs(hour))}"
            minute = f"0{int(abs(minute))}" if minute < 10 else f"{int(abs(minute))}"
            second = f"0{int(abs(second))}" if second < 10 else f"{int(abs(second))}"

            return f"{hour}:{minute}:{second}"

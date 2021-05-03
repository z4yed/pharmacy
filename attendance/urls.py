from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('add-attendance/', views.AddAttendanceView.as_view(), name='add_attendance'),
    path('attendance-list/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('update-attendance/<int:attendance_id>/', views.UpdateAttendanceView.as_view(), name='update_attendance'),
    path('remove-attendance/<int:attendance_id>/', views.RemoveAttendanceView.as_view(), name='remove_attendance'),
    path('datewise-attendance-report/', views.AttendanceFilterView.as_view(), name='attendance_filter'),
]

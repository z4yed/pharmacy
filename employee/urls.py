from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('designation-list', views.DesignationList.as_view(), name='designation_list'),
    path('add-designation', views.AddDesignation.as_view(), name='add_designation'),
    path('update-designation/<int:designation_id>', views.UpdateDesignation.as_view(), name='update_designation'),
    path('remove-designation/<int:designation_id>', views.RemoveDesignation.as_view(), name='remove_designation'),

    path('employee-list', views.EmployeeList.as_view(), name='employee_list'),
    path('add-employee', views.AddEmployee.as_view(), name='add_employee'),
    path('update-employee/<int:employee_id>', views.UpdateEmployee.as_view(), name='update_employee'),
    path('remove-employee/<int:employee_id>', views.RemoveEmployee.as_view(), name='remove_employee'),
]

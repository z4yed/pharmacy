from django.urls import path
from . import views

app_name = 'expense'

urlpatterns = [

   # Expense Item
   path('expense-items/', views.ExpenseItemList.as_view(), name='expense_items'),
   path('add-expense-item/', views.AddExpenseItem.as_view(), name='add_expense_item'),
   path('update-expense-item/<int:item_id>', views.UpdateExpenseItem.as_view(), name='update_expense_item'),
   path('remove-expense-item/<int:item_id>', views.UpdateExpenseItem.as_view(), name='remove_expense_item'),

   # Expense
   path('expense-list/', views.ExpenseList.as_view(), name='expense_list'),
   path('add-expense/', views.AddExpense.as_view(), name='add_expense'),
   path('remove-expense/<int:expense_id>', views.UpdateExpense.as_view(), name='remove_expense'),  # get request

]

from django.urls import path
from . import views
from tim_app.views import TimeIsMoneygeView, TimeIsMoneygeListView, MorningView, EveningView, HourlyWageView, PaidLeaveView, GeneratePdfView

app_name = 'tim_app'
urlpatterns = [
	path('', TimeIsMoneygeView.as_view(), name='timeismoneyge'),
	path('user/<int:id>', TimeIsMoneygeListView.as_view(), name='timeismoneyge_list'),
	path('morning_add/<int:id>', MorningView.as_view(), name='morning_add'),
	path('evening_add/<int:id>', EveningView.as_view(), name='evening_add'),

	path('detail/<int:overtime_id>', views.detail, name='detail'),
	# path('detail/<int:id>', views.TimeIsMoneygeDetailView.as_view(), name='detail'),

	path('delete/<int:overtime_id>', views.delete, name='delete'),
	path('morning_edit/<int:overtime_id>', views.morning_edit, name='morning_edit'),
	path('evening_edit/<int:overtime_id>', views.evening_edit, name='evening_edit'),
	path('hourly_wage_add/<int:id>', HourlyWageView.as_view(), name='hourly_wage_add'),

	# path('generate_pdf', views.generate_pdf, name='generate_pdf'),
	path('generate_pdf/<int:id>', GeneratePdfView.as_view(), name='generate_pdf'),

	path('paid_leave/<int:id>', PaidLeaveView.as_view(), name='paid_leave'),
	path('paid_leave_delete/<int:paid_leave_id>', views.paid_leave_delete, name='paid_leave_delete'),
	]
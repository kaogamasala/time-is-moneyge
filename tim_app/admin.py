from django.contrib import admin
from .models import Time_is_moneyge, Hourly_wage, Paid_leave
# Register your models here.

class Time_is_moneygeAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'morning_word', 'start_datetime', 'morning_overtime', 'evening_word', 'end_datetime','evening_overtime', 'overtime', 'todays_overtime', 'working_time', 'user')
admin.site.register(Time_is_moneyge, Time_is_moneygeAdmin)

class Hourly_wageAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_datetime', 'hourly_wage', 'user')
admin.site.register(Hourly_wage, Hourly_wageAdmin)

class Paid_leaveAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_datetime', 'paid_leave_date', 'memo', 'user')
admin.site.register(Paid_leave, Paid_leaveAdmin)

#kaogamasala
#n_suehiro@hyojito.co.jp
#django20190204
#kaoga

#tarokimura@example.com
#django20190414
#django20190423

#cd ~/1pro/Django/timeismoneyge/
#python3 -m venv timeismoneyge_venv
#source timeismoneyge_venv/bin/activate
#python time_is_moneyge/manage.py runserver
#python time_is_moneyge/manage.py makemigrations
#python time_is_moneyge/manage.py migrate
#python time_is_moneyge/manage.py test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, F
import re
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .models import Time_is_moneyge, Hourly_wage, Paid_leave
from .forms import MorningForm, EveningForm, HourlyWageForm, PaidLeaveForm

from django.views import generic, View
from django.contrib import messages

"""weasyprint"""
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.template.loader import get_template

from itertools import chain #queryset結合
from operator import attrgetter #結合したquerysetをソート

class TimeIsMoneygeView(View):
	def get(self, request, *args, **kwargs):		
		return render(request, 'tim_app/main.html')

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.id == self.kwargs['id'] or user.is_superuser

class TimeIsMoneygeListView(LoginRequiredMixin, OnlyYouMixin, View):
	def get(self, request, *args, **kwargs):
		
		"""ユーザー検証"""
		login_user_id = str(self.request.user.id) #ログインしているユーザーのid
		print("ログインID",login_user_id)
		url_user_id = str(self.kwargs['id']) #urlのid
		print("URLID", url_user_id)
		if login_user_id == url_user_id:

			"""一覧データ取得"""
			morning_list = Time_is_moneyge.objects.filter(user=self.request.user).exclude(morning_overtime__exact = None).order_by('id') 
			evening_list = Time_is_moneyge.objects.filter(user=self.request.user).exclude(evening_overtime__exact = None).order_by('id') 
			
			#querysetの結合
			total_list = sorted(
			chain(morning_list, evening_list),
			key=attrgetter('date')) 
			
			"""現在の時給"""
			try:
				get_current_hourly_wage = Hourly_wage.objects.filter(user=self.request.user).order_by('created_datetime').last() #created_datetimeの日付でソートして最新の時給を取得
				current_hourly_wage_str = str(get_current_hourly_wage) #１行上の型（'tim_app.models.Hourly_wage'）はintに変換できないため、まずstrに変換
				current_hourly_wage = int(current_hourly_wage_str) #strからintに変換
			except:
				current_hourly_wage = 0
			
			"""今日の日付を取得"""
			today = datetime.today() 
			
			"""今月の残業時間"""
			if today.day > 10: #日付が1日から10日以外
				print(type(today.day))
				print(today.day)
				eleventh_of_thismonth = today + relativedelta(day=11) #今月の11日を取得
				print("今月", eleventh_of_thismonth)
				work_of_thismonth = Time_is_moneyge.objects.filter(date__range=(eleventh_of_thismonth, today), user=self.request.user) #11日から今日までのオブジェクトをログインユーザーで取得
				morning_overtime_of_thismonth = work_of_thismonth.aggregate(morning_overtime=Sum('morning_overtime')) #今月の朝の残業時間を集計
				evening_overtime_of_thismonth = work_of_thismonth.aggregate(evening_overtime=Sum('evening_overtime')) #今月の夜の残業時間を集計
				for moot_key, moot_value in morning_overtime_of_thismonth.items(): #keyとvalueに分ける
					morning_total_overtime = moot_value #valueを取得
					for eoot_key, eoot_value in evening_overtime_of_thismonth.items(): #keyとvalueに分ける
						evening_total_overtime = eoot_value #valueを取得
						try:
							total_overtime_of_thismonth = morning_total_overtime + evening_total_overtime #今月の残業時間合計を取得
							minutes, seconds = divmod(total_overtime_of_thismonth.seconds + total_overtime_of_thismonth.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
							hours, minutes = divmod(minutes, 60) #分を時と分に
							total_overtime_of_thismonth = '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds) 
						except:
							total_overtime_of_thismonth = 0
			#今日の日付が1日〜10日の場合
			else:
				eleventh_of_one_month_ago = today - relativedelta(months=1, day=11) #一月前の11日を取得
				print("ひと月前", eleventh_of_one_month_ago)
				work_of_thismonth = Time_is_moneyge.objects.filter(date__range=(eleventh_of_one_month_ago, today), user=self.request.user) #11日から今日までのオブジェクトをログインユーザーで取得
				morning_overtime_of_thismonth = work_of_thismonth.aggregate(morning_overtime=Sum('morning_overtime')) #今月の朝の残業時間を集計
				evening_overtime_of_thismonth = work_of_thismonth.aggregate(evening_overtime=Sum('evening_overtime')) #今月の夜の残業時間を集計
				for moot_key, moot_value in morning_overtime_of_thismonth.items(): #keyとvalueに分ける
					morning_total_overtime = moot_value #valueを取得
					for eoot_key, eoot_value in evening_overtime_of_thismonth.items(): #keyとvalueに分ける
						evening_total_overtime = eoot_value #valueを取得
						try:
							total_overtime_of_thismonth = morning_total_overtime + evening_total_overtime #今月の残業時間合計を取得
							minutes, seconds = divmod(total_overtime_of_thismonth.seconds + total_overtime_of_thismonth.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
							hours, minutes = divmod(minutes, 60) #分を時と分に
							total_overtime_of_thismonth = '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
							print(total_overtime_of_thismonth)
						except:
							total_overtime_of_thismonth = 0

			"""合計の残業金額"""
			try:
				total_overtime_of_thismonth_str = '.'.join(re.split('[,:]', str(total_overtime_of_thismonth))[0:2]) #timedeltaを文字列に変換。dayとsecondをsplit
				total_overtime_of_thismonth_float = float(total_overtime_of_thismonth_str) #str型をfloat型に変換
				total_overtime_amount = total_overtime_of_thismonth_float * current_hourly_wage #合計残業金額を取得
				total_overtime_amount = (Decimal(str(total_overtime_amount)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)) #四捨五入
			except:
				total_overtime_amount = 0

			"""今月の有給"""
			if today.day  > 10:
				eleventh_of_thismonth = today + relativedelta(day=11) #今月の11日を取得
				tenth_of_next_month = today + relativedelta(months=1, day=10) #次月の10日取得
				paid_leave_list = Paid_leave.objects.filter(user=self.request.user, paid_leave_date__range=(eleventh_of_thismonth, tenth_of_next_month)).order_by('paid_leave_date') 
			else:
				eleventh_of_one_month_ago = today - relativedelta(months=1, day=11) #一月前の11日を取得
				tenth_of_this_month = today + relativedelta(day=10) #今月の10日取得
				paid_leave_list = Paid_leave.objects.filter(user=self.request.user, paid_leave_date__range=(eleventh_of_one_month_ago, tenth_of_this_month)).order_by('paid_leave_date') 

			"""月別残業時間（棒グラフ）"""
			latest_year = today.year # 今年
			last_year = today.year - 1 # 去年
			
			# 1月
			lastdata_of_latest_january = Time_is_moneyge.objects.all().filter(date__month=1, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_january != None: # date__monthの最後のデータがNoneではない場合
				if lastdata_of_latest_january.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールの場合
					sort_january = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=1, user=self.request.user) #今年でソート
					sort_january = sort_january.aggregate(overtime=Sum('overtime'))
					for sort_january_key, sort_january_value in sort_january.items():
						sort_january = sort_january_value #valueを取得
						minutes, seconds = divmod(sort_january.seconds + sort_january.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_january = '{:d}:{:02d}'.format(hours, minutes)
						sort_january = '.'.join(re.split('[:]', str(sort_january)))
				else:
					sort_january = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=1, user=self.request.user) # 去年でソート
					sort_january = sort_january.aggregate(overtime=Sum('overtime'))
					for sort_january_key, sort_january_value in sort_january.items():
						sort_january = sort_january_value #valueを取得
						minutes, seconds = divmod(sort_january.seconds + sort_january.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_january = '{:d}:{:02d}'.format(hours, minutes)
						sort_january = '.'.join(re.split('[:]', str(sort_january)))
			else:
				sort_january = 0
			# 2月					
			lastdata_of_latest_february = Time_is_moneyge.objects.all().filter(date__month=2, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_february != None:
				if lastdata_of_latest_february.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら
					sort_february = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=2, user=self.request.user) # 今年でソート
					sort_february = sort_february.aggregate(overtime=Sum('overtime'))
					for sort_february_key, sort_february_value in sort_february.items():
						sort_february = sort_february_value #valueを取得
						minutes, seconds = divmod(sort_february.seconds + sort_february.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_february = '{:d}:{:02d}'.format(hours, minutes)
						sort_february = '.'.join(re.split('[:]', str(sort_february)))
				else:
					sort_february = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=2, user=self.request.user) # 去年でソート
					sort_february = sort_february.aggregate(overtime=Sum('overtime'))
					for sort_february_key, sort_february_value in sort_february.items():
						sort_february = sort_february_value #valueを取得
						minutes, seconds = divmod(sort_february.seconds + sort_february.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_february = '{:d}:{:02d}'.format(hours, minutes)
						sort_february = '.'.join(re.split('[:]', str(sort_february)))
			else:
				sort_february = 0
			# 3月
			lastdata_of_latest_march = Time_is_moneyge.objects.all().filter(date__month=3, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_march != None:
				if lastdata_of_latest_march.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら
					sort_march = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=3, user=self.request.user)
					sort_march = sort_march.aggregate(overtime=Sum('overtime'))
					for sort_march_key, sort_march_value in sort_march.items():
						sort_march = sort_march_value #valueを取得
						minutes, seconds = divmod(sort_march.seconds + sort_march.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_march = '{:d}:{:02d}'.format(hours, minutes)
						sort_march = '.'.join(re.split('[:]', str(sort_march)))
				else:
					sort_march = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=3, user=self.request.user)
					sort_march = sort_march.aggregate(overtime=Sum('overtime'))
					for sort_march_key, sort_march_value in sort_march.items():
						sort_march = sort_march_value #valueを取得
						minutes, seconds = divmod(sort_march.seconds + sort_march.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_march = '{:d}:{:02d}'.format(hours, minutes)
						sort_march = '.'.join(re.split('[:]', str(sort_march)))
			else:
				sort_march = 0
			# 4月
			lastdata_of_latest_april = Time_is_moneyge.objects.all().filter(date__month=4, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_april != None:
				if lastdata_of_latest_april.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら			
					sort_april = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=4, user=self.request.user)
					sort_april = sort_april.aggregate(overtime=Sum('overtime'))
					for sort_april_key, sort_april_value in sort_april.items(): #keyとvalueに分ける
						sort_april = sort_april_value #valueを取得
						minutes, seconds = divmod(sort_april.seconds + sort_april.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_april = '{:d}:{:02d}'.format(hours, minutes)
						sort_april = '.'.join(re.split('[:]', str(sort_april)))
				else:
					sort_april = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=4, user=self.request.user)
					sort_april = sort_april.aggregate(overtime=Sum('overtime'))
					for sort_april_key, sort_april_value in sort_april.items(): #keyとvalueに分ける
						sort_april = sort_april_value #valueを取得
						minutes, seconds = divmod(sort_april.seconds + sort_april.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_april = '{:d}:{:02d}'.format(hours, minutes)
						sort_april = '.'.join(re.split('[:]', str(sort_april)))
			else:
				sort_april = 0
			# 5月
			lastdata_of_latest_may = Time_is_moneyge.objects.all().filter(date__month=5, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_may != None:
				if lastdata_of_latest_may.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら
					sort_may = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=5, user=self.request.user)
					sort_may = sort_may.aggregate(overtime=Sum('overtime'))
					for sort_may_key, sort_may_value in sort_may.items(): #keyとvalueに分ける
						sort_may = sort_may_value #valueを取得
						minutes, seconds = divmod(sort_may.seconds + sort_may.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_may = '{:d}:{:02d}'.format(hours, minutes)
						sort_may = '.'.join(re.split('[:]', str(sort_may)))
				else:
					sort_may = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=5, user=self.request.user)
					sort_may = sort_may.aggregate(overtime=Sum('overtime'))
					for sort_may_key, sort_may_value in sort_may.items(): #keyとvalueに分ける
						sort_may = sort_may_value #valueを取得
						minutes, seconds = divmod(sort_may.seconds + sort_may.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_may = '{:d}:{:02d}'.format(hours, minutes)
						sort_may = '.'.join(re.split('[:]', str(sort_may)))
			else:
				sort_may = 0
			# 6月
			lastdata_of_latest_june = Time_is_moneyge.objects.all().filter(date__month=6, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_june != None:
				if lastdata_of_latest_june.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら				
					sort_june = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=6, user=self.request.user)
					sort_june = sort_june.aggregate(overtime=Sum('overtime'))
					for sort_june_key, sort_june_value in sort_june.items(): #keyとvalueに分ける
						sort_june = sort_june_value #valueを取得
						minutes, seconds = divmod(sort_june.seconds + sort_june.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_june = '{:d}:{:02d}'.format(hours, minutes)
						sort_june = '.'.join(re.split('[:]', str(sort_june)))
				else:
					sort_june = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=6, user=self.request.user)
					sort_june = sort_june.aggregate(overtime=Sum('overtime'))
					for sort_june_key, sort_june_value in sort_june.items(): #keyとvalueに分ける
						sort_june = sort_june_value #valueを取得
						minutes, seconds = divmod(sort_june.seconds + sort_june.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_june = '{:d}:{:02d}'.format(hours, minutes)
						sort_june = '.'.join(re.split('[:]', str(sort_june)))
			else:
				sort_june = 0
			# 7月
			lastdata_of_latest_july = Time_is_moneyge.objects.all().filter(date__month=7, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_july != None:
				if lastdata_of_latest_july.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら				
					sort_july = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=7, user=self.request.user)
					sort_july = sort_july.aggregate(overtime=Sum('overtime'))
					for sort_july_key, sort_july_value in sort_july.items(): #keyとvalueに分ける
						sort_july = sort_july_value #valueを取得
						minutes, seconds = divmod(sort_july.seconds + sort_july.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_july = '{:d}:{:02d}'.format(hours, minutes)
						sort_july = '.'.join(re.split('[:]', str(sort_july)))
				else:
					sort_july = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=7, user=self.request.user)
					sort_july = sort_july.aggregate(overtime=Sum('overtime'))
					for sort_july_key, sort_july_value in sort_july.items(): #keyとvalueに分ける
						sort_july = sort_july_value #valueを取得
						minutes, seconds = divmod(sort_july.seconds + sort_july.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_july = '{:d}:{:02d}'.format(hours, minutes)
						sort_july = '.'.join(re.split('[:]', str(sort_july)))
			else:
				sort_july = 0
			# 8月
			lastdata_of_latest_august = Time_is_moneyge.objects.all().filter(date__month=8, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_august != None:
				if lastdata_of_latest_august.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら						
					sort_august = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=8, user=self.request.user)
					sort_august = sort_august.aggregate(overtime=Sum('overtime'))
					for sort_august_key, sort_august_value in sort_august.items(): #keyとvalueに分ける
						sort_august = sort_august_value #valueを取得
						minutes, seconds = divmod(sort_august.seconds + sort_august.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_august = '{:d}:{:02d}'.format(hours, minutes)
						sort_august = '.'.join(re.split('[:]', str(sort_august)))
				else:
					sort_august = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=8, user=self.request.user)
					sort_august = sort_august.aggregate(overtime=Sum('overtime'))
					for sort_august_key, sort_august_value in sort_august.items(): #keyとvalueに分ける
						sort_august = sort_august_value #valueを取得
						minutes, seconds = divmod(sort_august.seconds + sort_august.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_august = '{:d}:{:02d}'.format(hours, minutes)
						sort_august = '.'.join(re.split('[:]', str(sort_august)))
			else:
				sort_august = 0		
			# 9月	
			lastdata_of_latest_september = Time_is_moneyge.objects.all().filter(date__month=9, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_september != None:
				if lastdata_of_latest_september.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら					
					sort_september = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=9, user=self.request.user)
					sort_september = sort_september.aggregate(overtime=Sum('overtime'))
					for sort_september_key, sort_september_value in sort_september.items(): #keyとvalueに分ける
						sort_september = sort_september_value #valueを取得
						minutes, seconds = divmod(sort_september.seconds + sort_september.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_september = '{:d}:{:02d}'.format(hours, minutes)
						sort_september = '.'.join(re.split('[:]', str(sort_september)))
				else:
					sort_september = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=9, user=self.request.user)
					sort_september = sort_september.aggregate(overtime=Sum('overtime'))
					for sort_september_key, sort_september_value in sort_september.items(): #keyとvalueに分ける
						sort_september = sort_september_value #valueを取得
						minutes, seconds = divmod(sort_september.seconds + sort_september.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_september = '{:d}:{:02d}'.format(hours, minutes)
						sort_september = '.'.join(re.split('[:]', str(sort_september)))
			else:
				sort_september = 0		
			# 10月	
			lastdata_of_latest_october = Time_is_moneyge.objects.all().filter(date__month=10, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_october != None:
				if lastdata_of_latest_october.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら			
					sort_october = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=10, user=self.request.user)
					sort_october = sort_october.aggregate(overtime=Sum('overtime'))
					for sort_october_key, sort_october_value in sort_october.items(): #keyとvalueに分ける
						sort_october = sort_october_value #valueを取得
						minutes, seconds = divmod(sort_october.seconds + sort_october.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_october = '{:d}:{:02d}'.format(hours, minutes)
						sort_october = '.'.join(re.split('[:]', str(sort_october)))
				else:
					sort_october = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=10, user=self.request.user)
					sort_october = sort_october.aggregate(overtime=Sum('overtime'))
					for sort_october_key, sort_october_value in sort_october.items(): #keyとvalueに分ける
						sort_october = sort_october_value #valueを取得
						minutes, seconds = divmod(sort_october.seconds + sort_october.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_october = '{:d}:{:02d}'.format(hours, minutes)
						sort_october = '.'.join(re.split('[:]', str(sort_october)))
			else:
				sort_october = 0	
			# 11月
			lastdata_of_latest_november = Time_is_moneyge.objects.all().filter(date__month=11, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_november != None:
				if lastdata_of_latest_november.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら		
					sort_november = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=11, user=self.request.user)
					sort_november = sort_november.aggregate(overtime=Sum('overtime'))
					for sort_november_key, sort_november_value in sort_november.items(): #keyとvalueに分ける
						sort_november = sort_november_value #valueを取得
						minutes, seconds = divmod(sort_november.seconds + sort_november.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_november = '{:d}:{:02d}'.format(hours, minutes)
						sort_november = '.'.join(re.split('[:]', str(sort_november)))
				else:
					sort_november = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=11, user=self.request.user)
					sort_november = sort_november.aggregate(overtime=Sum('overtime'))
					for sort_november_key, sort_november_value in sort_november.items(): #keyとvalueに分ける
						sort_november = sort_november_value #valueを取得
						minutes, seconds = divmod(sort_november.seconds + sort_november.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_november = '{:d}:{:02d}'.format(hours, minutes)
						sort_november = '.'.join(re.split('[:]', str(sort_november)))
			else:
				sort_november = 0
			# 12月
			lastdata_of_latest_december = Time_is_moneyge.objects.all().filter(date__month=12, user=self.request.user).last() # date__monthの最後のデータ
			if lastdata_of_latest_december != None:
				if lastdata_of_latest_december.date.year == today.year: # 最後のデータの年と今日の年を比較してイコールだったら
					sort_december = Time_is_moneyge.objects.all().filter(date__year=latest_year, date__month=12, user=self.request.user)
					sort_december = sort_december.aggregate(overtime=Sum('overtime'))
					for sort_december_key, sort_december_value in sort_december.items(): #keyとvalueに分ける
						sort_december = sort_december_value #valueを取得
						minutes, seconds = divmod(sort_december.seconds + sort_december.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_december = '{:d}:{:02d}'.format(hours, minutes)
						sort_december = '.'.join(re.split('[:]', str(sort_december)))
				else:
					sort_december = Time_is_moneyge.objects.all().filter(date__year=last_year, date__month=12, user=self.request.user)
					sort_december = sort_december.aggregate(overtime=Sum('overtime'))
					for sort_december_key, sort_december_value in sort_december.items(): #keyとvalueに分ける
						sort_december = sort_december_value #valueを取得
						minutes, seconds = divmod(sort_december.seconds + sort_december.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						sort_december = '{:d}:{:02d}'.format(hours, minutes)
						sort_december = '.'.join(re.split('[:]', str(sort_december)))
			else:
				sort_december = 0

			"""最新の登録"""
			last_register =  Time_is_moneyge.objects.filter(user=self.request.user).last()
				
			context = {
				'total_list':total_list,
				'morning_list': morning_list,
				'evening_list': evening_list,
				'total_overtime_of_thismonth': total_overtime_of_thismonth,
				'total_overtime_amount': total_overtime_amount,
				'current_hourly_wage': current_hourly_wage,
				'last_register': last_register,
				'sort_january': sort_january,
				'sort_february': sort_february,
				'sort_march': sort_march,
				'sort_april': sort_april,
				'sort_may': sort_may,
				'sort_june': sort_june,
				'sort_july': sort_july,
				'sort_august': sort_august,
				'sort_september': sort_september,
				'sort_october': sort_october,
				'sort_november': sort_november,
				'sort_december': sort_december,
				'paid_leave_list': paid_leave_list,	
				'today': today,
			}

			return render(request, 'tim_app/index.html', context)

		else:
			return render(request, 'tim_app/exception.html')

timeismoneyge = TimeIsMoneygeView.as_view()

"""詳細表示"""
@login_required
def detail(request, overtime_id):
	overtime_detail = get_object_or_404(Time_is_moneyge.objects, id=overtime_id)
	if request.user == overtime_detail.user:
		return render(request, 'tim_app/detail.html', {'overtime_detail': overtime_detail})
	else:
		return render(request, "tim_app/exception.html")

"""出社時間登録"""
class MorningView(LoginRequiredMixin, OnlyYouMixin, View):
	def get(self, request, *args, **kwargs):
		context = {
			'morning_form': MorningForm(),
		}	
		return render(request, 'tim_app/morning_add.html', context)

	def post(self, request, *args, **kwargs):
		morning_form = MorningForm(request.POST)

		if morning_form.is_valid():
			morning = morning_form.save(commit=False) #保存待った！
			AM_NINE = datetime.now().replace(hour=9,minute=0,second=0,microsecond=0) #その日の朝9時を取得
			last_data = Time_is_moneyge.objects.filter(user=self.request.user).last() #ログインユーザーの最新のレコード取得

			#一番最初の登録
			if last_data == None:
				# 9時以降の登録
				if AM_NINE < datetime.now():
					morning.morning_overtime = AM_NINE - AM_NINE
					morning.overtime = AM_NINE - AM_NINE
					morning.user = self.request.user
					print("一番最初の登録、9時以降")
					morning.save() 
				# 9時以前の登録
				elif AM_NINE > datetime.now():
					morning.morning_overtime = AM_NINE - datetime.now()
					morning.overtime = AM_NINE -datetime.now()
					morning.user = self.request.user
					print("一番最初の登録、9時以前")
					morning.save()
			# 出勤登録をしていない場合
			elif last_data.evening_overtime == None: # 退勤手続きをしていない場合
				print("朝の登録無し")
				return render(request, 'tim_app/not_evening_register.html')
			#朝9時を超えている場合
			elif AM_NINE < datetime.now(): 
				morning.morning_overtime = AM_NINE - AM_NINE
				morning.overtime = AM_NINE - AM_NINE
				morning.user = self.request.user
				print("9時以降の登録")
				morning.save() 
			# 朝9時以前の場合（正常登録）
			else:
				morning.morning_overtime = AM_NINE - datetime.now() #朝の残業時間を取得
				morning.overtime = AM_NINE - datetime.now() #朝の残業時間を取得overtime用
				morning.user = self.request.user
				print("9時以前の登録")
				morning.save() #保存

			return redirect('tim_app:timeismoneyge_list', id=self.kwargs['id'])

		context = {
			   'morning_form': morning_form,
			   }

		return render(request, 'tim_app/morning_add.html', context)

	# def post(self, request, *args, **kwargs):
	# 	morning_form = MorningForm(request.POST)

	# 	if morning_form.is_valid():
	# 		morning = morning_form.save(commit=False) #保存待った！
	# 		AM_NINE = datetime.now().replace(hour=9,minute=0,second=0,microsecond=0) #その日の朝9時を取得
	# 		if AM_NINE < datetime.now(): #朝9時を超えている場合
	# 			morning.morning_overtime = AM_NINE - AM_NINE
	# 			morning.overtime = AM_NINE - AM_NINE
	# 			morning.user = self.request.user
	# 			morning.save() #保存
	# 		else:
	# 			morning.morning_overtime = AM_NINE - datetime.now() #朝の残業時間を取得
	# 			morning.overtime = AM_NINE - datetime.now() #朝の残業時間を取得overtime用
	# 			morning.user = self.request.user
	# 			morning.save() #保存
	# 		return redirect('tim_app:timeismoneyge_list', id=self.kwargs['id'])

	# 	context = {
	# 		   'morning_form': morning_form,
	# 		   }

	# 	return render(request, 'tim_app/morning_add.html', context)

morningview = MorningView.as_view()

"""退社時間登録"""
class EveningView(LoginRequiredMixin, OnlyYouMixin, View):
	def get(self, request, *args, **kwargs):
		context = {
			'evening_form': EveningForm(),
		}
		return render(request, 'tim_app/evening_add.html', context)

	def post(self, request, *args, **kwargs):
		evening_form = EveningForm(request.POST)

		if evening_form.is_valid():
			evening = evening_form.save(commit=False) #save待った！
			PM_SIX = datetime.now().replace(hour=18,minute=0,second=0,microsecond=0) #その日の18時を取得
			last_data = Time_is_moneyge.objects.filter(user=self.request.user).last()

			if last_data.morning_overtime == None: # 出勤手続きをしていない場合
				return render(request, "tim_app/not_morning_register.html")
			elif PM_SIX > datetime.now(): #18時を超えていない場合
				evening.evening_overtime = PM_SIX - PM_SIX
				evening.overtime = PM_SIX - PM_SIX #夜の残業時間をovertimeフィールド用
				evening.user = self.request.user
				evening.save() #一旦保存
				get_previous_record = evening.get_previous_by_date() #一つ前のレコード取得
				evening.todays_overtime = get_previous_record.overtime + evening.overtime #その日の残業時間を計算
				evening.working_time =evening.end_datetime - get_previous_record.start_datetime #トータル労働時間
				evening.save() #保存
			else: #18時を超えている場合
				evening.evening_overtime = datetime.now() - PM_SIX #夜の残業時間計算
				evening.overtime = datetime.now() - PM_SIX #夜の残業時間をovertimeフィールド用
				evening.user = self.request.user
				evening.save() #一旦保存
				get_previous_record = evening.get_previous_by_date() #一つ前のレコード取得
				evening.todays_overtime = get_previous_record.overtime + evening.overtime #その日の残業時間を計算
				evening.working_time =evening.end_datetime - get_previous_record.start_datetime #トータル労働時間
				print(get_previous_record.id)
				print(evening.id)
				evening.save() #保存

			return redirect('tim_app:timeismoneyge_list', id=self.kwargs['id'])	

		context = {
			'evening_form': evening_form,
			}

		return render(request, 'tim_app/evening_add.html', context)

eveningview = EveningView.as_view()		

"""編集"""
def morning_edit(request, overtime_id):
	edit_overtime = get_object_or_404(Time_is_moneyge, id=overtime_id)
	if request.method == "POST":
		morning_form = MorningForm(request.POST, instance=edit_overtime)
		if morning_form.is_valid():
			morning_form.save()
			return redirect('tim_app:timeismoneyge_list', id=request.user.id)
	else:
		morning_form = MorningForm(instance=edit_overtime)

	context = {
		'morning_form': morning_form,
		'edit_overtime': edit_overtime,
	}
	return render(request, 'tim_app/morning_edit.html', context)

def evening_edit(request, overtime_id):
	edit_overtime = get_object_or_404(Time_is_moneyge, id=overtime_id)
	if request.method == "POST":
		evening_form = EveningForm(request.POST, instance=edit_overtime)
		if evening_form.is_valid():
			evening_form.save()
			return redirect('tim_app:timeismoneyge_list', id=request.user.id)
	else:
		evening_form = EveningForm(instance=edit_overtime)

	context = {
		'evening_form': evening_form,
		'edit_overtime': edit_overtime,
	}
	return render(request, 'tim_app/evening_edit.html', context)

"""削除"""
@require_POST
def delete(request, overtime_id):
	delete_overtime = get_object_or_404(Time_is_moneyge, id=overtime_id)
	delete_overtime.delete()
	return redirect('tim_app:timeismoneyge_list', id=request.user.id)

"""時給登録"""
class HourlyWageView(LoginRequiredMixin, OnlyYouMixin, View):
	def get(self, request, *args, **kwargs):
		context = {
			'hourly_wage_form': HourlyWageForm(),
		}
		return render(request, 'tim_app/hourly_wage_add.html', context)

	def post(self, request, *args, **kwargs):
		hourly_wage_form = HourlyWageForm(request.POST)

		if hourly_wage_form.is_valid():
			hourly_wage_form = hourly_wage_form.save(commit=False) #保存待った
			hourly_wage_form.user = self.request.user
			hourly_wage_form.save() #保存

			return redirect('tim_app:timeismoneyge_list', id=self.kwargs['id'])	

		context = {
			'hourly_wage_form': hourly_wage_form,
			}

		return render(request, 'tim_app/hourly_wage_add.html', context)

hourlywageview = HourlyWageView.as_view()

"""有給休暇登録"""
class PaidLeaveView(LoginRequiredMixin, OnlyYouMixin, View):
	def get(self, request, *args, **kwargs):
		context = {
			'paid_leave_form': PaidLeaveForm(),
		}	
		return render(request, 'tim_app/paid_leave.html', context)

	def post(self, request, *args, **kwargs):
		paid_leave_form = PaidLeaveForm(request.POST)

		if paid_leave_form.is_valid():
			paid_leave_form = paid_leave_form.save(commit=False) #保存待った
			paid_leave_form.user = self.request.user
			paid_leave_form.save()

			return redirect('tim_app:timeismoneyge_list', id=self.kwargs['id'])

		context = {
			   'paid_leave_form': paid_leave_form,
			   }

		return render(request, 'tim_app/paid_leave.html', context)

paidleaveview = PaidLeaveView.as_view()

"""有給休暇削除"""
@require_POST
def paid_leave_delete(request, paid_leave_id):
	paid_leave_delete = get_object_or_404(Paid_leave, id=paid_leave_id)
	paid_leave_delete.delete()
	return redirect('tim_app:timeismoneyge_list', id=request.user.id)

"""PDF出力"""
class GeneratePdfView(LoginRequiredMixin, OnlyYouMixin, View):
	def get(self, request, *args, **kwargs):
		"""今月の労働実績"""
		today = datetime.today()
		if today.day > 10: #one_to_ten_daysには1から10の数字がくる
			eleventh_of_thismonth = today + relativedelta(day=11) #今月の11日を取得
			morning_overtime_of_thismonth_for_pdf = Time_is_moneyge.objects.filter(date__range=(eleventh_of_thismonth, today)).exclude(morning_overtime__exact = None) #11日から今日まで＆morning_overtime=None除外を取得
			evening_overtime_of_thismonth_for_pdf = Time_is_moneyge.objects.filter(date__range=(eleventh_of_thismonth, today)).exclude(evening_overtime__exact = None) #11日から今日まで＆evening_overtime=None除外を取得
			for mo in morning_overtime_of_thismonth_for_pdf:
					mo.morning_overtime = str(mo.morning_overtime).split('.')[0] #朝の時間外労働のmicrosecondを切り捨て
			for eve in evening_overtime_of_thismonth_for_pdf:
				eve.evening_overtime = str(eve.evening_overtime).split('.')[0] #夜の時間外労働のmicrosecondを切り捨て
				eve.todays_overtime = str(eve.todays_overtime).split('.')[0] #今日の残業時間のmicrosecondを切り捨て
		else:
			eleventh_of_one_month_ago = today - relativedelta(months=1, day=11) #一月前の11日を取得
			morning_overtime_of_thismonth_for_pdf = Time_is_moneyge.objects.filter(date__range=(eleventh_of_one_month_ago, today)).exclude(morning_overtime__exact = None) #11日から今日まで＆morning_overtime=None除外を取得
			evening_overtime_of_thismonth_for_pdf = Time_is_moneyge.objects.filter(date__range=(eleventh_of_one_month_ago, today)).exclude(evening_overtime__exact = None) #11日から今日まで＆evening_overtime=None除外を取得
			for mo in morning_overtime_of_thismonth_for_pdf:
					mo.morning_overtime = str(mo.morning_overtime).split('.')[0] #朝の時間外労働のmicrosecondを切り捨て
			for eve in evening_overtime_of_thismonth_for_pdf:
				eve.evening_overtime = str(eve.evening_overtime).split('.')[0] #夜の時間外労働のmicrosecondを切り捨て
				eve.todays_overtime = str(eve.todays_overtime).split('.')[0] #今日の残業時間のmicrosecondを切り捨て

		"""合計残業時間取得"""
		#今日の日付が11日〜31日の場合
		today = datetime.today() #今日の日付を取得
		if today.day > 10: #one_to_ten_daysには1から10の数字がくる
			eleventh_of_thismonth = today + relativedelta(day=11) #今月の11日を取得
			work_of_thismonth = Time_is_moneyge.objects.filter(date__range=(eleventh_of_thismonth, today), user=self.request.user) #11日から今日までのオブジェクトを取得
			morning_overtime_of_thismonth = work_of_thismonth.aggregate(morning_overtime=Sum('morning_overtime')) #今月の朝の残業時間を集計
			evening_overtime_of_thismonth = work_of_thismonth.aggregate(evening_overtime=Sum('evening_overtime')) #今月の夜の残業時間を集計
			for moot_key, moot_value in morning_overtime_of_thismonth.items(): #keyとvalueに分ける
				morning_total_overtime = moot_value #valueを取得
				for eoot_key, eoot_value in evening_overtime_of_thismonth.items(): #keyとvalueに分ける
					evening_total_overtime = eoot_value #valueを取得
					try:
						total_overtime_of_thismonth = morning_total_overtime + evening_total_overtime #今月の残業時間合計を取得
						minutes, seconds = divmod(total_overtime_of_thismonth.seconds + total_overtime_of_thismonth.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						total_overtime_of_thismonth = '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds) 
					except:
						total_overtime_of_thismonth = 0
		#今日の日付が1日〜10日の場合
		else:
			eleventh_of_one_month_ago = today - relativedelta(months=1, day=11) #一月前の11日を取得
			work_of_thismonth = Time_is_moneyge.objects.filter(date__range=(eleventh_of_one_month_ago, today), user=self.request.user) #11日から今日までのオブジェクトを取得
			morning_overtime_of_thismonth = work_of_thismonth.aggregate(morning_overtime=Sum('morning_overtime')) #今月の朝の残業時間を集計
			evening_overtime_of_thismonth = work_of_thismonth.aggregate(evening_overtime=Sum('evening_overtime')) #今月の夜の残業時間を集計
			for moot_key, moot_value in morning_overtime_of_thismonth.items(): #keyとvalueに分ける
				morning_total_overtime = moot_value #valueを取得
				for eoot_key, eoot_value in evening_overtime_of_thismonth.items(): #keyとvalueに分ける
					evening_total_overtime = eoot_value #valueを取得
					try:
						total_overtime_of_thismonth = morning_total_overtime + evening_total_overtime #今月の残業時間合計を取得
						minutes, seconds = divmod(total_overtime_of_thismonth.seconds + total_overtime_of_thismonth.days * 86400, 60) #days * 86400で日にちを秒に変換、時間を秒に変換したものを+して60で割って分と秒にわける
						hours, minutes = divmod(minutes, 60) #分を時と分に
						total_overtime_of_thismonth = '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
					except:
						total_overtime_of_thismonth = 0

		"""有給休暇一覧"""
		today = datetime.today() #今日の日付を取得
		if today.day > 10:
			eleventh_of_thismonth = today + relativedelta(day=11) #今月の11日を取得
			tenth_of_next_month = today + relativedelta(months=1, day=10) #次月の10日取得
			paid_leave_list_pdf = Paid_leave.objects.filter(paid_leave_date__range=(eleventh_of_thismonth, tenth_of_next_month), user=self.request.user).order_by('paid_leave_date') 
		else:
			eleventh_of_one_month_ago = today - relativedelta(months=1, day=11) #一月前の11日を取得
			tenth_of_this_month = today + relativedelta(day=10) #今月の10日取得
			paid_leave_list_pdf = Paid_leave.objects.filter(paid_leave_date__range=(eleventh_of_one_month_ago, tenth_of_this_month), user=self.request.user).order_by('paid_leave_date') 

		html_template = get_template('tim_app/generate_pdf.html')
		html_str = html_template.render({
			'morning_overtime_of_thismonth_for_pdf': morning_overtime_of_thismonth_for_pdf,
			'evening_overtime_of_thismonth_for_pdf': evening_overtime_of_thismonth_for_pdf,
			'total_overtime_of_thismonth': total_overtime_of_thismonth,
			'paid_leave_list_pdf': paid_leave_list_pdf,
			},request) 
		pdf_file = HTML(string=html_str).write_pdf()
		response = HttpResponse(pdf_file, content_type='application/pdf')
		response['Content-Disposition'] = 'filename="work_of_thismonth.pdf"'

		return response

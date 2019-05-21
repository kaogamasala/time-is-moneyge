from django.db import models
from django.conf import settings
from accounts.models import CustomUser

# Create your models here.
class Time_is_moneyge(models.Model):
	date = models.DateField(auto_now_add=True)
	morning_word = models.CharField('おはようの一言', max_length=150, null=True, blank=True)
	start_datetime = models.DateTimeField(auto_now_add=True)
	morning_overtime = models.DurationField(null=True)
	evening_word = models.CharField('お疲れ様の一言', max_length=150, null=True, blank=True)
	end_datetime = models.DateTimeField(auto_now_add=True)
	evening_overtime = models.DurationField(null=True)
	overtime = models.DurationField(null=True)
	todays_overtime = models.DurationField(null=True)
	working_time = models.DurationField(null=True)
	user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

	def __str__(self):
		return str(self.morning_word)

class Hourly_wage(models.Model):
	created_datetime = models.DateTimeField(auto_now_add=True)
	hourly_wage = models.PositiveIntegerField('時給', null=True)
	user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

	def __str__(self):
		return str(self.hourly_wage)

class Paid_leave(models.Model):
	created_datetime = models.DateTimeField(auto_now_add=True)
	paid_leave_date = models.DateField('有給休暇日', null=True)
	memo = models.CharField('メモ', max_length=300, null=True, blank=True)
	user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

	def __str__(self):
		return str(self.paid_leave_date)
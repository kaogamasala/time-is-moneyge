from django.forms import ModelForm
from django import forms
from .models import Time_is_moneyge, Hourly_wage, Paid_leave

class MorningForm(forms.ModelForm):
	class Meta:
		model = Time_is_moneyge
		fields = {'morning_word'}

class EveningForm(forms.ModelForm):
	class Meta:
		model = Time_is_moneyge
		fields = {'evening_word'}

class HourlyWageForm(forms.ModelForm):
	class Meta:
		model = Hourly_wage
		fields = {'hourly_wage'}

class PaidLeaveForm(forms.ModelForm):
	class Meta:
		model = Paid_leave
		fields = {'memo','paid_leave_date'}
		
	# modelformにplaceholderを入れる
	def __init__(self, *args, **kwargs):
		super(PaidLeaveForm, self).__init__(*args, **kwargs)
		for key, field in self.fields.items():
			if isinstance(field.widget, forms.TextInput) or \
				isinstance(field.widget, forms.Textarea) or \
				isinstance(field.widget, forms.DateInput) or \
				isinstance(field.widget, forms.DateTimeInput) or \
				isinstance(field.widget, forms.TimeInput):
				field.widget.attrs.update({'placeholder': field.label})

		
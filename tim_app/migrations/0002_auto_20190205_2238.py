# Generated by Django 2.1 on 2019-02-05 13:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tim_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='time_is_moneyge',
            name='morning_overtime',
        ),
        migrations.AddField(
            model_name='time_is_moneyge',
            name='word',
            field=models.CharField(default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
    ]
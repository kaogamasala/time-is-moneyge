# Generated by Django 2.1 on 2019-02-10 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tim_app', '0002_auto_20190205_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='time_is_moneyge',
            name='morning_overtime',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='time_is_moneyge',
            name='word',
            field=models.CharField(max_length=150, null=True, verbose_name='今日の一言'),
        ),
    ]
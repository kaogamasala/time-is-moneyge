# Generated by Django 2.1 on 2019-02-17 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tim_app', '0011_auto_20190217_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time_is_moneyge',
            name='overtime',
            field=models.DateTimeField(null=True),
        ),
    ]

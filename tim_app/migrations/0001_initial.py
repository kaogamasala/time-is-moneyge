# Generated by Django 2.1 on 2019-02-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Time_is_moneyge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(auto_now_add=True)),
                ('morning_overtime', models.DateTimeField()),
            ],
        ),
    ]

# Generated by Django 2.1 on 2019-04-15 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tim_app', '0017_paid_leave'),
    ]

    operations = [
        migrations.AddField(
            model_name='time_is_moneyge',
            name='user',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paid_leave',
            name='memo',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='メモ'),
        ),
    ]

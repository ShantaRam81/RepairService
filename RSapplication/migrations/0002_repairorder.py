# Generated by Django 5.0.2 on 2024-02-19 18:33

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RSapplication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Order created time')),
                ('end_time', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='End time')),
                ('repairman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Мастер', to=settings.AUTH_USER_MODEL, verbose_name='Repairman')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Заявка_на_ремонт', to='RSapplication.repairrequest', verbose_name='Request')),
            ],
            options={
                'verbose_name': 'Заказ на обслуживание',
                'verbose_name_plural': 'Заказы на обслуживание',
            },
        ),
    ]
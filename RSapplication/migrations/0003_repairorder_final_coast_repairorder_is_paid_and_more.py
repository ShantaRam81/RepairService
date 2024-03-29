# Generated by Django 5.0.2 on 2024-02-24 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RSapplication', '0002_repairrequest_take_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairorder',
            name='final_coast',
            field=models.CharField(default=0, max_length=6, verbose_name='Окончательная стоимость'),
        ),
        migrations.AddField(
            model_name='repairorder',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Статус оплаты'),
        ),
        migrations.AddField(
            model_name='repairrequest',
            name='technic_accepted',
            field=models.BooleanField(default=False, verbose_name='Статус принятия техники'),
        ),
    ]

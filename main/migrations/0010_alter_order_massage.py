# Generated by Django 5.0.4 on 2024-05-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_order_massage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='massage',
            field=models.CharField(default='Примечание', max_length=500, null=True),
        ),
    ]

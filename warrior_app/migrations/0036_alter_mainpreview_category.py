# Generated by Django 5.2 on 2025-05-16 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warrior_app', '0035_cart_items_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpreview',
            name='category',
            field=models.CharField(choices=[('home_ups', 'Home Ups'), ('solar_power', 'Solar Power'), ('batteries', 'Batteries'), ('ev_charger', 'EV Charger'), ('water_purifier', 'Water Purifier'), ('li_ion_battery_inverter', 'Lithium Ion Battery Inverter')], max_length=100),
        ),
    ]

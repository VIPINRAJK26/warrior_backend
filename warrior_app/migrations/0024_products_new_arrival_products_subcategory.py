# Generated by Django 5.2 on 2025-05-12 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warrior_app', '0023_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='new_arrival',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='products',
            name='subcategory',
            field=models.CharField(choices=[('online_ups', 'Online Ups'), ('offline_ups', 'Offline Ups'), ('hkva_ups', 'HKVA Ups'), ('solar_ups', 'Solar Ups'), ('solar_panel', 'Solar Panel'), ('lithium_solar_inverter', 'Lithium Solar Inverter'), ('MPPTS', 'MPPTS'), ('tubular_batteries', 'Tubular Batteries'), ('solar_batteries', 'Solar Batteries'), ('lithium_ion_batteries', 'Lithium Ion Batteries')], default=0, max_length=100),
        ),
    ]

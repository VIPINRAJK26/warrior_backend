# Generated by Django 5.2 on 2025-05-14 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warrior_app', '0031_products_ah_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='Type',
            new_name='product_type',
        ),
    ]

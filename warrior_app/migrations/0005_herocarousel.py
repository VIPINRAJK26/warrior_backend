# Generated by Django 5.2 on 2025-05-01 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warrior_app', '0004_products_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]

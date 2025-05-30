# Generated by Django 5.2 on 2025-05-14 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warrior_app', '0029_previewdetails_subcategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='Type',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='panel_capacity',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='product_series',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='suitable_for',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='technology',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='va_rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='warranty',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='wattage',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
    ]

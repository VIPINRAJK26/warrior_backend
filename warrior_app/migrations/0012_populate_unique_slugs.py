from django.db import migrations
from django.utils.text import slugify

def populate_unique_slugs(apps, schema_editor):
    PreviewDetails = apps.get_model('warrior_app', 'PreviewDetails')
    slugs = set()
    for obj in PreviewDetails.objects.all():
        if obj.slug:
            base_slug = slugify(obj.slug)
        else:
            base_slug = slugify(obj.variant_name or f"preview-{obj.id}")

        slug = base_slug
        counter = 1
        while slug in slugs or PreviewDetails.objects.filter(slug=slug).exclude(id=obj.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        obj.slug = slug
        obj.save()
        slugs.add(slug)

class Migration(migrations.Migration):

    dependencies = [
        ('warrior_app', '0011_alter_previewdetails_slug'),
    ]

    operations = [
        migrations.RunPython(populate_unique_slugs),
    ]

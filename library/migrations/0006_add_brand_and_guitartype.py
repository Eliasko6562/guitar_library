from django.db import migrations, models
import django.db.models.deletion


def migrate_guitar_type_and_brand(apps, schema_editor):
    Guitar = apps.get_model('library', 'Guitar')
    Brand = apps.get_model('library', 'Brand')
    GuitarType = apps.get_model('library', 'GuitarType')

    type_names = ['Classical', 'Electric', 'Acoustic', 'Electroacoustic', 'Bass']
    type_objects = {}
    for name in type_names:
        obj, _ = GuitarType.objects.get_or_create(name=name)
        type_objects[name] = obj

    brand_cache = {}
    for guitar in Guitar.objects.all():
        brand_name = 'Unknown'
        if guitar.name:
            brand_name = guitar.name.split()[0]
        brand = brand_cache.get(brand_name)
        if brand is None:
            brand, _ = Brand.objects.get_or_create(name=brand_name)
            brand_cache[brand_name] = brand

        guitar.brand = brand

        current_type = getattr(guitar, 'guitar_type_name', None)
        if current_type is None:
            current_type = getattr(guitar, 'guitar_type', None)

        if current_type:
            normalized = current_type.strip()
            if normalized not in type_objects:
                normalized = next((name for name in type_names if name.lower() in normalized.lower()), None)
            if normalized in type_objects:
                guitar.guitar_type = type_objects[normalized]

        guitar.save()


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_merge_20260523_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('founded_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('website', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GuitarType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Guitar type',
                'verbose_name_plural': 'Guitar types',
                'ordering': ['name'],
            },
        ),
        migrations.RenameField(
            model_name='guitar',
            old_name='guitar_type',
            new_name='guitar_type_name',
        ),
        migrations.AddField(
            model_name='guitar',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.brand'),
        ),
        migrations.AddField(
            model_name='guitar',
            name='guitar_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.guitartype'),
        ),
        migrations.RunPython(migrate_guitar_type_and_brand, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='guitar',
            name='guitar_type_name',
        ),
    ]

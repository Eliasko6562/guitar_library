from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_add_brand_and_guitartype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='website',
        ),
    ]

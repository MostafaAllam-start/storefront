# Generated by Django 4.0.6 on 2022-07-25 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_address_zip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='featured_products',
            new_name='featured_product',
        ),
        migrations.RenameField(
            model_name='collection', 
            old_name='tiltle',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='unit_price',
        ),
    ]

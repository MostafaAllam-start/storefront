# Generated by Django 4.1 on 2022-08-13 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_customer_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('placed_at',), 'permissions': [('cancel_order', 'Can cancel Order')]},
        ),
    ]
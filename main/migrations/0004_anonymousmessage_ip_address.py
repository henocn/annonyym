# Generated by Django 5.1.4 on 2024-12-26 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_anonymousmessage_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymousmessage',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]

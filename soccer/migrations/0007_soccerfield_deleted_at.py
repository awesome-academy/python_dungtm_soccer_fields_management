# Generated by Django 4.2.23 on 2025-07-23 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0006_fieldrequest_address_fieldrequest_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='soccerfield',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

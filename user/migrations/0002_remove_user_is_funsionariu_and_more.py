# Generated by Django 4.2.11 on 2024-07-09 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="is_funsionariu",),
        migrations.RemoveField(model_name="user", name="is_recepcionist",),
    ]
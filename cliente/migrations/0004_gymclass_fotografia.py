# Generated by Django 4.2.11 on 2024-07-09 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cliente", "0003_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="gymclass",
            name="fotografia",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
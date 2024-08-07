# Generated by Django 4.2.11 on 2024-07-04 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("custom", "0001_initial"),
        ("cliente", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("enrollment_date", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="GymClass",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("days_of_week", models.CharField(max_length=150)),
                (
                    "payment_per_month",
                    models.DecimalField(decimal_places=2, default=25.0, max_digits=6),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nu_id", models.CharField(max_length=20, null=True, unique=True)),
                ("naran", models.CharField(max_length=200, null=True)),
                (
                    "sexo",
                    models.CharField(
                        blank=True,
                        choices=[("Mane", "Mane"), ("Feto", "Feto")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "naturalidade",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("data_moris", models.DateField(null=True)),
                ("join_date", models.DateField(auto_now_add=True)),
                ("end_date", models.DateField(null=True)),
                ("enderesu", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Solteiru/a", "Solteiru/a"),
                            ("Marridu/a", "Marridu/a"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("phone", models.CharField(max_length=200, null=True)),
                ("email", models.EmailField(blank=True, max_length=200, null=True)),
                (
                    "fotografia",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
                (
                    "documentos",
                    models.FileField(blank=True, null=True, upload_to="CV/"),
                ),
                (
                    "municipio",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="custom.municipality",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(model_name="funcionariu", name="user",),
        migrations.RemoveField(model_name="visitor", name="user",),
        migrations.DeleteModel(name="DetailVisitor",),
        migrations.DeleteModel(name="Funcionariu",),
        migrations.DeleteModel(name="Visitor",),
        migrations.AddField(
            model_name="enrollment",
            name="gym_class",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="cliente.gymclass"
            ),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="cliente.member"
            ),
        ),
    ]

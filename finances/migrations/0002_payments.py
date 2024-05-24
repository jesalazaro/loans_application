# Generated by Django 5.0.6 on 2024-05-21 02:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finances", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payments",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(max_length=60, unique=True)),
                ("total_amount", models.DecimalField(decimal_places=10, max_digits=20)),
                ("status", models.SmallIntegerField()),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
# Generated by Django 4.2.2 on 2023-07-10 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="customers",
        ),
    ]

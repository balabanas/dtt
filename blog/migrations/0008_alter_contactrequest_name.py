# Generated by Django 4.2.7 on 2023-11-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0007_alter_contactrequest_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactrequest",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-22 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_alter_article_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactrequest", name="content", field=models.TextField(),
        ),
    ]

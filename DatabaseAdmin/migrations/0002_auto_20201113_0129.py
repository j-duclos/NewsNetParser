# Generated by Django 3.1.3 on 2020-11-13 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DatabaseAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_posted',
            field=models.CharField(max_length=25),
        ),
    ]
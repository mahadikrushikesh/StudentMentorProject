# Generated by Django 3.2.9 on 2021-12-02 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20211202_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-01 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='NewUser',
        ),
        migrations.AddField(
            model_name='questions',
            name='attachment_file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]

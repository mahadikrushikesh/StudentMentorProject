# Generated by Django 3.2.9 on 2021-12-02 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20211201_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questions',
            name='message',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]

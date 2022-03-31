# Generated by Django 4.0.2 on 2022-03-30 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='fileName',
        ),
        migrations.AddField(
            model_name='file',
            name='uploadedFile',
            field=models.FileField(default=1, upload_to='Uploaded Files/'),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.0.2 on 2022-04-20 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecSys', '0004_remove_userdata_file_id_userdata_uploadedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='uploadedFile',
            field=models.FileField(upload_to='Uploaded User Files/'),
        ),
    ]

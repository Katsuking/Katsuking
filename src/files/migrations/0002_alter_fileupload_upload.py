# Generated by Django 3.2.6 on 2021-09-07 05:43

from django.db import migrations, models
import files.models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='upload',
            field=models.FileField(upload_to=files.models.dir_path_name),
        ),
    ]
# Generated by Django 2.1.2 on 2018-12-24 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminInterface', '0004_auto_20181224_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='pics',
            field=models.FileField(upload_to='topic_image/'),
        ),
    ]
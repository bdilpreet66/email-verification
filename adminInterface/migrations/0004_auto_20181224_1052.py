# Generated by Django 2.1.2 on 2018-12-24 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminInterface', '0003_auto_20181224_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='pics',
            field=models.ImageField(default='icon/file-not-found.jpg', upload_to='topic_image/'),
        ),
    ]
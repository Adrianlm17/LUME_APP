# Generated by Django 5.0.4 on 2024-05-03 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_userprofile_img_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='IMG_profile',
            field=models.ImageField(default='anonimo.png', upload_to=''),
        ),
    ]

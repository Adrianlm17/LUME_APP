# Generated by Django 5.0.4 on 2024-05-03 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_comunidad_empresa_remove_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comunidad',
            name='IMG_community',
            field=models.ImageField(default='anonimo.jpg', upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='IMG_profile',
            field=models.ImageField(default='anonimo.jpg', upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='IMG_profile',
            field=models.ImageField(default='anonimo.jpg', upload_to='profiles/'),
        ),
    ]

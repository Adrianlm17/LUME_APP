# Generated by Django 5.0.4 on 2024-05-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_empresa_img_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidencia',
            name='fecha_cierre',
            field=models.DateField(blank=True, null=True),
        ),
    ]
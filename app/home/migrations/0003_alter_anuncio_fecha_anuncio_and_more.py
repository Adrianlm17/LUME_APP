# Generated by Django 5.0.4 on 2024-05-11 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_anuncio_fecha_anuncio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuncio',
            name='fecha_anuncio',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='vivienda',
            name='rol_comunidad',
            field=models.CharField(choices=[('community_president', 'Community President'), ('community_vicepresident', 'Community Vice President'), ('community_user', 'Community User')], default='community_user', max_length=100),
        ),
    ]

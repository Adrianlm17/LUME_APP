# Generated by Django 5.0.4 on 2024-05-12 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_anuncio_fecha_anuncio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='segurocomunidad',
            name='empresa',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='segurocomunidad',
            name='cubre',
            field=models.TextField(),
        ),
    ]
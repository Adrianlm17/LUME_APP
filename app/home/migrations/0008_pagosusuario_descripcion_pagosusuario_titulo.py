# Generated by Django 5.0.4 on 2024-05-07 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_gasto_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagosusuario',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pagosusuario',
            name='titulo',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

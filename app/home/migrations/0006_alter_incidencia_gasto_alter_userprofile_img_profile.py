# Generated by Django 5.0.4 on 2024-05-12 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_gasto_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidencia',
            name='gasto',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='IMG_profile',
            field=models.ImageField(default='profiles/anonimo.png', upload_to=''),
        ),
    ]

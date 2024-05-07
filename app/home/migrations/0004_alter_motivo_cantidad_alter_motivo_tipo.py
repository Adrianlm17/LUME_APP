# Generated by Django 5.0.4 on 2024-05-07 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_recibo_cantidad_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motivo',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='motivo',
            name='tipo',
            field=models.CharField(choices=[('luz', 'Luz'), ('agua', 'Agua'), ('gas', 'Gas'), ('piscina', 'Piscina'), ('jardineria', 'Jardinería'), ('personal_comunidad', 'Personal de comunidad'), ('limpieza', 'Limpieza'), ('extras', 'Extras')], max_length=100, null=True),
        ),
    ]

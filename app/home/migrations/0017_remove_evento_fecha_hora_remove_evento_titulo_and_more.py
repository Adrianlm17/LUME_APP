# Generated by Django 5.0.4 on 2024-05-14 11:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_alter_comunidad_img_profile_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='fecha_hora',
        ),
        migrations.RemoveField(
            model_name='evento',
            name='titulo',
        ),
        migrations.AddField(
            model_name='evento',
            name='current_attendees',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='evento',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='eventos/'),
        ),
        migrations.AddField(
            model_name='evento',
            name='max_attendees',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evento',
            name='visibility',
            field=models.CharField(choices=[('publico', 'Publico'), ('privado', 'Privado')], default='publico', max_length=10),
        ),
        migrations.AlterField(
            model_name='comunidad',
            name='IMG_profile',
            field=models.ImageField(default='perfiles/default.jpg', upload_to='perfiles/'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='IMG_profile',
            field=models.ImageField(default='perfiles/default.jpg', upload_to='perfiles/'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='comunidad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.comunidad'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='incidencia',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='incidencias/'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.evento')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('evento', 'usuario')},
            },
        ),
    ]
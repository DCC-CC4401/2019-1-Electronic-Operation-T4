# Generated by Django 2.2 on 2019-05-02 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Estudiante', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estudiante',
            old_name='public',
            new_name='Presentó',
        ),
    ]
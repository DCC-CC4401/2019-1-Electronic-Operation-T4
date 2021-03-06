# Generated by Django 2.2 on 2019-05-05 21:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('9916bef5-1c53-4d07-b7fb-eb59e9890d4b'), editable=False, primary_key=True, serialize=False)),
                ('código', models.CharField(max_length=20)),
                ('número_sección', models.PositiveSmallIntegerField(default=1)),
                ('año', models.IntegerField(default=2019)),
                ('semestre', models.SmallIntegerField(choices=[(1, 'Otoño'), (2, 'Primavera'), (3, 'Verano')], default=1)),
            ],
            options={
                'unique_together': {('código', 'número_sección', 'año', 'semestre')},
            },
        ),
    ]

# Generated by Django 3.2.3 on 2021-05-26 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paf', '0004_metier_profil'),
    ]

    operations = [
        migrations.AddField(
            model_name='metier',
            name='public_associe',
            field=models.ManyToManyField(to='paf.PublicCible'),
        ),
    ]

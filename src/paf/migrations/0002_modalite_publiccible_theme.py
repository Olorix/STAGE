# Generated by Django 3.2.3 on 2021-05-21 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modalite',
            fields=[
                ('code', models.CharField(max_length=1, primary_key=True, serialize=False, verbose_name='Code')),
                ('libelle', models.CharField(max_length=250, verbose_name='Libellé')),
            ],
        ),
        migrations.CreateModel(
            name='PublicCible',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='Code')),
                ('libelle', models.CharField(max_length=250, verbose_name='Libellé')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, verbose_name='Code')),
                ('libelle', models.CharField(max_length=250, verbose_name='Libellé')),
                ('code_origine', models.CharField(max_length=3, verbose_name="Code d'origine")),
            ],
        ),
    ]
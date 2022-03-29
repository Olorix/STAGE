# Generated by Django 3.2.3 on 2021-05-26 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paf', '0005_metier_public_associe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metier2Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0)),
                ('metier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paf.metier')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paf.theme')),
            ],
        ),
        migrations.AddField(
            model_name='metier',
            name='related_themes',
            field=models.ManyToManyField(through='paf.Metier2Theme', to='paf.Theme'),
        ),
    ]

# Generated by Django 3.0 on 2021-04-29 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210428_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feereason',
            name='label',
            field=models.CharField(choices=[('PESAGE', 'PESAGE'), ('PEAGE', 'PEAGE'), ('SBK', 'SEJOUR BOUAKE'), ('FRAIS TAXI', 'TAXI')], max_length=80, verbose_name='Libelle'),
        ),
    ]

# Generated by Django 3.0 on 2021-04-28 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feerequest',
            old_name='commentaire',
            new_name='description',
        ),
        migrations.AddField(
            model_name='feerequest',
            name='motif_refus',
            field=models.TextField(blank=True, verbose_name='Observation'),
        ),
    ]

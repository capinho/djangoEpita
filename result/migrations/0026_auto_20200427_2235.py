# Generated by Django 2.1.2 on 2020-04-27 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0025_auto_20200427_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(blank=True, choices=[('INFOSUP', 'INFOSUP'), ('INFOSPE', 'INFOSPE'), ('ING1', 'ING1'), ('ING2', 'ING2'), ('ING3', 'ING3')], max_length=12),
        ),
    ]

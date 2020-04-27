# Generated by Django 2.1.2 on 2020-04-27 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0026_auto_20200427_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carryoverstudent',
            name='level',
            field=models.CharField(blank=True, choices=[('INFOSUP', 'INFOSUP'), ('INFOSPE', 'INFOSPE'), ('ING1', 'ING1'), ('ING2', 'ING2'), ('ING3', 'ING3')], max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.CharField(choices=[('INFOSUP', 'INFOSUP'), ('INFOSPE', 'INFOSPE'), ('ING1', 'ING1'), ('ING2', 'ING2'), ('ING3', 'ING3')], max_length=12),
        ),
    ]

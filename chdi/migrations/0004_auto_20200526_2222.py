# Generated by Django 3.0.6 on 2020-05-26 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chdi', '0003_diplomsfile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='template',
            options={'verbose_name': 'Шаблон', 'verbose_name_plural': 'Шаблоны'},
        ),
        migrations.RemoveField(
            model_name='diplomsfile',
            name='updated',
        ),
    ]

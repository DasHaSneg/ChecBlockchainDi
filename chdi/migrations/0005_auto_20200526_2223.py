# Generated by Django 3.0.6 on 2020-05-26 22:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chdi', '0004_auto_20200526_2222'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='template',
            options={'ordering': ['-created'], 'verbose_name': 'Шаблон', 'verbose_name_plural': 'Шаблоны'},
        ),
        migrations.AddField(
            model_name='template',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создан'),
            preserve_default=False,
        ),
    ]

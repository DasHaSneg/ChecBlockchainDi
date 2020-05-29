# Generated by Django 3.0.6 on 2020-05-26 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chdi', '0002_auto_20200526_0707'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiplomsFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('file', models.FileField(upload_to='diplom_file/%y/%m/%d/', verbose_name='Файл')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменен')),
            ],
            options={
                'verbose_name': 'Архив дипломов',
                'verbose_name_plural': 'Архивы дипломов',
                'ordering': ['-created'],
            },
        ),
    ]
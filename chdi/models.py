from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Template(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    diplom_name =  models.CharField(max_length=200, default="Имя диплома")
    diplom_description =  models.CharField(max_length=200, default="Описание диплома")
    organization_name = models.CharField(max_length=200, default="имя организации")
    organization_url = models.CharField(max_length=200, default="https://www.susu.ru/")
    organization_email = models.CharField(max_length=200, default="info@susu.ru")
    logo_image = models.ImageField(upload_to='logo/%Y/%m/%d', blank=True)
    seal_image = models.ImageField(upload_to='diplom/%Y/%m/%d', blank=True)
    json_file = models.FileField(upload_to='json/', blank=True)
    created_data = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return '{0} ({1})'.format(self.diplom_name, self.created_data)

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['-created_data']

class Profile(models.Model):
    user_id=models.OneToOneField(User, on_delete=models.CASCADE)
    job = models.CharField(max_length=200, default="Сотрудник")
    patronymic = models.CharField(max_length=200, default="Ивановна")
    signature_image = models.ImageField(upload_to='sign_image/%Y/%m/%d', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return '{0} {1} {2} ({3})'.format(self.user_id.last_name,self.user_id.first_name,self.patronymic, self.job)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
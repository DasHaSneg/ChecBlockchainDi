from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200, default="Имя")
    user_jobtitle = models.CharField(max_length=200, default="Сотрудник")
    user_image = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)
    diplom_name =  models.CharField(max_length=200, default="Имя диплома")
    diplom_descr =  models.CharField(max_length=200, default="Описание диплома")
    diplom_image = models.ImageField(upload_to='diplom/%Y/%m/%d', blank=True)
    org_name = models.CharField(max_length=200, default="имя организации")
    org_url = models.CharField(max_length=200, default="https://www.susu.ru/")
    org_email = models.CharField(max_length=200, default="info@susu.ru")
    org_image = models.ImageField(upload_to='org/%Y/%m/%d', blank=True)
    json_data = models.CharField(max_length=1500, default="json data")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return '{0} ({1})'.format(self.diplom_name, self.created)

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['-created']

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
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
        return '{0} {1} {2} ({3})'.format(self.user.last_name,self.user.first_name,self.patronymic, self.job)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
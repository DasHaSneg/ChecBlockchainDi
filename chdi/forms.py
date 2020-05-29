from django import forms
from django.forms import ModelForm
from .models import Template

class TemplateCreateForm(forms.Form):
   # user_name = forms.CharField(required=True, label="Имя сотрудника", initial="Имя")
   # user_image = forms.ImageField(required=True, label="Изображение подписи сотрудника")
    diplom_name = forms.CharField(required=True, label="Наименование диплома", initial="Диплом бакалавра", widget=forms.TextInput(attrs={'class':'myfield'}))
    diplom_descr = forms.CharField(required=True, label="Описание", initial="Присвоена квалификация (степень) Бакалавр по направлению подготовки 090304 Программная инженерия", widget=forms.Textarea(attrs={'class':'myfield_text_area'}))
   # diplom_image = forms.ImageField(required=True, label="Изображение организации")
    org_name = forms.CharField(required=True, label="Наименование организации", initial="Южно-Уральский государственный университет", widget=forms.TextInput(attrs={'class':'myfield'}))
    org_url = forms.URLField(required=True, label="Сайт организации",  initial="https://www.susu.ru/", widget=forms.URLInput(attrs={'class':'myfield'}))
    org_email = forms.EmailField(required=True, label="Почта организации", initial="info@susu.ru", widget=forms.EmailInput(attrs={'class':'myfield'}))
   # org_image = forms.ImageField(required=True, label="Печать организации")

class TemplateSignForm(forms.Form):
   user_template = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'myfield'}), queryset=Template.objects.all(), label="Шаблон")
   roster = forms.FileField(required=True, label="", widget=forms.FileInput(attrs={'style':'display: none;', 'accept': '.csv'}))

   def __init__(self, tUser, *args, **kwargs):
       super(TemplateSignForm, self).__init__(*args, **kwargs)
       self.fields['user_template'].queryset = Template.objects.filter(user__exact=tUser)

class TemplateRecallForm(forms.Form):
    diplom_file = forms.FileField(required=True, label= "", widget=forms.FileInput(attrs={'style':'display: none;', 'accept': 'application/json'}))

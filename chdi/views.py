from django.shortcuts import render
from .models import Template
from tdiplom.create_diplom import TemplateJson
from pdiplom.issuer_diplom import sign_diplom, connection_on, connection_rpc_on
from rdiplom.recall_diplom import recall_diplom
from vdiplom.verifier import verify_diplom
from vdiplom.diplom_formatter import get_formatted_award_and_verification_info
from chdi.forms import TemplateCreateForm, TemplateSignForm, TemplateRecallForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
import os
import logging
import zipfile
from django.shortcuts import redirect
from django.core.files import File
import base64
from django.contrib.auth.models import User

PREFIX_UID = "urn:uuid:"

def index(request):
    if request.method == 'POST':
        if connection_rpc_on() == False:
            error = 'Нет связи с сервером'
            return render(
                request,
                'connection_error.html',
                {'error': error}
            )
        file = request.FILES['filesjson']
        json_byte_file = file.read()
        json_file = json_byte_file.decode()

        m1, m2 = verify_diplom(json_file)
        if m1 == 'exist' and m2 =='same':
            verify_response = 1
        elif m1 == 'recalled':
            verify_response = 2
        else:
            verify_response = 0

        award = get_formatted_award_and_verification_info(json_file, verify_response)

        return render(
            request,
            'award.html',
            award
        )
    return render(
        request,
        'index.html',
    )

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views import generic


class TemplateListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of templates."""
    model = Template

    def get_queryset(self):
        return Template.objects.filter(user=self.request.user)

class TemplateDetailView(LoginRequiredMixin, DetailView):
    """Generic class-based detail view for a template."""
    fields = ['user_jobtitle', 'diplom_name', 'diplom_descr', 'org_name', 'org_url', 'org_email']
    model = Template

class TemplateDelete(LoginRequiredMixin, DeleteView):
    model = Template
    success_url = reverse_lazy('templates')
    #permission_required = 'catalog.can_mark_returned'
    success_url = '/chdi/templates/'

@login_required
def CreateTemplate(request):
    if request.method == 'POST':
        form = TemplateCreateForm(request.POST)
        if form.is_valid():
            diplom_name = form.cleaned_data.get("diplom_name")
            diplom_description = form.cleaned_data.get("diplom_descr")
            org_name = form.cleaned_data.get("org_name")
            org_url = form.cleaned_data.get("org_url")
            org_email = form.cleaned_data.get("org_email")
            user_jobtitle = request.user.profile.job
            user_name = request.user.last_name  +" " + request.user.first_name + " " + request.user.profile.patronymic
            template = TemplateJson()
            template.diplom_name = diplom_name
            template.diplom_description = diplom_description
            template.org_name = org_name
            template.org_url = org_url
            template.org_email = org_email
            template.user_jobtitle = user_jobtitle
            template.user_name = user_name
            ditemp = template.create_diplom_template()
            json_data = json.dumps(ditemp)
            bd_temp = Template(user_id=request.user.id,diplom_name=diplom_name, diplom_descr=diplom_description, org_name=org_name, org_url=org_url, org_email=org_email, user_name=user_name, user_jobtitle=user_jobtitle, json_data=json_data)
            bd_temp.save()
            return HttpResponseRedirect(reverse('templates'))
    else:
        form = TemplateCreateForm()
    return render(
        request,
        'create_template.html',
        {'form': form}
    )

def handle_upload_file(f, user_id, itr=0):
    dest = './chdi/files/roster' + str(user_id) + str(itr) +'.csv'
    if os.path.exists(dest):
        os.remove(dest)
    with open(dest, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return dest


def handle_file_json(diplom_json, diplom_id, rec_name):
    dest_json = './chdi/files/json/'+str(diplom_id)+'_'+str(rec_name)+'.json'
    name = str(diplom_id)+'_'+str(rec_name)+'.json'
    with open(dest_json, 'w') as destination:
        json.dump(diplom_json, destination)
    return dest_json, name

def handler_upload_file_zip(user_id, destinations_json):
    dest_zip = './chdi/files/zip/filezip' + str(user_id) + '.zip'
    z = zipfile.ZipFile(dest_zip, 'w')
    for d in destinations_json:
        z.write(d)
    z.close()
    return dest_zip

ZIPFILE_NAME = 'archive.zip'
@login_required
def SignTemplate(request):
    user_id = request.user.id
    if request.method == 'POST':
        form = TemplateSignForm(request.POST, request.FILES, tUser=user_id)
        if form.is_valid():
            if connection_rpc_on() == False:
                error = 'Нет связи с сервером'
                return render(
                    request,
                    'connection_error.html',
                    {'error': error}
                )

            template = request.POST['user_template']
            diplom_template = Template.objects.get(pk=template)
            dest = handle_upload_file(request.FILES['roster'], user_id)
            diploms, messages = sign_diplom(dest, diplom_template.json_data)
            response = HttpResponse(content_type='application/zip')
            z = zipfile.ZipFile(response, 'w')
            for diplom in diploms:
                diplom_id = diploms[diplom]['id'].replace(PREFIX_UID, "")
                rec_name = diploms[diplom]['recipientProfile']['name']
                dest_json, file_json_name = handle_file_json(diploms[diplom],diplom_id, rec_name)
                z.write(dest_json,file_json_name )
                os.remove(dest_json)
            os.remove(dest)
            response['Content-Disposition'] = f'attachment; filename={ZIPFILE_NAME}'
            return response
    else:
        form = TemplateSignForm(tUser=user_id)
    return render(
        request,
        'sign_template.html',
        {'form': form}
    )

def handle_upload_json(f):
    diplom_json = f.read()
    diplom = json.loads(diplom_json)
    return diplom
@login_required
def RecallTemplate(request):
    if request.method == 'POST':
        form = TemplateRecallForm(request.POST, request.FILES)
        if form.is_valid():
            if connection_rpc_on() == False:
                error = 'Нет связи с сервером'
                return render(
                    request,
                    'connection_error.html',
                    {'error': error}
                )
            diplom = handle_upload_json(request.FILES['diplom_file'])
            diplom_id = diplom['id'].replace(PREFIX_UID, "")
            result = recall_diplom(diplom_id)

    else:
        form = TemplateRecallForm()
    return render(
        request,
        'recall_diplom.html',
        {'form': form}
    )


@login_required
def WatchProfile(request):
    user = request.user
    return render(
        request,
        'profile.html',
        {'user': user}
    )





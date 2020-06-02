from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('templates/', views.TemplateListView.as_view(), name='templates'),
    path('sign/', views.sign_template, name='template_sign'),
    path('recall/', views.recall_template, name='template_recall'),
    path('profile/', views.watch_profile, name='profile'),
]

urlpatterns += [
    path('template/<int:pk>', views.TemplateDetailView.as_view(), name='template-detail'),
    path('template/<int:pk>/delete/', views.TemplateDelete.as_view(), name='template_delete'),
    path('template/create/', views.create_template, name='template_create'),
]
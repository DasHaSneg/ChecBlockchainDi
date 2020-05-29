from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('templates/', views.TemplateListView.as_view(), name='templates'),
    path('sign/', views.SignTemplate, name='template_sign'),
    path('recall/', views.RecallTemplate, name='template_recall'),
    path('profile/', views.WatchProfile, name='profile'),
]

urlpatterns += [
    path('template/<int:pk>', views.TemplateDetailView.as_view(), name='template-detail'),
    path('template/<int:pk>/delete/', views.TemplateDelete.as_view(), name='template_delete'),
    path('template/create/', views.CreateTemplate, name='template_create'),
]
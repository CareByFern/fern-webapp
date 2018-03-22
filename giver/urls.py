from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('face/', views.face, name='face'),
    path('thanks/', views.thanks, name='thanks'),
    path('charge/<int:chargeid>/', views.charge, name='operate'),
    path('aide/', views.aide_hub, name='aide_hub'),
    path('fam/', views.fam_hub, name='fam_hub'),
    path('api/update_status.json', views.update_status, name='update_status'),
]

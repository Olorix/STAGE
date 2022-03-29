from django.urls import path

from . import views

app_name = 'paf'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('basket/', views.basket, name='basket'),
    path('ajax/selection/add', views.ajax_add_to_selection, name='add_to_selection'),
    path('ajax/selection/remove', views.ajax_remove_from_selection, name='remove_from_selection'),
    path('ajax/metier/<slug:pk>/', views.AjaxMetierLoad.as_view(), name='metier_load'),
    path('ajax/module/<int:pk>/', views.AjaxModuleDetail.as_view(), name='module_detail'),
]

"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Главная страница — список инструментов
    path('', views.InstrumentListView.as_view(), name='instrument_list'),

    # Инструменты
    path('instruments/create/', views.InstrumentCreateView.as_view(), name='instrument_create'),
    path('instruments/<int:pk>/', views.InstrumentDetailView.as_view(), name='instrument_detail'),
    path('instruments/<int:pk>/update/', views.InstrumentUpdateView.as_view(), name='instrument_update'),
    path('instruments/<int:pk>/delete/', views.InstrumentDeleteView.as_view(), name='instrument_delete'),

    # Ремонтники
    path('repairers/', views.RepairerListView.as_view(), name='repairer_list'),
    path('repairers/create/', views.RepairerCreateView.as_view(), name='repairer_create'),
    path('repairers/<int:pk>/', views.RepairerDetailView.as_view(), name='repairer_detail'),
    path('repairers/<int:pk>/update/', views.RepairerUpdateView.as_view(), name='repairer_update'),

    # Ремонты
    path('repairs/', views.RepairListView.as_view(), name='repair_list'),
    path('repairs/create/', views.RepairCreateView.as_view(), name='repair_create'),
    path('repairs/<int:pk>/', views.RepairDetailView.as_view(), name='repair_detail'),
    path('repairs/<int:pk>/update/', views.RepairUpdateView.as_view(), name='repair_update'),

    # Перемещения
    path('relocations/', views.RelocationListView.as_view(), name='relocation_list'),
    path('relocations/create/', views.RelocationCreateView.as_view(), name='relocation_create'),
]
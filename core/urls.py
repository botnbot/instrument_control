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

from core.views import (
    HomeView,

    InstrumentsListView,
    InstrumentsCreateView,
    InstrumentsDetailView,
    InstrumentsUpdateView,
    InstrumentsDeleteView,

    RepairersCreateView,
    RepairersListView,
    RepairersDetailView,
    RepairersUpdateView,
    RepairersDeleteView,

    RepairsCreateView,
    RepairsListView,
    RepairsDetailView,
    RepairsUpdateView,
    RepairsDeleteView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('instruments/', InstrumentsListView.as_view(), name='instrument_list'),
    path('instruments/create/', InstrumentsCreateView.as_view(), name='instrument_create'),
    path('instruments/<int:pk>/', InstrumentsDetailView.as_view(), name='instrument_detail'),
    path('instruments/<int:pk>/update/', InstrumentsUpdateView.as_view(), name='instrument_edit'),
    path('instruments/<int:pk>/delete/', InstrumentsDeleteView.as_view(), name='instrument_delete'),

    path('repairers/', RepairersListView.as_view(), name='repairer_list'),
    path('repairers/create/', RepairersCreateView.as_view(), name='repairer_create'),
    path('repairers/<int:pk>/', RepairersDetailView.as_view(), name='repairer_detail'),
    path('repairers/<int:pk>/update/', RepairersUpdateView.as_view(), name='repairer_update'),
    path('repairers/<int:pk>/delete/', RepairersDeleteView.as_view(), name='repairer_delete'),

    path('repairs/', RepairsListView.as_view(), name='repair_list'),
    path('repairs/create/', RepairsCreateView.as_view(), name='repair_create'),
    path('repairs/<int:pk>/', RepairsDetailView.as_view(), name='repair_detail'),
    path('repairs/<int:pk>/update/', RepairsUpdateView.as_view(), name='repair_update'),
    path('repairs/<int:pk>/delete/', RepairsDeleteView.as_view(), name='repair_delete'),
]

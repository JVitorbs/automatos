from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("historico/", views.history_view, name="history"),
    path("exportacao/", views.export_view, name="export"),
]

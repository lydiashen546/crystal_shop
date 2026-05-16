from django.urls import path

from . import views


urlpatterns = [
    path("", views.crystal_list, name="crystals"),
    path("<int:crystal_id>/", views.crystal_detail, name="crystal_detail"),
]

from django.contrib import admin
from django.urls import path, include

from data_api.views import Ndvi

urlpatterns = [
    path('get_ndvi_by_date_polygon/', Ndvi.as_view()),
]
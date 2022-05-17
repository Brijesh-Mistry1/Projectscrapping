# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from django.contrib import admin

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

admin.site.site_header = "Project Erasmus Administration"
admin.site.site_title = "Project Erasmus Administration"
admin.site.index_title = "Welcome to Project Erasmus Administration"
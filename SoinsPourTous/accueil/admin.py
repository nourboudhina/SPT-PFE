from typing import __all__
from django.contrib import admin
from django.contrib.admin import register

from .models import PageAcceuil


@admin.register(PageAcceuil)
class PageAcceuilAdmin(admin.ModelAdmin):
    list_display = ['postwithimage', 'postwithtet']


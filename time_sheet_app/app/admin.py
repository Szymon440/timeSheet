from django.contrib import admin
from .models import Raport


@admin.register(Raport)
class RaportsAdmin(admin.ModelAdmin):

    def data(self, obj):
        return obj.Raport.data

    def time_start(self, obj):
        return obj.Raport.time_start

    def time_end(self, obj):
        return obj.Raport.time_end

    def description(self, obj):
        return obj.Raport.description

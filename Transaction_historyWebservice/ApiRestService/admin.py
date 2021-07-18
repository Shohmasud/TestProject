from django.contrib import admin
from .models import *
# Register your models here.


class File_Name(admin.ModelAdmin):
    list_display = ('id', 'name_file')
    search_fields = ('id', 'name_file')
admin.site.register(fileName, File_Name)



class Response(admin.ModelAdmin):
    list_display = ('id','username','spent_money', 'gems')
    search_fields = ('id','username','spent_money', 'gems')
admin.site.register(response, Response)
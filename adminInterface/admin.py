from django.contrib import admin

# Register your models here.
from .models import Articles,Questions,Report

class ArticlesAdmin(admin.ModelAdmin):
    list_filter = ['author','date_added']

class QuestionsAdmin(admin.ModelAdmin):
    list_filter = ['answered']

admin.site.register(Articles,ArticlesAdmin)
admin.site.register(Questions,QuestionsAdmin)
admin.site.register(Report)
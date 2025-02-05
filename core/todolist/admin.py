from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('user' , 'title', 'completed' , 'created_date')
    list_filter = ('user',)
    search_fields = ('user',)

admin.site.register(Task,TaskAdmin)
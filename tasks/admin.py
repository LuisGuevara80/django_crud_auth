from django.contrib import admin
from .models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', ) # se coloca created ya que solo ese campo es de lectura y la "," se pone porque es una tupla en el "Task Model explica esto"

admin.site.register(Task, TaskAdmin)

# luigi, luigi123

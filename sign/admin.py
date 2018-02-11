from django.contrib import admin
from sign.models import Event, Guest, test1


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'address', 'start_time']
    search_fields = ['name']
    list_filter = ['status']

# Register your models here.
admin.site.register(Event, EventAdmin)
admin.site.register(Guest)
admin.site.register(test1)
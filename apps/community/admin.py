from apps.community.models import Event, EventType
from django.contrib import admin

class SlugOnlyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Event, SlugOnlyAdmin)
admin.site.register(EventType, SlugOnlyAdmin)

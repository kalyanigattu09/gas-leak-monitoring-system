from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'current_gas_level', 'current_status')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    ordering = ('name',)

    @admin.display(description='Gas Level')
    def current_gas_level(self, obj):
        return obj.current_gas_level or '—'

    @admin.display(description='Status')
    def current_status(self, obj):
        return obj.current_status

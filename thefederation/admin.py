from django.contrib import admin

from thefederation.models import Node, Platform, Protocol, Service, Stat


class NodeAdmin(admin.ModelAdmin):
    pass


class PlatformAdmin(admin.ModelAdmin):
    pass


class ProtocolAdmin(admin.ModelAdmin):
    pass


class ServiceAdmin(admin.ModelAdmin):
    pass


class StatAdmin(admin.ModelAdmin):
    pass


admin.site.register(Node, NodeAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Stat, StatAdmin)

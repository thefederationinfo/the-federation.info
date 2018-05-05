from django.contrib import admin

from thefederation.models import Node, Platform, Protocol, Service, Stat


class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'platform', 'version', 'last_success', 'open_signups', 'relay', 'country',
                    'hide_from_list', 'blocked')
    list_display_links = ('name', 'host')
    list_filter = ('platform', 'version', 'open_signups', 'relay', 'country', 'hide_from_list', 'blocked')
    search_fields = ['name', 'host', 'version', 'ip', 'features', 'server_meta',
                     'organization_account', 'organization_contact', 'organization_name']


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'license')
    list_display_links = ('display_name', 'name')
    list_filter = ('license', 'version_clean_style')
    search_fields = ['display_name', 'name', 'description', 'tagline']


class ProtocolAdmin(admin.ModelAdmin):
    pass


class ServiceAdmin(admin.ModelAdmin):
    pass


class StatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'node', 'platform', 'protocol')
    list_filter = ('platform', 'protocol')
    search_fields = ['date', 'node__name']


admin.site.register(Node, NodeAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Stat, StatAdmin)

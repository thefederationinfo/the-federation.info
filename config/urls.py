from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    url(r"", include("thefederation.urls")),

    # JavaScript translations
    path("jsi18n/", JavaScriptCatalog.as_view(packages=['thefederation']), name="javascript-catalog"),

    # Admin pages
    url(settings.ADMIN_URL, admin.site.urls),
    url(r"^django-rq/", include("django_rq.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r"^400/$", default_views.bad_request, kwargs={"exception": Exception("Bad Request!")}),
        url(r"^403/$", default_views.permission_denied, kwargs={"exception": Exception("Permission Denied")}),
        url(r"^404/$", default_views.page_not_found, kwargs={"exception": Exception("Page not Found")}),
        url(r"^500/$", default_views.server_error),
    ]
    if settings.DEBUG_TOOLBAR_ENABLED:
        import debug_toolbar
        urlpatterns += [
            url(r"^__debug__/", include(debug_toolbar.urls)),
        ]

from django.urls import path

from thefederation.views import register_view, mass_register_view, legacy_pods_json_view

urlpatterns = [
    path("massregister/", mass_register_view, name="massregister"),
    path("register/<host>/", register_view),

    # Social-Relay uses this
    path("pods.json", legacy_pods_json_view, name="pods_json"),
]

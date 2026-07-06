from django.urls import path

from thefederation.views import register_view, legacy_pods_json_view

urlpatterns = [
    path("register/<host>/", register_view),
    # Social-Relay uses this
    path("pods.json", legacy_pods_json_view, name="pods_json"),
]

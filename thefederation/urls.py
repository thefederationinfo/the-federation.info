from django.urls import path

from thefederation.views import register_view

urlpatterns = [
    path("register/<host>/", register_view),
]

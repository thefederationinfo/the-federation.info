from django.urls import path

from thefederation.views import register_view, mass_register_view

urlpatterns = [
    path("massregister/", mass_register_view, name="massregister"),
    path("register/<host>/", register_view),
]

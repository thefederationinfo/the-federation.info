from django.http import JsonResponse
from django.shortcuts import redirect

from thefederation import registration
from thefederation.models import Node


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        # nginx sets this, first entry is the client
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def register_view(request, host):
    json = True if request.content_type == "application/json" else False
    result, host = registration.register_node(host, client_ip=_client_ip(request))
    if result == registration.OK:
        if json:
            return JsonResponse({"error": None})
        return redirect(f"/node/{host}")
    if result == registration.RATE_LIMITED:
        if json:
            return JsonResponse({"error": "Too many requests, try again later."}, status=429)
        return redirect("/")
    if json:
        return JsonResponse({"error": "Invalid hostname!"})
    # TODO show an error or something
    return redirect("/")


def legacy_pods_json_view(request):
    """
    Legacy pods.json route from the old version of this site

    Turns out someone did use it - the Social-Relay. Bring it back until that is rewritten.
    """
    nodes = list(Node.objects.active().values("host"))
    return JsonResponse({"pods": nodes})

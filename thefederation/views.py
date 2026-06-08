from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import redirect

from thefederation.models import Node
from thefederation.tasks import poll_node
from thefederation.utils import is_valid_hostname, clean_hostname


def register_view(request, host):
    json = True if request.content_type == "application/json" else False
    # TODO rate limit this view per caller ip?
    host = clean_hostname(host)
    # Validate cheaply, then queue the poll instead of fetching the remote
    # node inline. Polling synchronously blocked the gunicorn worker for the
    # whole remote fetch, so a slow node would exceed the worker timeout and
    # get killed (WORKER TIMEOUT). Queue it like mass_register_view does.
    if is_valid_hostname(host):
        poll_node.delay(host)
        if json:
            return JsonResponse({'error': None})
        return redirect(f"/node/{host}")
    if json:
        return JsonResponse({'error': 'Invalid hostname!'})
    # TODO show an error or something
    return redirect("/")


@staff_member_required
def mass_register_view(request):
    input = request.POST.get('domain-list')
    if not input:
        return redirect('admin:app_list', app_label="thefederation")

    lines = input.split('\n')
    lines = [line for line in lines if len(line.strip())]
    domains = []
    for line in lines:
        domains += line.split(',')

    domains = {clean_hostname(domain) for domain in domains}
    domains = {domain for domain in domains if is_valid_hostname(domain)}

    for domain in domains:
        poll_node.delay(domain)

    messages.info(request, f"Triggered job to register {len(domains)} domains!")

    return redirect('admin:app_list', app_label='thefederation')


def legacy_pods_json_view(request):
    """
    Legacy pods.json route from the old version of this site

    Turns out someone did use it - the Social-Relay. Bring it back until that is rewritten.
    """
    nodes = list(Node.objects.active().values('host'))
    return JsonResponse({'pods': nodes})

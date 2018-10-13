from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import redirect

from thefederation.models import Node
from thefederation.tasks import poll_node
from thefederation.utils import is_valid_hostname


def register_view(request, host):
    # TODO rate limit this view per caller ip?
    if not is_valid_hostname:
        return redirect("/")
    if poll_node(host):
        # Success!
        return redirect(f"/node/{host}")
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

    domains = {domain.strip() for domain in domains}

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

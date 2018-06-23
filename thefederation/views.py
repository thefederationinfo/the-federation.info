from django.shortcuts import redirect

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


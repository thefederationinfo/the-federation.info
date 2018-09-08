{% load math %}#### Daily statistics from The Federation

##### Count of nodes

Total count of nodes per platform and change from 30 days.

{% for platform in platform_nodes|dictsortreversed:"percentage" %}
* {{ platform.name }}: {{ platform.value }} (share: {{ platform.percentage|floatformat }}%, value change: {{ platform.change }}){% endfor %}

For more statistics visit [the-federation.info](https://the-federation.info)

#thefederationstatsdaily

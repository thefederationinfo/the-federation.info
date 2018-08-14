{% load math %}#### Daily statistics from The Federation

##### Platform distribution

Percentage of nodes per platform.

{% for platform in platform_nodes|dictsortreversed:"percentage" %}
* {{ platform.name }}: {{ platform.percentage|floatformat }}%{% endfor %}

For more detailed statistics visit [the-federation.info](https://the-federation.info)

#thefederationstatsdaily

{% load math %}#### Daily statistics from The Federation

##### Platform distribution

Percentage of active users per platform and change from 30 days ago.

###### Active users

{% for platform in platform_users|dictsortreversed:"percentage" %}
* {{ platform.name }}: {{ platform.percentage|floatformat }}%{% endfor %}

For more detailed statistics visit [the-federation.info](https://the-federation.info)

#thefederationstatsdaily

{% load math %}#### Daily statistics from The Federation

##### Active users

Active users per platform and change from 30 days ago.

{% for platform in platform_users|dictsortreversed:"value" %}
* {{ platform.name }}: {{ platform.value }} (share: {{ platform.percentage|floatformat }}%, value change: {{ platform.old_value }}){% endfor %}

For more statistics visit [the-federation.info](https://the-federation.info)

#thefederationstatsdaily

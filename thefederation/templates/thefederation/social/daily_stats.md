{% load math %}#### Daily statistics from The Federation

##### Global counts

Current values and change from 30 days ago.

* Nodes: {{ nodes.count }} ({{ nodes.count|subtract:prevnodes.count|with_sign }})
* Active users (6 months): {{ stat.users_half_year }} ({{ stat.users_half_year|subtract:prevstat.users_half_year|with_sign }})
* Active users (30 days): {{ stat.users_monthly }} ({{ stat.users_monthly|subtract:prevstat.users_monthly|with_sign }})
* Total user accounts: {{ stat.users_total }} ({{ stat.users_total|subtract:prevstat.users_total|with_sign }})

##### Platform distribution

Distribution of nodes and users per platform and change from 30 days ago.

###### Nodes

{% for platform in platform_nodes|dictsortreversed:"percentage" %}
* {{ platform.name }}: {{ platform.percentage|floatformat }}% ({{ platform.change|floatformat|with_sign }}%){% endfor %}

###### Active users

{% for platform in platform_users|dictsortreversed:"percentage" %}
* {{ platform.name }}: {{ platform.percentage|floatformat }}% ({{ platform.change|floatformat|with_sign }}%){% endfor %}

For more detailed statistics visit [the-federation.info](https://the-federation.info)

#thefederationstatsdaily

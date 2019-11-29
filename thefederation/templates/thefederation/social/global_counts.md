{% load math %}#### Daily statistics from The Federation / Fediverse

##### Global network counts for all platforms

Current values and change from 30 days ago.

* Nodes: {{ nodes.count }} ({{ nodes.count|subtract:prevnodes.count|with_sign }})
* Active users (6 months): {{ stat.users_half_year }} ({{ stat.users_half_year|subtract:prevstat.users_half_year|with_sign }})
* Active users (30 days): {{ stat.users_monthly }} ({{ stat.users_monthly|subtract:prevstat.users_monthly|with_sign }})
* Total user accounts: {{ stat.users_total }} ({{ stat.users_total|subtract:prevstat.users_total|with_sign }})

For more statistics visit [the-federation.info](https://the-federation.info)

#fediversestats #fediversestatsdaily #thefederationstatsdaily

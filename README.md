[![Stories in Ready](https://badge.waffle.io/jaywink/the-federation.info.png?label=ready&title=Ready)](https://waffle.io/jaywink/the-federation.info) [![chat on freenode](https://img.shields.io/badge/chat-on%20freenode-brightgreen.svg)](http://webchat.freenode.net?channels=%23thefederation&uio=d4) [![Chat on Gitter](https://badges.gitter.im/the-federation-info/Lobby.svg)](https://gitter.im/the-federation-info/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![chat on matrix](https://img.shields.io/badge/chat-on%20matrix-orange.svg)](https://riot.im/app/#/room/#thefederation:matrix.org) [![](https://img.shields.io/badge/license-AGPLv3-green.svg)](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0))

# The-Federation.info

Statistics hub and node list for the Fediverse. Currently tracking projects using the Diaspora protocol, including:
 
 * diaspora*
 * Friendica
 * Hubzilla
 * GangGo
 * Socialhome
 
Tracking of ActivityPub and OStatus protocols is planned.

**NOTE! This branch is part of a site rewrite. For current production version, see master branch.**

Site found at: https://the-federation.info

## Contributing

TBD

## Tech stack

* Node 9
* Python 3.6
* Django 2.0
* PostgreSQL
* Vue 2
* Webpack

## Backend

### Dependencies

``` bash
pip install -U pip setuptools pip-tools
pip-sync dev-requirements.txt
```

### DB

``` bash
sudo su - postgres
createuser -s -P thefederation  # give password 'thefederation'
createdb -O thefederation thefederation
exit
python manage.py migrate
```

## Frontend

### Build Setup

``` bash
# install dependencies
npm i

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Authors

* Jason Robinson / @jaywink / https://jasonrobinson.me
* Flaburgan / @Flaburgan

See [other awesome contributors](https://github.com/thefederationinfo/the-federation.info/graphs/contributors)!

## License

AGPLv3

[![Stories in Ready](https://badge.waffle.io/jaywink/the-federation.info.png?label=ready&title=Ready)](https://waffle.io/jaywink/the-federation.info) [![chat on matrix](https://img.shields.io/badge/chat-on%20matrix-orange.svg)](https://matrix.to/#/#feneas:feneas.org) [![](https://img.shields.io/badge/license-AGPLv3-green.svg)](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0))

# The-Federation.info

Tracking various projects using the Diaspora, ActivityPub, OStatus and other protocols.

Site found at: https://the-federation.info

## How to get your platform listed

Implement NodeInfo, NodeInfo2, Statistics.json or Mastodon stats API endpoint.

### OK, I've done that, what now?

Register your node here, for example `https://the-federation.info/register/mynode.tld`. If it is a success, you're good! If your platform is new, or you want to update an existing platform information, raise an issue providing the following:

* URL to code
* Description
* Display name
* Code license
* Icon
* URL to install guide
* Tagline
* URL to official website

If it's closed source, leave out link to code and install guide. Icon can be any size, currently only using 16px. Possibly will have a larger image at some point on the platform page. Tagline is a kind of short one sentence marketing line, see other platforms.

## Tech stack

* Node 9
* Python 3.6
* Django 2.0
* PostgreSQL
* Vue 2
* Webpack
* GraphQL

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

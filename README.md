[![](https://img.shields.io/matrix/thefederation:feneas.org.svg?server_fqdn=feneas.org)](https://matrix.to/#/#thefederation:feneas.org) [![](https://img.shields.io/badge/license-AGPLv3-green.svg)](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0))

# IMPORTANT: This project is largely in low maintenance mode

If you wish to change that, **please become a contributor**. Active contributors will be awarded
full ownership of the code repository and if wanted, ownership of the domain too.
As original author and maintainer, I don't intend to work on this project much at all
in the future. I would however like it to live and pass on to other more enthusiastic
maintainers.

# The-Federation.info

Tracking various projects using the ActivityPub, Matrix, Diaspora, OStatus and other protocols.

Site found at: https://the-federation.info

## How to get your platform listed

The recommended metadata to implement is [NodeInfo2](https://git.feneas.org/jaywink/nodeinfo2).

Failing that, [NodeInfo](http://nodeinfo.diaspora.software/) works too.

Mastodon and Matrix instances are scraped with a dedicated scraper since they don't (yet) provide generic metadata.

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

### Code of Conduct

While interactions on our site is not possible, we expect sites we list to have a humane code of conduct in place. Should sites who fail to ban content that can be found generally harmful, that node will be blocked from listing here.

Harmful content can be, but not limited to, malware, graphical material of minorities, abusive images, hateful content, racist content and climate denialism. The admins of this site reserve the right to decide case by case on blocking of nodes. Please report any nodes violating our terms to the admins. 

## Tech stack

* Node 10
* Python 3.6
* Django 2.0
* PostgreSQL
* Vue 2
* Webpack
* GraphQL

## Development

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
yarn

# serve with hot reload at localhost:8080
yarn run dev

# build for production with minification
yarn run build
```

## Authors

* Jason Robinson / @jaywink / https://jasonrobinson.me / `@jaywink:federator.dev`
* Flaburgan / @Flaburgan

See [other awesome contributors](https://github.com/thefederationinfo/the-federation.info/graphs/contributors)!

## License

Source code: AGPLv3

### Third party

This product includes GeoLite2 data created by MaxMind, available from https://www.maxmind.com.

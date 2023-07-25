<template>
    <div>
        <Drawer />

        <main>
            <header class="main-header">
                <div class="main-title">
                    <h1>About</h1>
                    <h2>Behind the scenes</h2>
                </div>
            </header>
            <section class="tile">
                <header>
                    <h2>What is this site?</h2>
                </header>
                <div>
                    <p>
                        This site is for gathering statistics about nodes in the fediverse. Depending on the project,
                        exposed statistics might have to be activated separately. To appear on this list, the node
                        needs to be registered on this site separately, either manually or extracted from
                        another list of nodes.
                    </p>
                    <p>
                        The code is <a
                            href="https://codeberg.org/thefederationinfo/the-federation.info"
                            rel="noopener noreferrer"
                            @click="trackEvent('source_code_info')"
                        >
                            on Codeberg
                        </a> under AGPLv3. Please file bugs and ideas there if you want to - and of course pull
                        requests are welcome too.
                    </p>

                    <h3>Can I get a copy of the data?</h3>
                    <p>
                        It's all available as JSON, feel free to use any data you want! We cannot guarantee the
                        JSON will not change over time, though it should stay mostly stable. You can always let us
                        know if you depend on some JSON feed and we'll try our best not to break it.
                    </p>
                    <p>
                        All the data is available via a
                        <a
                            href="/graphql"
                            rel="noopener noreferrer"
                            @click="trackEvent('graphql_info')"
                        >
                            GraphQL
                        </a>
                        endpoint. (deprecated)
                        <br><br>
                        A new, more stable and faster endpoint is now available!<br>
                        To work with GraphiQL visit the
                        <a
                            href="https://cloud.hasura.io/public/graphiql"
                            rel="noopener noreferrer"
                            @click="trackEvent('graphiql_info')"
                        >
                            GraphiQL App
                        </a>
                        from Hasura and paste following url: <code>https://the-federation.info/v1/graphql</code>
                    </p>

                    <h3>How do I get my node listed?</h3>
                    <p>
                        For registering your node with this site, go to
                        <code>https://the-federation.info/register/&lt;yournode.tld&gt;</code>. After some seconds,
                        you will be redirected to the created node page. If this doesn't happen, something went
                        wrong when checking the node for data. Please contact us using the
                        <a
                            href="https://codeberg.org/thefederationinfo/the-federation.info"
                            rel="noopener noreferrer"
                            @click="trackEvent('source_code_info')"
                        >
                            Codeberg
                        </a>
                        issue tracker or in our
                        <a
                            href="https://matrix.to/#/#the-federation:matrix.org"
                            rel="noopener noreferrer"
                            @click="trackEvent('matrix_info')"
                        >
                            Matrix
                        </a>
                        channel.
                    </p>

                    <h3>Code of Conduct</h3>
                    <p>
                        While interactions on our site is not possible, we expect sites we list to have a humane code
                        of conduct in place. Should sites who fail to ban content that can be found generally harmful,
                        that node will be blocked from listing here.
                    </p>
                    <p>
                        Harmful content can be, but not limited to, malware, graphical material of minors, abusive
                        images, hateful content, racist content and climate denialism. The admins of this site reserve
                        the right to decide case by case on blocking of nodes. Please report any nodes violating our
                        terms to the admins.
                    </p>

                    <h3>Follow on The Federation / Fediverse</h3>
                    <p>
                        You can follow the
                        <a
                            href="https://socialhome.network/u/thefederation"
                            title="thefederation@socialhome.network"
                            @click="trackEvent('mastodon_info')"
                        >
                            official account</a> on The Federation to receive daily or weekly statistics. The posts
                        will be tagged according to frequency, so instead of following the account you can also
                        subscribe to the hashtags. The following hashtags will be used:
                    </p>
                    <blockquote>
                        <p>
                            <a
                                href="https://socialhome.network/tags/fediversestats/"
                                rel="noopener noreferrer"
                            >
                                #fediversestats
                            </a>
                        </p>
                        <p>
                            <a
                                href="https://socialhome.network/tags/fediversestatsdaily/"
                                rel="noopener noreferrer"
                            >
                                #fediversestatsdaily
                            </a>
                        </p>
                        <p>
                            <a
                                href="https://socialhome.network/tags/fediversestatsweekly/"
                                rel="noopener noreferrer"
                            >
                                #fediversestatsweekly
                            </a>
                        </p>
                        <p>
                            <a
                                href="https://socialhome.network/tags/thefederationstatsdaily/"
                                rel="noopener noreferrer"
                            >
                                #thefederationstatsdaily
                            </a>
                        </p>
                        <p>
                            <a
                                href="https://socialhome.network/tags/thefederationstatsweekly/"
                                rel="noopener noreferrer"
                            >
                                #thefederationstatsweekly
                            </a>
                        </p>
                    </blockquote>
                    <h3>Licence</h3>
                    <ul>
                        <li>
                            The Federation website code
                            <a
                                href="https://codeberg.org/thefederationinfo/the-federation.info"
                                rel="noopener noreferrer"
                                @click="trackEvent('source_code_info')"
                            >
                                on Codeberg
                            </a> (<a
                                href="https://www.gnu.org/licenses/agpl-3.0.en.html"
                                rel="noopener noreferrer"
                            >AGPLv3</a>)
                        </li>
                        <li>
                            Blur background image
                            <a
                                href="https://www.flickr.com/photos/voidobjects/6204459845/"
                                rel="noopener noreferrer"
                            >
                                by Teppo Kotirinta on flickr
                            </a> (<a
                                href="https://creativecommons.org/licenses/by/2.0/"
                                rel="noopener noreferrer"
                            >CC-BY</a>)
                        </li>
                        <li>
                            The font used is
                            <a
                                href="http://www.latofonts.com/lato-free-fonts/"
                                rel="noopener noreferrer"
                            >
                                lato
                            </a> (<a
                                href="http://scripts.sil.org/OFL"
                                rel="noopener noreferrer"
                            >SIL Open Font License 1.1</a>)
                        </li>
                    </ul>

                    <br>
                    <h3>Privacy Policy</h3>
                    <p>
                        We use <a
                            href="https://umami.is"
                            rel="noopener noreferrer"
                        >
                            Umami
                        </a>
                        to get a very anonymized view of how you use this page.
                        You can see all data we have collected
                        <a
                            href="https://umami.crapstone.xyz/share/JqltAQUexefik4oT/The-Federation"
                            rel="noopener noreferrer"
                            @click="trackEvent('umami_info')"
                        >
                            here
                        </a>.
                    </p>
                    <p>
                        To disable tracking enable <a
                            href="https://en.wikipedia.org/wiki/Do_Not_Track"
                            rel="noopener noreferrer"
                        >
                            Do-Not-Track
                        </a>
                        in your browser or block the domain <code>umami.crapstone.xyz</code>.
                    </p>

                    <p class="center">
                        Hosted with &lt;3 by
                        <a
                            href="https://codeberg.org/6543"
                            rel="noopener noreferrer"
                        >
                            6543
                        </a>,
                        <a
                            href="https://codeberg.org/crapStone"
                            rel="noopener noreferrer"
                        >
                            crapStone
                        </a>
                        &amp;
                        <a
                            href="https://codeberg.org/Epsilon_02"
                            rel="noopener noreferrer"
                        >Epsilon_02</a>
                    </p>
                </div>
            </section>
        </main>

        <Footer />
    </div>
</template>

<script>
import Drawer from "./common/Drawer"
import Footer from "./common/Footer"
import {trackEvent} from "../tracker"

export default {
    name: "InfoPage",
    components: {Drawer, Footer},
    methods: {
        trackEvent,
    },
}
</script>

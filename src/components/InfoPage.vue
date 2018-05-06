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
                        exposed statistics might have to be separately activated. To appear on this list, the node
                        needs to be separately registered on this site, either manually or extracted from
                        another list of nodes.
                    </p>
                    <p>
                        The code is <a
                            href="https://github.com/thefederationinfo/the-federation.info"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            in GitHub
                        </a> under AGPLv3. Please file bugs and ideas there if you want to - and of course pull
                        request are welcome too.
                    </p>

                    <h3>Can I get a copy of the data?</h3>
                    <p>
                        It's all available as JSON, feel free to use any data you want! We cannot guarantee the
                        JSON will not change over time, though it should mostly stay stable. You can always let us
                        know if you depend on some JSON feed and we'll make sure not to break it.
                    </p>
                    <p>
                        All the data is available via a <a href="/graphql">GraphQL</a> endpoint.
                    </p>


                    <h3>How do I get my node listed?</h3>
                    <p>
                        For registering your node with this site, go to
                        <code>https://the-federation.info/register/&lt;yournode.tld&gt;</code>. After some seconds,
                        you will be redirected to the created node page. If this doesn't happen, something went
                        wrong when checking the node for data. Please contact us using the GitHub issue tracker.
                    </p>

                    <h3>Follow on The Federation</h3>
                    <p>
                        You can follow the
                        <a href="https://socialhome.network/u/thefederation" title="thefederation@socialhome.network">
                        official account</a> on The Federation to receive daily or weekly statistics. The posts will be
                        tagged according to frequency, so instead of following the account you can also subscribe to
                        the hashtags. The following hashtags will be used:
                    </p>
                    <blockquote>
                        <p><a href="https://socialhome.network/tags/thefederationstatsdaily/">
                            #thefederationstatsdaily
                        </a></p>
                        <p><a href="https://socialhome.network/tags/thefederationstatsweekly/">
                            #thefederationstatsweekly
                        </a></p>
                    </blockquote>
                    <h3>Licence</h3>
                    <ul>
                        <li>The Federation website code
                            <a
                                href="https://github.com/thefederationinfo/the-federation.info"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                on GitHub
                            </a> (<a
                                href="https://www.gnu.org/licenses/agpl-3.0.en.html"
                                target="_blank"
                                rel="noopener noreferrer"
                            >AGPLv3</a>)
                        </li>
                        <li>Blur background image
                            <a
                                href="https://www.flickr.com/photos/voidobjects/6204459845/"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                by Teppo Kotirinta on flickr
                            </a> (<a
                                href="https://creativecommons.org/licenses/by/2.0/"
                                target="_blank"
                                rel="noopener noreferrer"
                            >CC-BY</a>)
                        </li>
                        <li>The font used is
                            <a
                                href="http://www.latofonts.com/lato-free-fonts/"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                lato
                            </a> (<a
                                href="http://scripts.sil.org/OFL"
                                target="_blank"
                                rel="noopener noreferrer"
                            >SIL Open Font License 1.1</a>)
                        </li>
                    </ul>

                    <p class="center">Hosted with &lt;3 by
                        <a
                            href="https://jasonrobinson.me"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Jason Robinson
                        </a>
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

export default {
    name: "InfoPage",
    components: {Drawer, Footer},
}
</script>

<style scoped>

</style>

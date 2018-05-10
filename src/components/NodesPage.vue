<template>
    <div>
        <Drawer />
        <NodesContent />
        <Footer />
    </div>
</template>

<script>
import Drawer from "./common/Drawer"
import Footer from "./common/Footer"
import NodesContent from "./NodesContent"

export default {
    name: 'NodesPage',
    components: {NodesContent, Footer, Drawer},
}
</script>

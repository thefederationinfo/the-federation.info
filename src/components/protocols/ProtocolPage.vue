<template>
    <div>
        <Drawer />
        <Footer />
    </div>
</template>

<script>
import Drawer from "../common/Drawer"
import Footer from "../common/Footer"

export default {
    name: "ProtocolPage",
    components: {Footer, Drawer},
}
</script>

<style scoped>

</style>

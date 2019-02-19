<template>
    <span>
        {{ number ? number.toLocaleString() : ' ' }}
    </span>
</template>

<script>
export default {
    name: "Number",
    props: {
        number: {
            type: Number,
            default: null,
        },
    },
}
</script>

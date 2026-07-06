<template>
  <div class="node-search">
    <input
      v-model="term"
      type="search"
      :placeholder="placeholder"
      @input="onInput"
      @keyup.enter="onEnter"
    />
  </div>
</template>

<script>
export default {
  name: "NodeSearchBox",
  props: {
    placeholder: {
      type: String,
      default: "Search nodes by name",
    },
    // How long to wait after the last keystroke before searching
    delay: {
      type: Number,
      default: 500,
    },
  },
  data() {
    return {
      term: "",
      timer: null,
    };
  },
  beforeDestroy() {
    clearTimeout(this.timer);
  },
  methods: {
    onInput() {
      // Lazy search: only fire once typing has paused
      clearTimeout(this.timer);
      this.timer = setTimeout(this.emitSearch, this.delay);
    },
    onEnter() {
      // Enter searches immediately
      clearTimeout(this.timer);
      this.emitSearch();
    },
    emitSearch() {
      this.$emit("search", this.term.trim());
    },
  },
};
</script>

<style scoped>
.node-search {
  margin-bottom: 10px;
}

.node-search input {
  width: 100%;
  max-width: 400px;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  box-sizing: border-box;
}
</style>

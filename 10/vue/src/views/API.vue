<template>
  <div>
    <!--- Matriculation number(s): ?, ? -->
    <!--- It took me 0,5 hours to solve the tasks in this file -->
    <!--- It took me 1 hours to set up the Vue application -->
    <div class="container">
      <h2>API "Content" - Page {{ currentPage }}</h2>

      <!-- TODO second pagination like pagination below table here (1 Point) -->
      <b-pagination
        align="center"
        size="md"
        :total-rows="totalCount"
        v-model="currentPage"
        :per-page="itemsPerPage"
      ></b-pagination>

      <!-- Bonus points for a loading screen appearing when loading new entries -->
      <b-card-group columns class="mb-4" v-if="!loading">
        <b-card
          :key="entry['id']"
          v-for="entry in pageEntries"
          :header="entry['category']"
          :img-src="getImageSrc(entry)"
          img-fluid
          img-alt="Image described by captions"
          img-top
        >
          <ul>
            <li v-for="caption in entry.captions" :key="caption.text">{{caption.text}}</li>
            <!-- TODO insert list of captions here, consider caption['text'] as a unique value, use v-for to accomplish this (3 Points) -->
          </ul>
        </b-card>
      </b-card-group>
      <b-spinner v-else></b-spinner>
      <b-pagination
        align="center"
        size="md"
        :total-rows="totalCount"
        v-model="currentPage"
        :per-page="itemsPerPage"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import { ITEMS_PER_PAGE } from "../constants";
export default {
  name: "API",
  data() {
    return {
      currentPage: 1,
      API_URL: "https://flask-training-api.www-technologien.marschke.me/v1",
      itemsPerPage: ITEMS_PER_PAGE,
      pageEntries: [],
      loading: false,
      totalCount: 1
    };
  },
  watch: {
    currentPage: function() {
      // trigger loading new items here (we do not care about race conditions here, but if you want to prevent them, you probably get some bonus points ;) )
      this.loadActualPageEntries();
    }
  },
  methods: {
    loadActualPageEntries: function() {
      if (this.loading) return;
      let url =
        this.API_URL +
        "/images?offset=" +
        (this.currentPage - 1) * this.itemsPerPage +
        "&limit=" +
        this.itemsPerPage;
      this.loading = true;
      fetch(url).then(result => {
        result = result.json().then(result => {
          this.pageEntries = [];
          this.totalCount = result.count;
          for (let image of result.images) {
            image.title = "Image " + image.id;
            this.pageEntries.push(image);
          }
          this.loading = false;
        });
      });

      // TODO load up to date page entries and store them in pageEntries (this.pageEntries) (3 Points)
      // TODO Don't forget to update totalCount by request information! (1 Point)
    },
    getImageSrc: function(entry) {
      // TODO get real address (1 Point)
      return this.API_URL + "/images/" + entry.id + "/bitmap";
    }
  },
  mounted() {
    this.loadActualPageEntries();
  }
  // TODO ensure loadActualPageEntries() gets called when the component gets displayed. Take a look at https://vuejs.org/v2/guide/instance.html#Lifecycle-Diagram (2 Points)
};
</script>

<style lang="scss" scoped>
@import "../style/bootstrap-component-include";
.question {
  color: $gray-700;
}

// TODO What does it do? Explain especially the @include command (1 Point class explanation, 2 Points include explanation)
.card-columns {
  @include media-breakpoint-only(md) {
    column-count: 2;
  }
  @include media-breakpoint-only(lg) {
    column-count: 3;
  }
  @include media-breakpoint-only(xl) {
    column-count: 4;
  }
}
</style>

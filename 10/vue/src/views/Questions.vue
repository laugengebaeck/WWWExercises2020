<template>
  <div>
    <!--- Matriculation number(s): ?, ? -->
    <!--- It took me 0,5 hours to solve the tasks in this file -->
    <div class="container">
      <h2>Questions & Answers</h2>
      <p>
        Please answer questions directly in source code at
        <code>src/components/Questions.vue</code>
        and then remove this comment!
      </p>

      <b-card-group columns>
        <b-card v-bind:key="question.title" v-for="question in questions" :title="question.title">
          <div slot="header">
            <span v-if="question.points === 1">{{ question.points}} Point</span>
            <span v-else>{{ question.points }} Points</span>
          </div>

          <p class="question card-text">{{ question.question }}</p>

          <p class="answer card-text">{{ question.answer }}</p>
        </b-card>
      </b-card-group>
    </div>
  </div>
</template>

<script>
export default {
  name: "Questions",
  data() {
    return {
      questions: [
        {
          title: "SCSS",
          question:
            "Why is it preferable to use SCSS for large projects? What are the downsides of using it?",
          points: 2,
          answer:
            "It is preferrable because it allows devs to use the DRY princpile when designing styles through SCSS variables, with the known DRY advantages. A disadvantage is that it is compiled into css which is opaque to the dev, so they have less control over the results and errors may occur in the process."
        },
        {
          title: "Vue Component",
          question: "What is a Vue Component?",
          points: 1,
          answer: "A reusable Vue object with its own HTML, scripts and styles"
        },
        {
          title: "Vue Router",
          question:
            "What is the responsibility of the Vue Router? (file src/router/index.js)",
          points: 1,
          answer: "Hmmm, I did not come up with a solution yet."
        },
        {
          title: "Vue Watcher",
          question:
            'When is a watcher like "currentPage" in src/components/API.vue called?',
          points: 1,
          answer: "Hmmm, I did not come up with a solution yet."
        }
      ]
    };
  }
};
</script>

<style lang="scss" scoped>
@import "../style/bootstrap-component-include";

.question {
  color: $gray-700;
}

.card-columns {
  @include media-breakpoint-only(sm) {
    column-count: 2;
  }
  @include media-breakpoint-only(md) {
    column-count: 3;
  }
  @include media-breakpoint-only(lg) {
    column-count: 4;
  }
}
</style>

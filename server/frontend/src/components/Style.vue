<template>
<div></div>
</template>
<script>
export default {
  name: 'Style',
};
</script>
<style>
body {
  background-color: rgba(7, 13, 23, 0.9);
  color: #eee;
  display: flex;
  flex-direction: column;
}

html,
body {
  height: 100%;
}

.p2 {
  padding: 0.5rem 1rem;
}

.content {
  flex: 1 0 auto;
}

.left-menu,
.maincontent {
  min-height: 100%;
}

footer {
  flex-shrink: 0;
}

.row {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
}

.column {
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
  flex: 1;
}

.card {
  margin-bottom: 1rem;
  border-color: #555;

  background: linear-gradient(0deg, rgba(100, 100, 100, .2)100%, rgba(100, 100, 100, 1) 100%);
}

.card-header {
  background-color: rgba(30, 30, 30, .1);
  border-bottom: 1px solid rgba(90, 90, 90, 0.6);
}

.card-body {
  -webkit-box-flex: 1;
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
  padding: 1.25rem;
}

.flot-base {
  background-color: rgba(5, 5, 5, .5);
}

.flot-y-axis,
.flot-x-axis {
  fill: #4f923b;
  font-size: 15px;
  font-family: "Courier New", Courier, monospace;
}

.items {
  display: flex;
  flex-wrap: wrap;
  margin-left: -10px;
  margin-top: -10px;
}

.items .item {
  flex: 1 0 400px;
  box-sizing: border-box;
  padding: 10px;
  margin-left: 10px;
  margin-top: 10px;
}

@media (min-width: 410px) {
  .items .item {
    max-width: calc(100s% - 10px);
  }
}

@media (min-width: 620px) {
  .items .item {
    max-width: calc(50% - 10px);
  }
}

@media (min-width: 830px) {
  .items .item {
    max-width: calc(50% - 10px);
  }
}

@media (min-width: 1040px) {
  .items .item {
    max-width: calc(33.33% - 10px);
  }
}

@media (min-width: 1460px) {
  .items .item {
    max-width: calc(33.33% - 10px);
  }
}

@media (min-width: 1920px) {
  .items .item {
    min-width: calc(25% - 10px);
  }
}
</style>

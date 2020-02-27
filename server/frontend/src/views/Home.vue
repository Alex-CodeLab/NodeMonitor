<template>
<div class="home">
  <apexcharts width="500" type="line" :options="chartOptions" :series="series.load"></apexcharts>
  <apexcharts width="500" type="line" :options="chartOptions" :series="series.memory"></apexcharts>
  <Style></Style>
</div>
</template>

<script>
// @ is an alias to /src
import Style from '@/components/Style.vue';
import VueApexCharts from 'vue-apexcharts';

const chartOptions = {
  chartOptions: {
    chart: {
      id: 'vuechart',
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: false,
      },
      animations: {
        enabled: false,
        easing: 'linear',
        dynamicAnimation: {
          speed: 100,
        },
      },
    },
    xaxis: {
      labels: {
        show: false,
      },
    },
    stroke: {
      curve: 'straight',
      width: 1,
    },
    title: {
      text: 'Load',
      align: 'left',
    },
    colors: ['#00BAEC'],
    grid: {
      yaxis: {
        lines: {
          show: false,
        },
      },
    },
  },
  series: {
    load: [{
      name: 'load',
      data: [],
    }],
    memory: [{
      name: 'memory',
      data: [],
    }],
    btcticker: [{
      name: 'btcticker',
      data: [],
    }],
  },
};


export default {
  name: 'Home',
  data: () => (chartOptions),
  components: {
    apexcharts: VueApexCharts,
    Style,
  },
  mounted() {
    // TODO: load from config
    const modules = ['load', 'memory'];
    modules.forEach((element) => this.callApi(element));
    this.startWebsocket();
  },
  methods: {
    updateChart(data) {
      // TODO: remove this
      const msg = JSON.parse(data);
      const newData = this.series[msg.module][0].data;
      newData.shift();
      newData.push(msg.data.value);
      // const newData = this.series[msg.module][0].data.push(1);
      // console.log(msg.module, newData);
      // //   const newData = this.series[msg.module][0].data.push(1);
      this.series.load = [{
        data: newData,
      }];
      // }
    },
    initChartData(module, data) {
      const values = [];
      for (let i = 0; i < data.msg.length; i += 1) {
        values.push(parseFloat(data.msg[i].data.value));
      }
      // console.log(values);
      this.series[module] = [{
        data: values,
      }];
    },
    startWebsocket() {
      const ws = new WebSocket('ws://127.0.0.1:5555', ['pub.sp.nanomsg.org']);
      ws.addEventListener('message', (e) => {
        const reader = new FileReader(); // handle binary messages
        reader.addEventListener('loadend', () => {
          const { result } = reader;
          this.updateChart(result);
        });
        reader.readAsText(e.data);
      });
    },
    callApi(module) {
      // eslint-disable-next-line
      // console.log(module);
      const url = `http://127.0.0.1:5000/data/${module}`;
      fetch(url)
        .then((response) => response.json())
        .then((myJson) => {
          this.messages = myJson;
          this.initChartData(module, myJson);
        });
    },
  },
};
</script>

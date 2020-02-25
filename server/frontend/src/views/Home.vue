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
      animations: {
        enabled: false,
        easing: 'linear',
        dynamicAnimation: {
          speed: 1000,
        },
      },
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: false,
      },
    },
    colors: ['#00BAEC'],
    stroke: {
      width: 1,
    },
    grid: {
      yaxis: {
        lines: {
          show: false,
        },
      },
      xAxis: {
        labels: {
          show: true,
          hideOerlappingLabels: true,
          showDuplcates: false,
          trim: true,
          style: {
            colors: ['#AAAAAA'],
          },
        },
      },
    },
  },
  series: {
    load: [{
      name: 'series-1',
      data: [1, 2, 3, 4],
    }],
    memory: [{
      name: 'series-1',
      data: [5, 6, 7, 8],
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
    updateChart() {
      // TODO: remove this
      const newData = this.series[0].data.map(() => Math.floor(Math.random() * 10) / 10);
      console.log(newData);
      this.series = [{
        data: newData,
      }];
    },
    initChartData(module, data) {
      const values = [];
      for (let i = 0; i < data.msg.length; i += 1) {
        values.push(parseFloat(data.msg[i].data.value));
      }
      console.log(values);

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
          // eslint-disable-next-line
          console.log(2, result);
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

<template>
<div class="home">
  <Style></Style>
  <div v-for="(item, index) in series" :key="item.name" >
    <apexcharts width="500" :options="getChartOptions(index)" :series="getData(index)" >
    </apexcharts>
  </div>
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
      type: 'line',
      stacked: false,
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
    markers: {
      size: 0,
    },
    stroke: {
      curve: 'straight',
      width: 1,
    },
    title: {
      text: '',
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
      type: 'line',
    }],
    memory: [{
      data: [],
      name: 'memory',
      type: 'line',
    }],
    btcticker: [{
      data: [],
      name: 'btcticker',
      type: 'line',
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
    const url = 'http://127.0.0.1:5000/modules';
    fetch(url)
      .then((response) => response.json())
      .then((modulesJson) => {
        // console.log(modulesJson);
        this.config = modulesJson;
        const modules = Object.keys(modulesJson);
        this.modules = modules;
        modules.forEach((element) => this.initChartData(element));
      });
    this.startWebsocket();
  },
  methods: {
    getData(index) {
      return this.series[index];
    },
    getChartOptions(index) {
      console.log(this.config[index]);
      if (this.config[index].type === 'stacked') {
        this.chartOptions.stacked = true;
      } else {
        this.config[index].type = 
      }
      return this.chartOptions;
    },
    updateChart(data) {
      const msg = JSON.parse(data);
      // console.log(msg);
      const newData = this.series[msg.module][0].data;
      if (newData.length > 1000) {
        newData.shift();
      }
      newData.push(msg.data.value);
      this.series[msg.module] = [{
        data: newData,
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
    initChartData(module) {
      // eslint-disable-next-line
      // console.log(module);
      const url = `http://127.0.0.1:5000/data/${module}`;
      fetch(url)
        .then((response) => response.json())
        .then((myJson) => {
          this.messages = myJson;
          // this.initChartData(module, myJson);
          const values = [];
          for (let i = 0; i < myJson.msg.length; i += 1) {
            values.push(parseFloat(myJson.msg[i].data.value));
          }
          // console.log(values);
          this.series[module] = [{
            data: values,
          }];
        });
    },
  },
};
</script>

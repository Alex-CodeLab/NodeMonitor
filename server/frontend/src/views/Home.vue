<template>
<div class="home">
  <Style></Style>
  <div class="clearfix border">
    <div v-for="(item, index) in series" :key="item.name" >
      <div class="md-col md-col-4 border">
        <apexcharts width="500" :options="getChartOptions(index)" :series="getData(index)" >
        </apexcharts>
      </div>
    </div>
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
    plotOptions: {
      bar: {
        horizontal: true,
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
    colors: ['#00BAEC', '#BA00EC', '#ECBA00'],
    grid: {
      yaxis: {
        lines: {
          show: false,
        },
      },
    },
  },
  series: {},
};

const series = {
  load: [{
    data: [],
  }],
  memory: [{
    data: [],
  }],
  btcticker: [{
    data: [],
  }],
};

chartOptions.series = series;

export default {
  name: 'Home',
  created() {
    const url = 'http://127.0.0.1:5000/modules';
    fetch(url)
      .then((response) => response.json())
      .then((modulesJson) => {
        // this.config = modulesJson;
        this.modules = Object.keys(modulesJson);
        this.modules.forEach((element) => {
          chartOptions.series[element] = [{ data: [] }];
          this.initChartData(element);
        });
      });
  },
  data: () => (chartOptions),
  components: {
    apexcharts: VueApexCharts,
    Style,
  },
  mounted() {
    this.startWebsocket();
  },
  beforeCreate() {
    const url = 'http://127.0.0.1:5000/modules';
    fetch(url)
      .then((response) => response.json())
      .then((modulesJson) => {
        this.config = modulesJson;
      });
  },
  methods: {
    getData(index) {
      return this.series[index];
    },
    getChartOptions(index) {
      if (typeof this.config !== 'undefined') {
        if (this.config[index].type === 'stacked') {
          this.chartOptions.stacked = true;
        } else {
          this.chartOptions.type = this.config[index].type;
        }
      }
      return this.chartOptions;
    },
    updateChart(data) {
      const msg = JSON.parse(data);
      let newData = this.series[msg.module][0].data;
      if (newData.length >= 1000) {
        newData.shift();
      }
      if ('value' in msg) {
        newData.push(msg.value);
        this.series[msg.module] = [{
          data: newData,
        }];
      } else {
        const subdata = [];
        Object.keys(msg.data).forEach((key) => {
          for (let i = 0; i < Object.keys(msg.data).length; i += 1) {
            if (typeof this.series[msg.module][i] !== 'undefined') {
              if (this.series[msg.module][i].name === key) {
                newData = this.series[msg.module][i].data;
                if (newData.length >= 1000) {
                  newData.shift();
                }
                newData.push(msg.data[key]);
                subdata.push({ data: newData, name: key });
              }
            }
          }
        });
        this.series[msg.module] = subdata;
      }
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
          const values = [];
          const subdata = [];
          subdata.total = [];
          subdata.used = [];
          subdata.value = [];
          for (let i = 0; i < myJson.msg.length; i += 1) {
            if ('value' in myJson.msg[i]) {
              values.push(parseFloat(myJson.msg[i].value));
            }
            if ('data' in myJson.msg[i]) {
              Object.keys(myJson.msg[i].data).forEach((key) => {
                subdata[key].push(myJson.msg[i].data[key]);
              });
            }
          }
          // console.log(myJson.msg[0], typeof myJson.msg[0], Object.keys(myJson.msg[0]).length);
          if (Object.keys(myJson.msg[0]).length > 0) {
            if ('value' in myJson.msg[0]) {
              this.series[module] = [{
                data: values,
              }];
            } else if ('data' in myJson.msg[0]) {
              Object.keys(subdata).forEach((key) => {
                values.push({ data: subdata[key], name: key });
              });
              this.series[module] = values;
            }
          }
        });
    },
  },
};
</script>

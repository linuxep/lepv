/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuGauguChart = function(divName, socket, server) {

    LepvChart.call(this, divName, socket, server);

    this.socket_message_key = 'cpu.stat';

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};

    // this.updateChartHeader();
    this.initializeChart();

    this.setupSocketIO();
};

CpuGauguChart.prototype = Object.create(LepvChart.prototype);
CpuGauguChart.prototype.constructor = CpuGauguChart;

CpuGauguChart.prototype.initializeChart = function() {
    
    this.chart = new LepvGaugeChart(this.chartDivName);
};

CpuGauguChart.prototype.updateChartData = function(response) {

    var data = response['data']['cpu_stat'];

    var cpuOccupationRatio = 100 - parseFloat(data['all']['idle']);
    this.chart.updateChartData({'ratio': cpuOccupationRatio.toFixed(2)});
    this.requestData();
};

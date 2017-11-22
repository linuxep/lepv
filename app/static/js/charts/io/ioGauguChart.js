/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var IOGauguChart = function(divName, socket, server) {

    LepvChart.call(this, divName, socket, server);

    this.socket_message_key = 'io.status';
    this.isLeadingChart = false;

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};

    // this.updateChartHeader();
    this.initializeChart();

    this.setupSocketIO();
};

IOGauguChart.prototype = Object.create(LepvChart.prototype);
IOGauguChart.prototype.constructor = IOGauguChart;

IOGauguChart.prototype.initializeChart = function() {
    
    this.chart = new LepvGaugeChart(this.chartDivName);
};

IOGauguChart.prototype.updateChartData = function(response) {

    var data = response['data'];
    // update gauge
    this.chart.updateChartData(data);
    this.requestData();
};

/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var MemoryGauguChart = function(divName, socket, server) {

    LepvChart.call(this, divName, socket, server);

    this.socket_message_key = 'memory.status';
    this.isLeadingChart = false;

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};

    // this.updateChartHeader();
    this.initializeChart();

    this.setupSocketIO();
};

MemoryGauguChart.prototype = Object.create(LepvChart.prototype);
MemoryGauguChart.prototype.constructor = MemoryGauguChart;

MemoryGauguChart.prototype.initializeChart = function() {
    
    this.chart = new LepvGaugeChart(this.chartDivName);
};

MemoryGauguChart.prototype.updateChartData = function(response) {
    var data = response['data'];
    if (!data && typeof(data)!='undefined' && data!=0) {
        return
    }
    if (typeof(data) == "undefined"){
        return
    }
    console.log(data)

    // update gauge
    this.chart.updateChartData(data);
    this.requestData();
};

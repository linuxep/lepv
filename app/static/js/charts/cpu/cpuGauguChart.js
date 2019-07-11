/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuGauguChart = function(divName, socket, server) {

    LepvChart.call(this, divName, socket, server);

    this.socket_message_key = 'cpu.status';
    // this.isLeadingChart = false;

    this.socket_response = null;
    this.chart = null;
    this.refreshInterval = 3;
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
    var data = response['data'];
    if (!data && typeof(data)!='undefined' && data!=0) {
        return
    }
    if (typeof(data) == "undefined"){
        return
    }
//    console.log(data)

    
    var cpuOccupationRatio = parseFloat(data['idle']);
    this.chart.updateChartData({'ratio': cpuOccupationRatio.toFixed(2)});
    // this.requestData();
};

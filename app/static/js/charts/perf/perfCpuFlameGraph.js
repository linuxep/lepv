/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2017, LEP>.
 */

var PerfCpuFlameGraph = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.isLeadingChart = false;

    this.chartWidth = $(".col-md-12").width() * 0.96;

    this.locateUIElements();

    this.socket_message_key = 'perf.cpuclock.flame';

    this.initializeChart();
    this.setupSocketIO();
};

PerfCpuFlameGraph.prototype = Object.create(LepvChart.prototype);
PerfCpuFlameGraph.prototype.constructor = PerfCpuFlameGraph;

PerfCpuFlameGraph.prototype.initializeChart = function() {
    this.chart = d4.flameGraph().width(this.chartWidth);

    var thisChart = this;
    d4.json('/static/test.json', function(error, data) {
        if (error) return console.warn(error);

        d4.select('#' + thisChart.mainDivName).datum(data).call(thisChart.chart);
    });
};

PerfCpuFlameGraph.prototype.updateChartData = function(response) {

    var thisChart = this;


};

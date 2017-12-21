/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2017, LEP>.
 */

var PerfFlameGraph = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.chartWidth = $(".col-md-12").width() * 0.96;

    this.locateUIElements();
    this.refreshInterval = 8;

    this.socket_message_key = 'perf.flame';

    this.initializeChart();
    this.setupSocketIO();
};

PerfFlameGraph.prototype = Object.create(LepvChart.prototype);
PerfFlameGraph.prototype.constructor = PerfFlameGraph;

PerfFlameGraph.prototype.initializeChart = function() {
    this.chart = d4.flameGraph().width(this.chartWidth);
};

PerfFlameGraph.prototype.updateChartData = function(response) {

    var thisChart = this;
    if (response['flame'] != null) {
        d4.select('#' + thisChart.mainDivName).datum(response['flame']).call(thisChart.chart);
    }
    // this.requestData();
};

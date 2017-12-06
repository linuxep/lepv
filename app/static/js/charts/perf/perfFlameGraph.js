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

    this.socket_message_key = 'perf.flame';

    this.initializeChart();
    this.setupSocketIO();
};

PerfFlameGraph.prototype = Object.create(LepvChart.prototype);
PerfFlameGraph.prototype.constructor = PerfFlameGraph;

PerfFlameGraph.prototype.initializeChart = function() {
    this.chart = d4.flameGraph().width(this.chartWidth);

//    var thisChart = this;
//    d4.json('/static/test.json', function(error, data) {
//        if (error) return console.warn(error);
//
//        d4.select('#' + thisChart.mainDivName).datum(data).call(thisChart.chart);
//    });
};

PerfFlameGraph.prototype.updateChartData = function(response) {

    var thisChart = this;

    d4.select('#' + thisChart.mainDivName).datum(response).call(thisChart.chart);

};

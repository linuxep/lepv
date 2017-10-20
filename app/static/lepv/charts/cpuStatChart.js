/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChart = function(rootDivName, socket) {

  this.rootDiv = $("#" + rootDivName);

  this.socketIO = socket;

  this.initializeChart();
  this.setupSocketIO();

};

LepvChart.prototype.setupSocketIO = function() {

    var thisChart = this;

    this.socketIO.on('cpu.stat.res', function(response) {

        console.log("cpu.stat.res received: " + response);

        thisChart.updateChartData(response['data']['all']);

    });



};


LepvChart.prototype.requestData = function() {
    this.socketIO.emit("cpu.stat.req", {'server': "www.rmlink.cn"})
};

LepvChart.prototype.initializeChart = function() {
  $('#' + this.chartDivName).empty();

    this.chart = c3.generate({
        bindto: '#div-cpu-stat-panel',
        data: {
            columns: [
                ['user', 0],
                ['nice', 0],
                ['system', 0],
                ['idle', 0],
                ['iowait', 0],
                ['irq', 0],
                ['softirq', 0],
                ['steal', 0],
                ['guest', 0],
                ['guestnice', 0]
            ],
            type : 'donut',
            colors: {
                idle: "green",
                user: 'blue',
                system: 'red',
                nice: "orange"
            }
        },
        donut: {
            title: "CPU STAT"
        },
        legend: {
            show: true,
            position: 'right'
        }
    });
};


LepvChart.prototype.updateChartData = function(overallData) {
    this.chart.load({
        columns: [
            ['user', overallData.user],
            ['nice', overallData.nice],
            ['system', overallData.system],
            ['idle', overallData.idle],
            ['iowait', overallData.iowait],
            ['irq', overallData.irq],
            ['softirq', overallData.soft],
            ['steal', overallData.steal],
            ['guest', overallData.guest],
            ['guestnice', overallData.gnice]
        ],
        keys: {
            value: ['']
        }
    });

    this.requestData();

};



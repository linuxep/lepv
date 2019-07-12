/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuStatDonutChart = function (rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.socket_message_key = 'cpu.stat';
    this.refreshInterval = 3;

    this.socket_response = null;
    this.chart = null;
    this.chartData = null;

    this.initializeChart();
    this.setupSocketIO();

};

CpuStatDonutChart.prototype = Object.create(LepvChart.prototype);
CpuStatDonutChart.prototype.constructor = CpuStatDonutChart;


CpuStatDonutChart.prototype.initializeChart = function () {

    this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
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
            type: 'donut',
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


CpuStatDonutChart.prototype.updateChartData = function (response) {
    var data = response['data'];
    if (!data && typeof (data) != 'undefined' && data != 0) {
        return
    }
    if (typeof (data) == "undefined") {
        return
    }
    console.log(data)
    console.log('------------')

    var overallData = data['all'];
    if (!overallData && typeof (overallData) != 'undefined' && overallData != 0) {
        return
    }
    if (typeof (overallData) == "undefined") {
        return
    }

    console.log(overallData)

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

    // this.requestData();

};



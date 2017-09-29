/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvCpuDonutChart = function(chartDivName) {
    
    LepvChart.call(this, chartDivName);
    
    this.chartTitle = "CPU Chart";
    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;

    this.proactive = false;

    this.updateChartHeader();
    this.initialize();
};

LepvCpuDonutChart.prototype = Object.create(LepvChart.prototype);
LepvCpuDonutChart.prototype.constructor = LepvCpuDonutChart;

LepvCpuDonutChart.prototype.initialize = function() {

    $('#' + this.chartDivName).empty();
    
    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
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

LepvCpuDonutChart.prototype.updateChartData = function(overallData) {
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

};

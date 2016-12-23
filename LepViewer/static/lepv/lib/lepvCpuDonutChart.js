/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvCpuDonutChart = function(chartDivNames) {
    
    LepvChart.call(this, chartDivNames.donutChartDivName);
    
    this.chartTitle = "CPU Chart";
    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;

    //this.dataUrlPrefix = "/cpustat/";

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

LepvCpuDonutChart.prototype.updateChartData = function(data) {
    this.chart.load({
        columns: [
            ['user', data.all.user],
            ['nice', data.all.nice],
            ['system', data.all.system],
            ['idle', data.all.idle],
            ['iowait', data.all.iowait],
            ['irq', data.all.irq],
            ['softirq', data.all.soft],
            ['steal', data.all.steal],
            ['guest', data.all.guest],
            ['guestnice', data.all.gnice]
        ],
        keys: {
            value: ['']
        }
    });

};

/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuAvgLoadChart = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.socket_message_key = 'cpu.avgload';
    this.chart = null;
    
    this.chartTitle = "Average Load Chart";
    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;

    this.chartData['last1'] = ['Last minute'];
    this.chartData['last5'] = ['Last 5 minutes'];
    this.chartData['last15'] = ['Last 15 minutes'];

    this.cpuCoreCount = 1;
    this.yellowAlertValue = 0.7;
    this.redAlertValue = 0.9;
    
    this.initializeChart();
    this.setupSocketIO();
};

CpuAvgLoadChart.prototype = Object.create(LepvChart.prototype);
CpuAvgLoadChart.prototype.constructor = CpuAvgLoadChart;

CpuAvgLoadChart.prototype.initializeChart = function() {

    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            x: 'x',
            columns: [this.timeData,
                ['Last minute'],
                ['Last 5 minute'],
                ['Last 15 minute']]

        },
        legend: {
            show: true,
            position: 'bottom',
            inset: {
                anchor: 'top-right',
                x: 20,
                y: 10,
                step: 2
            }
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%H:%M:%S'
                }
            },
            y: {
                label: {
                    position: "inner-middle"
                },
                min: 0,
                max: undefined,
                padding: {
                    top:10,
                    bottom:10
                }
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value;
                }
            }
        }
    });

};

CpuAvgLoadChart.prototype.updateChartData = function(data) {

    if (this.chart == null) {
        return;
    }

    if (this.chartData['last1'].length > this.maxDataCount) {
        this.timeData.splice(1, 1);
        this.chartData['last1'].splice(1, 1);
        this.chartData['last1'].splice(1, 1);
        this.chartData['last1'].splice(1, 1);
    }

    this.timeData.push(new Date());
    this.chartData['last1'].push(data['last1']);
    this.chartData['last5'].push(data['last5']);
    this.chartData['last15'].push(data['last15']);

//    this.chart.load({
//        columns: [this.timeData,
//            this.chartData['last1'],
//            this.chartData['last5'],
//            this.chartData['last15']],
//        keys: {
//            value: ['']
//        }
//    });
};

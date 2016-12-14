/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvMemoryChart = function(divName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);

    this.chartTitle = "RAM Chart";
    this.chartHeaderColor = 'green';

    this.maxDataCount = 150;
    this.refreshInterval = 2;

    this.dataUrlPrefix = "/status/memory/";

    this.updateChartHeader();
    this.initialize();
};

LepvMemoryChart.prototype = Object.create(LepvChart.prototype);
LepvMemoryChart.prototype.constructor = LepvMemoryChart;

LepvMemoryChart.prototype.initialize = function() {
    
    this.chartData['Free'] = ['Free'];
    this.chartData['Cached'] = ['Cached'];
    this.chartData['Buffers'] = ['Buffers'];
    this.chartData['Used'] = ['Used'];

    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            x: 'x',
            // the order matters: free -> cached -> buffers -> used
            columns: [this.timeData, 
                this.chartData['Used'],
                this.chartData['Buffers'],
                this.chartData['Cached'],
                this.chartData['Free']],

            types: {
                Used: 'area',
                Buffers: "area",
                Cached: "area",
                Free: "area"
            },

            groups: [['Free', 'Cached', 'Buffers', 'Used']],
            order: null,

            colors: {
                Free: '#2d862d',
                Cached: "#ffb84d",
                Buffers: "#4d94ff",
                Used: "#ff6666"
            }
        },
        point: {
            show: false
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
                padding: {top:0, bottom:0}
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value + " MB";
                }
            }
        }
    });
};

LepvMemoryChart.prototype.updateChartData = function(data) {
    if (this.timeData.length > this.maxDataCount) {
        this.timeData.splice(1, 1);
        this.chartData['Free'].splice(1, 1);
        this.chartData['Used'].splice(1, 1);
        this.chartData['Buffers'].splice(1, 1);
        this.chartData['Cached'].splice(1, 1);
    }

    this.timeData.push(new Date());
    this.chartData['Used'].push(data['used']);
    this.chartData['Buffers'].push(data['buffers']);
    this.chartData['Free'].push(data['free']);
    this.chartData['Cached'].push(data['cached']);

    this.chart.load({
        //// the order matters: free -> cached -> buffers -> used
        columns: [this.timeData,
            this.chartData['Used'],
            this.chartData['Buffers'],
            this.chartData['Cached'],
            this.chartData['Free']]
    });
};

/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var MemoryChart = function(divName, socket, server) {

    LepvChart.call(this, divName, socket, server);
    this.chartTitle = "RAM Chart";
    this.chartHeaderColor = 'green';

    this.socket_message_key = 'memory.status';
    this.isLeadingChart = false;

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};
    this.timeData = ['x'];

    this.maxDataCount = 150;
    this.refreshInterval = 2;


    // this.updateChartHeader();
    this.initializeChart();

    this.setupSocketIO();
};

MemoryChart.prototype = Object.create(LepvChart.prototype);
MemoryChart.prototype.constructor = MemoryChart;

MemoryChart.prototype.initializeChart = function() {
    
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

MemoryChart.prototype.updateChartData = function(response) {
    // console.log(response)
    data = response['data']
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

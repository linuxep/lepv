/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuStatIdleChart = function(rootDivName, socket, server) {

  LepvChart.call(this, rootDivName, socket, server);

  this.socket_message_key = 'cpu.stat';
  this.chart = null;

  this.isLeadingChart = false;

  this.maxDataCount = 150;
  this.refreshInterval = 2;
  this.timeData = ['x'];

  this.initializeChart();
  this.setupSocketIO();

};

CpuStatIdleChart.prototype = Object.create(LepvChart.prototype);
CpuStatIdleChart.prototype.constructor = CpuStatIdleChart;


CpuStatIdleChart.prototype.initializeChart = function() {

    var thisChart = this;

    this.chart = c3.generate({
        bindto: '#div-cpu-stat-idle-panel',
        data: {
            x: 'x',
            columns: [thisChart.timeData]
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
                max: 100,
                padding: {top:0, bottom:0}
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value + " %";
                }
            }
        }
    });
};


CpuStatIdleChart.prototype.updateChartData = function(response) {

    var thisChart = this;

    var data = response['data'];
    delete data['all'];

    if ( !( 'CPU-0' in this.chartData) ) {
        this.chartData = {};
        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName] = ['CPU-' + coreName];
        });

    }
    if (this.timeData.length > this.maxDataCount) {
        this.timeData.splice(1, 1);

        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName].splice(1, 1);
        });
    }

    this.timeData.push(new Date());
    $.each( data, function( coreName, statValue ) {
        thisChart.chartData['CPU-' + coreName].push(statValue);
    });

    var columnDatas = [];
    columnDatas.push(this.timeData);
    $.each( data, function( coreName, statValue ) {
        columnDatas.push(thisChart.chartData['CPU-' + coreName]);
    });

    this.chart.load({
        columns: columnDatas
    });

};



/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuIrqChart = function(rootDivName, socket, server, typ) {

  LepvChart.call(this, rootDivName, socket, server);

  this.socket_message_key = 'cpu.stat';
  this.chart = null;
  this.dataType = typ;

  this.isLeadingChart = false;

  this.maxDataCount = 150;
  this.refreshInterval = 2;
  this.timeData = ['x'];

  this.initializeChart();
  this.setupSocketIO();

};

CpuIrqChart.prototype = Object.create(LepvChart.prototype);
CpuIrqChart.prototype.constructor = CpuIrqChart;


CpuIrqChart.prototype.initializeChart = function() {

    var thisChart = this;

    this.chart = c3.generate({
        bindto: '#' + thisChart.chartDivName,
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
                    text: "Times/s",
                    position: "outter-middle"
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
                    return value + " times ";;
                }
            }
        }
    });
};


CpuIrqChart.prototype.updateChartData = function(response) {

    var thisChart = this;
    var data = {};
    if (thisChart.dataType == 'irq') {
        data = response['data']['irq'];
    }else{
        data = response['data']['softirq'];
    }
    // var data = response['data']['softirq'][thisChart.dataType];
    // delete data['all'];

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
        if (thisChart.dataType == 'irq') {
            thisChart.chartData['CPU-' + coreName].push(statValue);
        }else{
            thisChart.chartData['CPU-' + coreName].push(statValue[thisChart.dataType]);
        }
        
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



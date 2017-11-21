/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuStatUserGroupChart = function(rootDivName, socket, server) {

  LepvChart.call(this, rootDivName, socket, server);

  this.rootDivName = rootDivName;
  this.socket = socket;
  this.serverToWatch = server;

  this.socket_message_key = 'cpu.stat';
  this.chart = null;

  this.isLeadingChart = false;

  this.maxDataCount = 150;
  this.refreshInterval = 2;
  this.timeData = ['x'];

  this.initializeChart();
  this.setupSocketIO();

};

CpuStatUserGroupChart.prototype = Object.create(LepvChart.prototype);
CpuStatUserGroupChart.prototype.constructor = CpuStatUserGroupChart;


CpuStatUserGroupChart.prototype.initializeChart = function() {

    var thisChart = this;

    this.chart = c3.generate({
        bindto: '#' + thisChart.mainDivName,
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
                max: 105,
                padding: {
                        top:10,
                        bottom:10
                }
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


CpuStatUserGroupChart.prototype.updateChartData = function(response) {

    var thisChart = this;

    var data = response['data']['cpu_stat'];
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

//    userGroupStatData[coreName] = parseFloat(coreStatData.user) + parseFloat(coreStatData.system) + parseFloat(coreStatData.nice);
//    irqGroupStatData[coreName] = parseFloat(coreStatData.irq) + parseFloat(coreStatData.soft);
    this.timeData.push(new Date());
    $.each( data, function( coreName, statValue ) {
        thisChart.chartData['CPU-' + coreName].push(statValue['user'] + statValue['system'] + statValue['nice']);
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



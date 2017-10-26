/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvIrqLineChart = function(divName, chartTitle) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    
    this.chartTitle = chartTitle;
    this.chartHeaderColor = 'orange';
    
    this.proactive = false;
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;
    this.timeData = ['x'];
    
    this.updateChartHeader();
    this.initialize();
};

LepvIrqLineChart.prototype = Object.create(LepvChart.prototype);
LepvIrqLineChart.prototype.constructor = LepvIrqLineChart;

LepvIrqLineChart.prototype.initialize = function() {
    
    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            x: 'x',
            columns: [this.timeData]
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
                padding: {top:0, bottom:0}
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value + " ";
                }
            }
        }
    });
};

LepvIrqLineChart.prototype.updateChartData = function(data, messages) {

    var thisChart = this;
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

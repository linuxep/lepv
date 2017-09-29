/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvLineChart = function(divName, chartTitle, headerColor) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    
    this.chartTitle = "IO Stat Chart";
    this.chartHeaderColor = 'orange';
    
    this.proactive = false;
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;
    this.timeData = ['x'];

    this.updateChartHeader();
    this.initialize();
};

LepvLineChart.prototype = Object.create(LepvChart.prototype);
LepvLineChart.prototype.constructor = LepvLineChart;

LepvLineChart.prototype.initialize = function() {
    
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

LepvLineChart.prototype.updateChartData = function(data) {
    this.chart.load({
        columns: data,
        keys: {
            value: ['']
        }
    });
};

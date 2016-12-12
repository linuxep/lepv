/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvMemoryChart = function(divName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    
    this.maxDataCount = 200;
    this.refreshInterval = 2;
    this.chartHeaderColor = 'green';

    this.updateChartHeader();

    this.initializeChart();
};

LepvMemoryChart.prototype = Object.create(LepvChart.prototype);

LepvMemoryChart.prototype.constructor = LepvMemoryChart;

LepvMemoryChart.prototype.refreshChart = function() {
    if (this.isChartPaused) {
        return;
    }

    $.get(this.dataUrl, function(data, status){
        console.log("refreshed......");
        this.reloadChartData(data);
    });
};

LepvMemoryChart.prototype.reloadChartData = function(data) {
    
};

LepvMemoryChart.prototype.initializeChart = function() {
    
    console.log("chart initialized in lepvMemory");
    console.log(this.isChartPaused);
    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            x: 'x',
            columns: [['x'], ['readYYY'], ['writeYYY']],
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
                    text: "MMMB/S",
                    position: "inner-middle"
                }
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value + " MMMMb/s";
                }
            }
        }
    });
};

LepvMemoryChart.prototype.start = function() {
    this.initialize();
    this.refreshChart();

    var refreshFunction = this.refreshChart;
    this.intervalId = setInterval(function () {
        refreshFunction();
    }, this.refreshInterval * 1000);

};

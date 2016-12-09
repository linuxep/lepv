/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvIOChart = function(divName) {
    
    LepvChart.call(this, divName);
    console.log("I'm initialized in LepvIO");
    
    this.maxDataCount = 500;
    this.refreshInterval = 10;

    this.initializeChart();
    console.log(this.writeData);
};

LepvIOChart.prototype = Object.create(LepvChart.prototype);

LepvIOChart.prototype.constructor = LepvIOChart;

LepvIOChart.prototype.refreshChart = function() {
    if (this.isChartPaused) {
        return;
    }

    $.get(this.dataUrl, function(data, status){
        console.log("refreshed......");
        this.reloadChartData(data);
    });
};

LepvIOChart.prototype.reloadChartData = function(data) {
    
};

LepvIOChart.prototype.initializeChart = function() {
    
    console.log("chart initialized in lepvIO");
    console.log(this.isChartPaused);
    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            x: 'x',
            columns: [['x'], ['read'], ['write']],
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
                    text: "KB/S",
                    position: "inner-middle"
                }
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value + " kb/s";
                }
            }
        }
    });

    console.log("IO chart initialization done.");
};

LepvIOChart.prototype.start = function() {
    this.initialize();
    this.refreshChart();

    var refreshFunction = this.refreshChart;
    this.intervalId = setInterval(function () {
        refreshFunction();
    }, this.refreshInterval * 1000);

};


LepvIOChart.prototype.updateConfigs = function() {
    this.maxDataCount = newConfigs.maxDataCount;

    var updatedFlushInterval = newConfigs.flushInterval;

    if (updatedFlushInterval != this.refreshInterval) {
        this.refreshInterval = newConfigs.flushInterval;

        clearInterval(this.invervalId);

        this.intervalId = setInterval(function () {
            this.refreshChart();
        }, this.refreshInterval * 1000);
    }
};

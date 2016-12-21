/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvCpuGauge = function(divName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvGauge.call(this, divName);
    
    this.initialize();
};

LepvCpuGauge.prototype = Object.create(LepvGauge.prototype);
LepvCpuGauge.prototype.constructor = LepvCpuGauge;

LepvCpuGauge.prototype.initialize = function() {
    
    this.chart = c3.generate({
        bindto: this.chartDivName,
        data: {
            columns: [
                ['core-0', 30],
                ['core-1', 50],
                ['core-2', 45],
                ['core-3', 30],
                ['core-4', 10],
                ['core-5', 45],
                ['core-6', 30],
                ['core-7', 99]
            ],
            type: 'bar'
        },
        bar: {
            width: {
                ratio: 0.5 // this makes bar width 50% of length between ticks
            }
        },
        legend: {
            show: false
        },
        size: {
            height: 160
        },
        padding: {
            top: 0,
            right: 10,
            bottom: 0,
            left: 30
        },
        axis: {
            y: {
                max: 100,
                min: 0,
                // Range includes padding, set 0 if no padding needed
                 padding: {top:0, bottom:0}
            }
        }
    });
};

LepvCpuGauge.prototype.updateChartData = function(data) {

    this.chart.load({
        columns: [
            ['core-0', 30],
            ['core-1', 50],
            ['core-2', 45],
            ['core-3', 30],
            ['core-4', 50],
            ['core-5', 45],
            ['core-6', 30],
            ['core-7', 50]
        ],
        legend: {
            show: false
        }
    });
};

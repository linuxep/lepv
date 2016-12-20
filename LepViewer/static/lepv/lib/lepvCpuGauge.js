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
                ['core-2', 45]
            ],
            type: 'bar'
        },
        bar: {
            width: {
                ratio: 0.5 // this makes bar width 50% of length between ticks
            }
            // or
            //width: 100 // this makes bar width 100px
        }
    });
};

LepvCpuGauge.prototype.updateChartData = function(data) {

    this.chart.load({
        columns: [
            ['core-0', 60],
            ['core-1', 20],
            ['core-2', 55]
        ]
    });
};

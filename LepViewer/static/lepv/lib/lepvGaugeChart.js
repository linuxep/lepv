/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvGaugeChart = function(divName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    
    this.chartDivName = divName;
    this.proactive = false;

    this.initialize();
};

LepvGaugeChart.prototype = Object.create(LepvChart.prototype);
LepvGaugeChart.prototype.constructor = LepvGaugeChart;

LepvGaugeChart.prototype.initialize = function() {

    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            columns: [
            ],
            type: 'gauge'
        },
        gauge: {
            label: {
                format: function(value, ratio) {
                    return value + "%";
                },
                show: true // to turn off the min/max labels.
            },
            min: 0, // 0 is default, //can handle negative min e.g. vacuum / voltage / current flow / rate of change
            max: 100, // 100 is default
            width: 30 // for adjusting arc thickness
        },
        color: {
            pattern: ['#60B044', '#F6C600', '#F97600', '#FF0000'], // the three color levels for the percentage values.
            threshold: {
                values: [30, 60, 90, 100]
            }
        },
        size: {
            height: 100
        }
    });
};

LepvGaugeChart.prototype.updateChartData = function(data) {

    this.chart.load({
        json: [
            data
        ],
        keys: {
            value: ['ratio']
        }
    });
};

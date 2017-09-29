/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvProcrankPssPieChart = function(divName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);

    this.chartTitle = "RAM Chart";
    this.chartHeaderColor = 'green';
    this.proactive = false;

    this.maxDataCount = 25;
    
    this.chartData = [];

    this.updateChartHeader();
    this.initialize();
};

LepvProcrankPssPieChart.prototype = Object.create(LepvChart.prototype);
LepvProcrankPssPieChart.prototype.constructor = LepvProcrankPssPieChart;

LepvProcrankPssPieChart.prototype.initialize = function() {

    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            columns: this.chartData,
            type : 'donut'
        },
        donut: {
            title: "PSS"
        },
        legend: {
            show: true,
            position: 'right'
        }
    });
};

LepvProcrankPssPieChart.prototype.updateChartData = function(pssData) {

    this.chart.unload();
    this.chart.load({
        columns: pssData,
        keys: {
            value: ['']
        }
    });
};

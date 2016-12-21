/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvMemoryStatFreeVsPieChart = function(divName) {

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

LepvMemoryStatFreeVsPieChart.prototype = Object.create(LepvChart.prototype);
LepvMemoryStatFreeVsPieChart.prototype.constructor = LepvMemoryStatFreeVsPieChart;

LepvMemoryStatFreeVsPieChart.prototype.initialize = function() {

    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            columns: this.chartData,
            type : 'donut'
        },
        donut: {
            title: "PSS vs. Total"
        },
        legend: {
            show: true,
            position: 'bottom'
        }
    });
};

LepvMemoryStatFreeVsPieChart.prototype.updateChartData = function(sumData) {
    var dataColumn = [];

    // to show the correct % of pss against total in donut chart, we need to to set total as (total - pss)
    dataColumn.push(["Total Memory", sumData['total'] - sumData['pssTotal']]);
    dataColumn.push(["Total PSS", sumData['pssTotal']]);


    this.chart.load({
        columns: dataColumn,
        keys: {
            value: ['']
        }
    });
};

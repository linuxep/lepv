/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvCpuCharts = function(chartDivNames) {

    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;

    this.dataUrlPrefix = "/cpustat/";

    //this.donutChart = new LepvCpuDonutChart(chartDivNames.donutChartDivName);
    this.gaugeChart = new LepvGaugeChart(chartDivNames.gaugeDivName);
    this.idleChart = new LepvLineChart(chartDivNames.idleDivName, 'CPU Stat: Idle', this.chartHeaderColor);
    this.userGroupChart = new LepvLineChart(chartDivNames.userGroupDivName, 'CPU Stat: User+Sys+Nice', this.chartHeaderColor);
    this.irqGroupChart = new LepvLineChart(chartDivNames.irqGroupDivName, 'CPU Stat: IRQ + SoftIRQ', this.chartHeaderColor);
};

LepvCpuCharts.prototype = Object.create(LepvChart.prototype);
LepvCpuCharts.prototype.constructor = LepvCpuCharts;

LepvCpuCharts.prototype.initializeControlElements = function() {
    //this.donutChart.initializeControlElements();
    this.idleChart.initializeControlElements();
    this.userGroupChart.initializeControlElements();
    this.irqGroupChart.initializeControlElements();
};

LepvCpuCharts.prototype.initialize = function() {
    
    //this.donutChart.initialize();
    this.gaugeChart.initialize();
    this.idleChart.initialize();
    this.userGroupChart.initialize();
    this.irqGroupChart.initialize();
};

LepvCpuCharts.prototype.updateChartData = function(data) {
    //this.donutChart.updateChartData(data);
    this.gaugeChart.updateChartData(data.ratio);
    this.idleChart.updateChartData(data);
    this.userGroupChart.updateChartData(data);
    this.irqGroupChart.updateChartData(data);
};

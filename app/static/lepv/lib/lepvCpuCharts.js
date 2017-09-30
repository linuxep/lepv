/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvCpuCharts = function(chartDivNames) {

    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;

    this.proactive = true;
    this.maxRequestIdGap = 2;

    this.dataUrlPrefix = "/api/cpu/stat/";

    this.donutChart = new LepvCpuDonutChart(chartDivNames.donutChartDivName);
    
    this.idleChart = new LepvCpuLineChart(chartDivNames.idleDivName, 'CPU Stat; Idle');
    this.userGroupChart = new LepvCpuLineChart(chartDivNames.userGroupDivName, 'CPU Stat: User+Sys+Nice');
    this.irqGroupChart = new LepvCpuLineChart(chartDivNames.irqGroupDivName, 'CPU Stat: IRQ + SoftIRQ');
    
    this.gaugeChart = new LepvGaugeChart(chartDivNames.gaugeDivName);
};

LepvCpuCharts.prototype = Object.create(LepvChart.prototype);
LepvCpuCharts.prototype.constructor = LepvCpuCharts;

LepvCpuCharts.prototype.initializeControlElements = function() {
    this.donutChart.initializeControlElements();
    this.idleChart.initializeControlElements();
    this.userGroupChart.initializeControlElements();
    this.irqGroupChart.initializeControlElements();
};

LepvCpuCharts.prototype.initialize = function() {

    this.gaugeChart.initialize();
    
    this.donutChart.initialize();
    this.idleChart.initialize();
    this.userGroupChart.initialize();
    this.irqGroupChart.initialize();
};

LepvCpuCharts.prototype.updateChartData = function(data) {
    
    this.donutChart.updateChartData(data['all']);
    
    var cpuOccupationRatio = (100 - data['all']['idle']).toFixed(2);
    this.gaugeChart.updateChartData({'ratio': cpuOccupationRatio});
    
    delete data['all'];

    var idleStatData = {};
    var userGroupStatData = {};
    var irqGroupStatData = {};
    
    $.each( data, function( coreName, coreStatData ) {
        idleStatData[coreName] = coreStatData.idle;
        userGroupStatData[coreName] = coreStatData.user + coreStatData.system + coreStatData.nice;
        irqGroupStatData[coreName] = coreStatData.irq + coreStatData.soft;
    });
    
    this.idleChart.updateChartData(idleStatData);
    
    this.userGroupChart.updateChartData(userGroupStatData);
    this.irqGroupChart.updateChartData(irqGroupStatData);
};

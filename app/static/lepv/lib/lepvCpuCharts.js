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
    this.irqGroupChart = new LepvIrqLineChart(chartDivNames.irqGroupDivName, 'CPU Stat: IRQ');
    this.softIrqGroupChart = new LepvIrqLineChart(chartDivNames.softIrqGroupDivName, 'CPU Stat: SoftIRQ');
    
    this.gaugeChart = new LepvGaugeChart(chartDivNames.gaugeDivName);
};

LepvCpuCharts.prototype = Object.create(LepvChart.prototype);
LepvCpuCharts.prototype.constructor = LepvCpuCharts;

LepvCpuCharts.prototype.initializeControlElements = function() {
    this.donutChart.initializeControlElements();
    this.idleChart.initializeControlElements();
    this.userGroupChart.initializeControlElements();
    this.irqGroupChart.initializeControlElements();
    his.softIrqGroupChart.initializeControlElements();
};

LepvCpuCharts.prototype.initialize = function() {

    this.gaugeChart.initialize();
    
    this.donutChart.initialize();
    this.idleChart.initialize();
    this.userGroupChart.initialize();
    this.irqGroupChart.initialize();
    this.softIrqGroupChart.initialize();
};

LepvCpuCharts.prototype.updateChartData = function(data, messages={}) {
    // console.log(data)
    this.donutChart.updateChartData(data['cpu_stat']['all']);
    
    var cpuOccupationRatio = 100 - parseFloat(data['cpu_stat']['all']['idle']);
    this.gaugeChart.updateChartData({'ratio': cpuOccupationRatio.toFixed(2)});
    
    delete data['cpu_stat']['all'];

    var idleStatData = {};
    var idleStatMessages = {};

    var userGroupStatData = {};
    var userGroupStatMessages = {};

    var irqGroupStatData = {};
    var irqGroupStatMessages = {};

    var softIrqGroupStatData = {};
    var softIrqGroupStatMessages = {};

    cpuStatData = data['cpu_stat'];
    $.each(cpuStatData, function(coreName, coreStatData ) {
        idleStatData[coreName] = coreStatData.idle;
        userGroupStatData[coreName] = parseFloat(coreStatData.user) + parseFloat(coreStatData.system) + parseFloat(coreStatData.nice);
        // irqGroupStatData[coreName] = parseFloat(coreStatData.irq) + parseFloat(coreStatData.soft);

        idleStatMessages[coreName] = messages[coreName];
        // irqGroupStatMessages[coreName] = messages[coreName];
    });
    
    this.idleChart.updateChartData(idleStatData, idleStatMessages);
    
    this.userGroupChart.updateChartData(userGroupStatData);

    irqGroupStatData = data['irq']
    $.each(irqGroupStatData, function(coreName, coreStatData ) {
        irqGroupStatMessages[coreName] = messages[coreName];
    });
    console.log(irqGroupStatData)
    this.irqGroupChart.updateChartData(irqGroupStatData, irqGroupStatMessages);

    softIrqGroupStatData = data['softirq']
    $.each(softIrqGroupStatData, function(coreName, coreStatData ) {
        softIrqGroupStatMessages[coreName] = messages[coreName];
    });
    console.log(softIrqGroupStatData)
    this.softIrqGroupChart.updateChartData(softIrqGroupStatData, softIrqGroupStatMessages);
};

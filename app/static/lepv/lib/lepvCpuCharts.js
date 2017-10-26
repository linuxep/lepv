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
    this.nettxIrqGroupChart = new LepvIrqLineChart(chartDivNames.nettxIrqGroupDivName, 'CPU Stat: SoftIRQ- NET_TX');
    this.netrxIrqGroupChart = new LepvIrqLineChart(chartDivNames.netrxIrqGroupDivName, 'CPU Stat: SoftIRQ- NET_RX');
    this.taskletIrqGroupChart = new LepvIrqLineChart(chartDivNames.taskletIrqGroupDivName, 'CPU Stat: SoftIRQ- TASKLET');
    this.hrtimerIrqGroupChart = new LepvIrqLineChart(chartDivNames.hrtimerIrqGroupDivName, 'CPU Stat: SoftIRQ- HRTIMER');
    
    this.gaugeChart = new LepvGaugeChart(chartDivNames.gaugeDivName);
};

LepvCpuCharts.prototype = Object.create(LepvChart.prototype);
LepvCpuCharts.prototype.constructor = LepvCpuCharts;

LepvCpuCharts.prototype.initializeControlElements = function() {
    this.donutChart.initializeControlElements();
    this.idleChart.initializeControlElements();
    this.userGroupChart.initializeControlElements();
    this.irqGroupChart.initializeControlElements();
    this.nettxIrqGroupChart.initializeControlElements();
    this.netrxIrqGroupChart.initializeControlElements();
    this.taskletIrqGroupChart.initializeControlElements();
    this.hrtimerIrqGroupChart.initializeControlElements();
};

LepvCpuCharts.prototype.initialize = function() {

    this.gaugeChart.initialize();
    
    this.donutChart.initialize();
    this.idleChart.initialize();
    this.userGroupChart.initialize();
    this.irqGroupChart.initialize();
    this.nettxIrqGroupChart.initialize();
    this.netrxIrqGroupChart.initialize();
    this.taskletIrqGroupChart.initialize();
    this.hrtimerIrqGroupChart.initialize();
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

    var irqGroupStatMessages = {};
    irqGroupStatData = data['irq']
    $.each(irqGroupStatData, function(coreName, coreStatData ) {
        irqGroupStatMessages[coreName] = messages[coreName];
    });
    // console.log(irqGroupStatData)
    this.irqGroupChart.updateChartData(irqGroupStatData, irqGroupStatMessages);

    var nettxIrqGroupStatData = {};
    var netrxIrqGroupStatData = {};
    var taskletIrqGroupStatData = {};
    var hrtimerIrqGroupStatData = {};
    var softIrqGroupStatMessages = {};
    softIrqGroupStatData = data['softirq']

    $.each(softIrqGroupStatData, function(coreName, coreStatData ) {
        nettxIrqGroupStatData[coreName] = coreStatData['NET_TX'];
        netrxIrqGroupStatData[coreName] = coreStatData['NET_RX'];
        taskletIrqGroupStatData[coreName] = coreStatData['TASKLET'];
        hrtimerIrqGroupStatData[coreName] = coreStatData['HRTIMER'];
        softIrqGroupStatMessages[coreName] = messages[coreName];
    });
    // console.log(softIrqGroupStatData)
    this.netrxIrqGroupChart.updateChartData(netrxIrqGroupStatData, softIrqGroupStatMessages);
    this.nettxIrqGroupChart.updateChartData(nettxIrqGroupStatData, softIrqGroupStatMessages);
    this.taskletIrqGroupChart.updateChartData(taskletIrqGroupStatData, softIrqGroupStatMessages);
    this.hrtimerIrqGroupChart.updateChartData(hrtimerIrqGroupStatData, softIrqGroupStatMessages);
};

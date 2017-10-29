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
    this.irqChart = new LepvIrqLineChart(chartDivNames.irqDivName, 'CPU Stat: IRQ');
    this.nettxIrqChart = new LepvIrqLineChart(chartDivNames.nettxIrqDivName, 'CPU Stat: SoftIRQ- NET_TX');
    this.netrxIrqChart = new LepvIrqLineChart(chartDivNames.netrxIrqDivName, 'CPU Stat: SoftIRQ- NET_RX');
    this.taskletIrqChart = new LepvIrqLineChart(chartDivNames.taskletIrqDivName, 'CPU Stat: SoftIRQ- TASKLET');
    this.hrtimerIrqChart = new LepvIrqLineChart(chartDivNames.hrtimerIrqDivName, 'CPU Stat: SoftIRQ- HRTIMER');
    
    this.gaugeChart = new LepvGaugeChart(chartDivNames.gaugeDivName);
};

LepvCpuCharts.prototype = Object.create(LepvChart.prototype);
LepvCpuCharts.prototype.constructor = LepvCpuCharts;

LepvCpuCharts.prototype.initializeControlElements = function() {
    this.donutChart.initializeControlElements();
    this.idleChart.initializeControlElements();
    this.userGroupChart.initializeControlElements();
    this.irqGroupChart.initializeControlElements();
    this.irqChart.initializeControlElements();
    this.nettxIrqChart.initializeControlElements();
    this.netrxIrqChart.initializeControlElements();
    this.taskletIrqChart.initializeControlElements();
    this.hrtimerIrqChart.initializeControlElements();
};

LepvCpuCharts.prototype.initialize = function() {

    this.gaugeChart.initialize();
    
    this.donutChart.initialize();
    this.idleChart.initialize();
    this.userGroupChart.initialize();
    this.irqGroupChart.initialize();
    this.irqChart.initialize();
    this.nettxIrqChart.initialize();
    this.netrxIrqChart.initialize();
    this.taskletIrqChart.initialize();
    this.hrtimerIrqChart.initialize();
};

LepvCpuCharts.prototype.updateChartData = function(data, messages=[]) {
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
    var irqGroupStatMessages = [];

    cpuStatData = data['cpu_stat'];
    $.each(cpuStatData, function(coreName, coreStatData ) {
        idleStatData[coreName] = coreStatData.idle;
        userGroupStatData[coreName] = parseFloat(coreStatData.user) + parseFloat(coreStatData.system) + parseFloat(coreStatData.nice);
        irqGroupStatData[coreName] = parseFloat(coreStatData.irq) + parseFloat(coreStatData.soft);

    });
    irqGroupStatMessages = messages;
    
    this.idleChart.updateChartData(idleStatData, idleStatMessages);
    
    this.userGroupChart.updateChartData(userGroupStatData);
    this.irqGroupChart.updateChartData(irqGroupStatData, messages);

    var irqStatMessages = {};
    var irqStatMessages = {};
    irqStatData = data['irq']
//    $.each(irqStatData, function(coreName, coreStatData ) {
//        irqStatMessages[coreName] = messages[coreName];
//    });
    // console.log(irqGroupStatData)
    this.irqChart.updateChartData(irqStatData, messages);

    var nettxIrqStatData = {};
    var netrxIrqStatData = {};
    var taskletIrqStatData = {};
    var hrtimerIrqStatData = {};
    var softIrqStatMessages = {};
    softIrqStatData = data['softirq']

    $.each(softIrqStatData, function(coreName, coreStatData ) {
        nettxIrqStatData[coreName] = coreStatData['NET_TX'];
        netrxIrqStatData[coreName] = coreStatData['NET_RX'];
        taskletIrqStatData[coreName] = coreStatData['TASKLET'];
        hrtimerIrqStatData[coreName] = coreStatData['HRTIMER'];
//        softIrqStatMessages[coreName] = messages[coreName];
    });
    // console.log(softIrqStatData)
    this.netrxIrqChart.updateChartData(netrxIrqStatData, []);
    this.nettxIrqChart.updateChartData(nettxIrqStatData, []);
    this.taskletIrqChart.updateChartData(taskletIrqStatData, []);
    this.hrtimerIrqChart.updateChartData(hrtimerIrqStatData, []);
};

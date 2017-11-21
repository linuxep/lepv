/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var ProcrankFreeVsPieChart = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);
    this.chartTitle = "RAM Chart";
    this.chartHeaderColor = 'green';

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'memory.procrank';
    this.isLeadingChart = false;

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};

    this.maxDataCount = 150;
    this.refreshInterval = 2;


    // this.updateChartHeader();
    this.initializeChart();

    this.setupSocketIO();
};

ProcrankFreeVsPieChart.prototype = Object.create(LepvChart.prototype);
ProcrankFreeVsPieChart.prototype.constructor = ProcrankFreeVsPieChart;

ProcrankFreeVsPieChart.prototype.initializeChart = function() {
    
   this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
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

ProcrankFreeVsPieChart.prototype.updateChartData = function(response) {
    // console.log(response)
    sumData = response['data']['sum']
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

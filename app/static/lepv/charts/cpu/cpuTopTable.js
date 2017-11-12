/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuTopTable = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.socket_message_key = 'cpu.top';
    
//    this.setTableDivName(rootDivName);
    
    this.chartTitle = "CPU Top Table";
    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 25;
    this.refreshInterval = 5;

    // this.updateChartHeader();
    this.initializeChart();
    this.setupSocketIO();
};

CpuTopTable.prototype = Object.create(LepvChart.prototype);
CpuTopTable.prototype.constructor = CpuTopTable;

CpuTopTable.prototype.initializeChart = function() {

    if (!this.chartDivName) {
        console.log("The table div name was not specified for " + this.chartDivName);
        return;
    }
};

CpuTopTable.prototype.updateChartData = function(response) {
    data = response['data']
    // console.log(data)
    var thisChart = this;
    
    if (!this.table) {
        this.initializeDataTable(data['headerline']);
    }
    
    this.table.rows().remove().draw( true );

    var headerColumns = data['headerline'].split(/\s+/);

    var topData = data['top'];
    if (topData) {
        $.each( topData, function( lineIndex, dataItem ) {

            if (lineIndex >= thisChart.maxDataCount) {
                return;
            }
            
            var rowData = [];
            headerColumns.forEach(function(value, index) {
                rowData.push(dataItem[value]);
            });

            thisChart.table.row.add(rowData);

        });
    } else {
        var rowData = [];
        var columnCount = headerColumns.size();
        while(columnCount--) {
            rowData.push("--")
        }

        thisChart.table.row.add(rowData);
    }
    
    this.table.draw(true);
    
    this.requestData();
};

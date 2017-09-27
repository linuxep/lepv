/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvCpuTopTable = function(divName, tableDivName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    
    this.setTableDivName(tableDivName);
    
    this.chartTitle = "CPU Top Table";
    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 25;
    this.refreshInterval = 5;

    this.dataUrlPrefix = "/api/cpu/top/";

    this.updateChartHeader();
    this.initialize();
};

LepvCpuTopTable.prototype = Object.create(LepvChart.prototype);
LepvCpuTopTable.prototype.constructor = LepvCpuTopTable;

LepvCpuTopTable.prototype.initialize = function() {

    if (!this.tableDivName) {
        console.log("The table div name was not specified for " + this.chartDivName);
        return;
    }
};

LepvCpuTopTable.prototype.updateChartData = function(data) {

    var thisChart = this;
    
    if (!this.table) {
        this.initializeDataTable(data.headerline);
    }
    
    this.table.rows().remove().draw( true );

    var headerColumns = data.headerline.split(/\s+/);

    var topData = data.top;
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
};

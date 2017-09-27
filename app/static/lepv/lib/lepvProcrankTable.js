/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvProcrankTable = function(divName, tableDivName, pssPieDivName, freeVsPssDivName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    this.setTableDivName(tableDivName);
    
    this.chartTitle = "Memory Stat Table";
    this.chartHeaderColor = 'green';
    
    this.maxDataCount = 25;
    this.refreshInterval = 5;

    this.dataUrlPrefix = "/api/memory/procrank/";
    
    this.updateChartHeader();
    this.initialize();

    this.pssData = [];
    this.pssBenchmark = 200;
    this.pssPieChart = new LepvProcrankPssPieChart(pssPieDivName);
    this.FreeVsPssChart = new LepvProcrankFreeVsPieChart(freeVsPssDivName);
};

LepvProcrankTable.prototype = Object.create(LepvChart.prototype);
LepvProcrankTable.prototype.constructor = LepvProcrankTable;

LepvProcrankTable.prototype.initialize = function() {

    this.table = $(this.tableDivName).DataTable( {
        destroy: true,
        paging: false,
        info: false,
        searching: true,
        columns: [
            { title: "PID", orderable: false },
            { title: "VSS", orderable: false },
            { title: "RSS", orderable: false },
            { title: "PSS", orderable: true },
            { title: "USS", orderable: false },
            { title: "CMDLINE", orderable: false }
        ],
        order: [[ 4, "desc" ]]
    });
};

LepvProcrankTable.prototype.updateChartData = function(data) {

    this.updateStatTableData(data.procranks);
    
    this.pssPieChart.updateChartData(this.pssData);
    this.FreeVsPssChart.updateChartData(data.sum);
};

LepvProcrankTable.prototype.updateStatTableData = function(procranks) {

    var thisChart = this;

    var index = 0;
    this.pssData = [];
    this.table.rows().remove().draw( true );
    if (procranks != null) {
        $.each( procranks, function( lineIndex, dataItem ) {

            if (lineIndex >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                dataItem.pid,
                dataItem.vss,
                dataItem.rss,
                dataItem.pss,
                dataItem.uss,
                dataItem.cmdline
            ]);
            
            if (dataItem.pss > thisChart.pssBenchmark) {
                thisChart.pssData.push([dataItem.cmdline, dataItem.pss]);
            }
            
            index = index + 1;
        });
    } else {
        while(index < maxDataCount) {
            thisChart.table.row.add([
                "--",
                "--",
                "--",
                "--",
                "--",
                "--"
            ]);
            index = index + 1;
        }
    }
    this.table.draw(true);
};

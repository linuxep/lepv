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

    this.dataUrlPrefix = "/cputop/";

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
    
    this.table = $(this.tableDivName).DataTable( {
        destroy: true,
        paging: false,
        info: false,
        searching: true,
        columns: [
            {
                title: "PID",
                orderable: false
            },
            {
                title: "User",
                orderable: false
            },
            {
                title: "PRI",
                orderable: false
            },
            {
                title: "NI",
                orderable: false
            },
            {
                title: "VSZ",
                orderable: false
            },
            {
                title: "RSS",
                orderable: false
            },
            {
                title: "S",
                orderable: false
            },
            {
                title: "%CPU"
            },
            {
                title: "%MEM",
                orderable: false
            },
            {
                title: "Time",
                orderable: false
            },
            {
                title: "Command",
                orderable: false
            }
        ],
        order: [[ 7, "desc" ]],
    });
};

LepvCpuTopTable.prototype.updateChartData = function(data) {

    var thisChart = this;
    
    this.table.rows().remove().draw( true );
    var lineCount = 0;
    if (data != null) {
        $.each( data, function( processId, dataItem ) {

            if (lineCount >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                processId,
                dataItem['user'],
                dataItem['pri'],
                dataItem['ni'],
                dataItem['vsz'],
                dataItem['rss'],
                dataItem['s'],
                dataItem['cpu'],
                dataItem['mem'],
                dataItem['time'],
                dataItem['command']
            ]);

            lineCount = lineCount + 1;
        });
    } else {
        while(lineCount < thisChart.maxDataCount) {
            thisChart.table.row.add([
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--"
            ]);
            lineCount = lineCount + 1;
        }
    }
    this.table.draw(true);
};

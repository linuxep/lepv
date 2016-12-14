/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvIOPPTable = function(divName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    
    this.chartTitle = "IOPP Table";
    this.chartHeaderColor = 'yellow';
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;

    this.dataUrlPrefix = "/status/iopp/";

    this.updateChartHeader();
    this.initialize();
};

LepvIOPPTable.prototype = Object.create(LepvChart.prototype);
LepvIOPPTable.prototype.constructor = LepvIOPPTable;

LepvIOPPTable.prototype.initialize = function() {

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
                title: "RCHAR",
                orderable: false
            },
            {
                title: "WCHAR",
                orderable: false
            },
            {
                title: "SYSCR",
                orderable: false
            },
            {
                title: "SYSCW",
                orderable: false
            },
            {
                title: "RBYTES",
                orderable: false
            },
            {
                title: "WBYTES",
                orderable: true
            },
            {
                title: "CWBYTES",
                orderable: true
            },
            {
                title: "COMMAND",
                orderable: false
            }
        ],
        order: [[ 7, "desc" ], [4, "desc"], [5, "desc"], [6, "desc"]]
    });
};

LepvIOPPTable.prototype.updateChartData = function(data) {

    var thisChart = this;
    
    this.table.rows().remove().draw( true );
    if (data != null) {
        $.each( data, function( itemIndex, ioppData ) {

            if (itemIndex >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                ioppData['pid'],
                ioppData['rchar'],
                ioppData['wchar'],
                ioppData['syscr'],
                ioppData['syscw'],
                ioppData['rbytes'],
                ioppData['wbytes'],
                ioppData['cwbytes'],
                ioppData['command']
            ]);
        });
    } else {
        var index = 0;
        while(index < thisChart.maxDataCount) {
            thisChart.table.row.add([
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
            index = index + 1;
        }
    }
    this.table.draw(true);
};

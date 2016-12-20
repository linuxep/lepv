/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvIOTopTable = function(divName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    
    this.chartTitle = "IO Top Table";
    this.chartHeaderColor = 'yellow';
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;

    this.dataUrlPrefix = "/status/iotop/";

    this.updateChartHeader();
    this.initialize();
};

LepvIOTopTable.prototype = Object.create(LepvChart.prototype);
LepvIOTopTable.prototype.constructor = LepvIOTopTable;

LepvIOTopTable.prototype.initialize = function() {

    this.table = $(this.tableDivName).DataTable( {
        destroy: true,
        paging: false,
        info: false,
        searching: true,
        columns: [
            {
                title: "TID",
                orderable: false
            },
            {
                title: "PRIO",
                orderable: false
            },
            {
                title: "USER",
                orderable: false
            },
            {
                title: "DISK READ",
                orderable: true
            },
            {
                title: "DISK WRITE",
                orderable: true
            },
            {
                title: "SWAPIN",
                orderable: false
            },
            {
                title: "IO",
                orderable: false
            },
            {
                title: "COMMAND",
                orderable: false
            }
        ],
        order: [[4, "desc"], [5, "desc"]]
    });
};

LepvIOTopTable.prototype.updateChartData = function(data) {

    var thisChart = this;
    
    this.table.rows().remove().draw( true );
    if (data != null) {
        $.each( data, function( itemIndex, ioppData ) {

            if (itemIndex >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                ioppData['TID'],
                ioppData['PRIO'],
                ioppData['USER'],
                ioppData['READ'],
                ioppData['WRITE'],
                ioppData['SWAPIN'],
                ioppData['IO'],
                ioppData['COMMAND']
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
                "--"
            ]);
            index = index + 1;
        }
    }
    this.table.draw(true);
};

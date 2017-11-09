/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var IoTopTable = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.socket_message_key = 'io.top';
    
    this.setTableDivName(rootDivName);
    
    this.chartTitle = "IO Top Table";
    this.chartHeaderColor = 'yellow';
    
    this.maxDataCount = 25;
    this.refreshInterval = 5;

    this.initializeChart();
    this.setupSocketIO();
};

IoTopTable.prototype = Object.create(LepvChart.prototype);
IoTopTable.prototype.constructor = IoTopTable;

IoTopTable.prototype.initializeChart = function() {
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

IoTopTable.prototype.updateChartData = function(response) {
    console.log(response)
    data = response['data']
    // console.log(data)
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
            index = index + 1;
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
    
    this.requestData();
};

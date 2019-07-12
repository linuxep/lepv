/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var PerfCpuTable = function (rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'perf.cpuclock';

    this.chartTitle = "Perf Table";
    this.chartHeaderColor = 'blue';

    this.maxDataCount = 25;
    this.refreshInterval = 5;

    this.initializeChart();
    this.setupSocketIO();
};

PerfCpuTable.prototype = Object.create(LepvChart.prototype);
PerfCpuTable.prototype.constructor = PerfCpuTable;

PerfCpuTable.prototype.initializeChart = function () {
    this.table = $('#' + this.mainDivName).DataTable({
        destroy: true,
        paging: false,
        info: false,
        searching: true,
        columns: [
            {
                title: "Command",
                orderable: false
            },
            {
                title: "Overhead",
                orderable: false
            },
            {
                title: "Shared Object",
                orderable: false
            },
            {
                title: "Symbol",
                orderable: false
            }
        ],
        order: [[1, "desc"]]
    });
};

PerfCpuTable.prototype.updateChartData = function (response) {
    var thisChart = this;
    var data = response['data'];
    if (!data && typeof (data) != 'undefined' && data != 0) {
        return
    }
    if (typeof (data) == "undefined") {
        return
    }
    console.log(data)

    this.table.rows().remove().draw(true);
    if (data != null) {
        $.each(data, function (itemIndex, dataItem) {

            if (itemIndex >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                dataItem['Command'],
                dataItem['Overhead'],
                dataItem['Shared Object'],
                dataItem['Symbol']
            ]);
            index = index + 1;
        });
    } else {
        var index = 0;
        while (index < thisChart.maxDataCount) {
            thisChart.table.row.add([
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

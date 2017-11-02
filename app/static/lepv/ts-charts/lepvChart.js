var TsLepvChart = /** @class */ (function () {
    function TsLepvChart(rootDivName, socket, server) {
        console.log("constructing " + rootDivName);
        this.rootDivName = rootDivName;
        this.socketIO = socket;
        this.serverToMonitor = server;
        this.socketMessageKey = 'cpu.stat';
        this.isLeadingChart = true;
        this.setupSocketIO();
    }
    /**
     * setupSocketIO
     */
    TsLepvChart.prototype.setupSocketIO = function () {
        this.socketIO.on(this.socketMessageKey + ".res", function (response) {
            console.log("  <- " + this.socketMessageKey + ".res");
            this.updateChartData(response);
        });
        if (this.isLeadingChart) {
            this.requestData();
        }
    };
    /**
     * requestData
     */
    TsLepvChart.prototype.requestData = function () {
        if (this.socketMessageKey == null) {
            return;
        }
        if (!this.isLeadingChart) {
            return;
        }
        this.socketIO.emit(this.socketMessageKey + ".req", { 'server': this.serverToMonitor });
    };
    /**
     * initialize
     */
    TsLepvChart.prototype.initializeChart = function () {
    };
    /**
     * refreshData
     */
    TsLepvChart.prototype.refreshData = function () {
    };
    /**
     * locateControlElements
     */
    TsLepvChart.prototype.locateControlElements = function () {
    };
    /**
     * alert
     */
    TsLepvChart.prototype.alert = function (message) {
    };
    /**
     * name
     */
    TsLepvChart.prototype.clearAlert = function () {
    };
    return TsLepvChart;
}());

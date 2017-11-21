/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChart = function(rootDivName, socket, server) {

  this.rootDivName = rootDivName;
  this.headerDiv = null;
  this.chartDiv = null;
  this.footerDiv = null;
  this.footerIcon = null;
  this.mainDivName = null;
  this.mainDiv = null;
  this.locateUIElements();

  this.socketIO = socket;

  this.serverToWatch = server;

  this.socket_message_key = null;
  this.socket_request_id = 0;

  this.chart = null;
  this.table = null;
  
  this.chartData = {};
  this.timeData = ['x'];

  // if this is a leading chart, it will send socket message to backend proactively
  // otherwise, it just listen to message, but not send.
  this.isLeadingChart = true;


//  this.initializeChart();
//  this.setupSocketIO();

};

LepvChart.prototype.locateUIElements = function() {

    var thisChart = this;

    if (this.rootDivName.startsWith('#')) {
        this.rootDivName = divName.substr(1);
    }

    this.rootDiv = $("#" + this.rootDivName)[0];

    this.headerDiv = $("#" + this.rootDivName).find("div.card-header")[0];

    this.footerDiv = $("#" + this.rootDivName).children("div.card-footer")[0];
//    this.footerIcon = this.footerDiv.firstElementChild;

//    var chartDiv = this.rootDiv.children("chart-panel")[0];

    // TODO, locate the control elements
    this.mainDivName = this.rootDivName.replace("container-", "");
//    this.mainDiv = $("#" + this.rootDivName).children("div.chart-panel")[0];
//    this.mainDiv.attr("id", this.mainDivName);

    var s = "";
//    this.mainDivName = this.mainDiv.getAttribute('name');

};

LepvChart.prototype.setupSocketIO = function() {

    var thisChart = this;

    this.socketIO.on(thisChart.socket_message_key + ".res", function(response) {

        console.log("  <- " + thisChart.socket_message_key + ".res(" + response['response_id'] + ")");

        if ("request_time" in response) {
            var requestTime = response['request_time'];

            var responseTime = (new Date()).getTime();

            var requestDuration = responseTime - requestTime;
            console.log("  <- " + thisChart.socket_message_key + ".res(" + response['response_id'] + ") in " + requestDuration + " milliseconds");

        }

        thisChart.updateChartData(response);
    });

    if (this.isLeadingChart) {
        this.requestData();
    }

};


LepvChart.prototype.requestData = function() {

    if (this.socket_message_key == null) {
        return;
    }

    if (! this.isLeadingChart) {
        return;
    }

    this.socket_request_id++;
    console.log(" ->   " + this.socket_message_key + ".req(" + (this.socket_request_id) + ") for " + this.serverToWatch);
    this.socketIO.emit(this.socket_message_key + ".req",
                            {
                                'server': this.serverToWatch,
                                "request_id": this.socket_request_id,
                                "request_time": (new Date()).getTime(),
                            }
    );
};


LepvChart.prototype.initializeChart = function() {
    console.log("initializeChart() method needs to be overwritten by sub-classes!");
};


LepvChart.prototype.updateChartData = function(responseData) {
    console.log("updateChartData() method needs to be overwritten by sub-classes!");
};

LepvChart.prototype.setTableDivName = function(tableDivName) {
  if (tableDivName.startsWith('#')) {
    this.tableDivName = tableDivName;
  } else {
    this.tableDivName = '#' + tableDivName;
  }
};

LepvChart.prototype.initializeDataTable = function(headerLine) {
  
  var headerColumns = headerLine.split(/\s+/);
  
  var columns = [];
  headerColumns.forEach(function(value, index) {
    var columnItem = {};
    columnItem['title'] = value;
    columnItem['orderable'] = false;
    
    columns.push(columnItem);
  });
  
  this.table = $(this.tableDivName).DataTable( {
    destroy: true,
    paging: false,
    info: false,
    searching: true,
    columns: columns,

    // TODO: refactor so we can allow for chart-specific sorting
    order: []
  });
};



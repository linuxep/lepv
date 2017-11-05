/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChart = function(rootDivName, socket, server) {

  this.rootDiv = $("#" + rootDivName);
  this.socketIO = socket;

   this.headerDiv = null;
   this.chartDiv = null;
   this.footerDiv = null;
   this.mainDivName = null;

   this.serverToWatch = server;

  this.socket_message_key = null;
  this.socket_request_id = 0;
  this.chart = null;
  this.chartData = {};
  this.timeData = ['x'];

  // if this is a leading chart, it will send socket message to backend proactively
  // otherwise, it just listen to message, but not send.
  this.isLeadingChart = true;

  this.locateUIElements();

  this.initializeChart();
  this.setupSocketIO();

};

LepvChart.prototype.locateUIElements = function() {

    var thisChart = this;

//    <div id="div-cpu-stat-idle" class="card mb-3">
//      <div class="card-header">
//        <i class="icon-cpu-processor"></i> CPU Stat: Idle</div>
//      <div class="card-body">
//        <div id="div-cpu-stat-idle-panel" class="chart-panel"></div>
//      </div>
//      <div class="card-footer small text-muted" hidden>
//        <span></span>
//      </div>
//    </div>

    var rootDivName = 'div-root-cpu-stat-donut';

    var rootDiv = $("#" + rootDivName);

    var headerDiv = rootDiv.children("div.card-header")[0];

    var footerDiv = rootDiv.children("div.card-footer")[0];
    var footerIcon = footerDiv.firstElementChild;
//    footerIcon.text("dfjaskldfjalskdjfalskdjflasdjf");

    var chartDiv =  rootDiv.children("chart-panel")[0];

    // TODO, locate the control elements

//    this.mainDiv = this.rootDiv.children("div.chart-panel").attr('id', 'sdfsfsdf');
//    this.mainDivName = this.mainDiv.getAttribute('name');

};

LepvChart.prototype.setupSocketIO = function() {

    var thisChart = this;

    this.socketIO.on(thisChart.socket_message_key + ".res", function(response) {

        console.log("  <- " + thisChart.socket_message_key + ".res(" + response['response_id'] + ")");

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
    this.socketIO.emit(this.socket_message_key + ".req", {'server': this.serverToWatch, "request_id": this.socket_request_id});
};


LepvChart.prototype.initializeChart = function() {
    console.log("initializeChart() method needs to be overwritten by sub-classes!");
};


LepvChart.prototype.updateChartData = function(responseData) {
    console.log("updateChartData() method needs to be overwritten by sub-classes!");
};



/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChart = function(rootDivName, socket) {

  this.rootDiv = $("#" + rootDivName);
  this.socketIO = socket;

   this.headerDiv = null;
   this.mainDiv = null;

   this.serverToWatch = 'www.rmlink.cn';

  this.socket_message_key = null;
  this.socket_request = null;
  this.socket_response = null;
  this.chart = null;
  this.chartData = null;

  this.initializeChart();
  this.setupSocketIO();

};

LepvChart.prototype.setupSocketIO = function() {

    var thisChart = this;

    this.socketIO.on(thisChart.socket_message_key + ".res", function(response) {

        console.log("Socket Message received: " + thisChart.socket_message_key + ".res");

        thisChart.updateChartData(response);
    });

    this.requestData();
};


LepvChart.prototype.requestData = function() {

    if (this.socket_message_key == null) {
        return;
    }

    this.socketIO.emit(this.socket_message_key + ".req", {'server': this.serverToWatch})
};


LepvChart.prototype.initializeChart = function() {
    console.log("initializeChart() method needs to be overwritten by sub-classes!")
};


LepvChart.prototype.updateChartData = function(responseData) {
    console.log("updateChartData() method needs to be overwritten by sub-classes!")
};



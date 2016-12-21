/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvGauge = function(divName) {
  this.setDivName(divName);
  
  this.chartDiv = null;
  if (this.chartDivName != '') {
    this.chartDiv = $(this.chartDivName);
  }
  
};

LepvGauge.prototype.setDivName = function(divName) {
  if (divName.startsWith('#')) {
    this.chartDivName = divName;
  } else {
    this.chartDivName = '#' + divName;
  }
};

LepvGauge.prototype.createGauge = function(gaugeId) {
  // TODO: create a gauge with the given id.
};

LepvGauge.prototype.start = function(server) {
  //console.log("start() method needs to be overwritten by sub-classes!")
};
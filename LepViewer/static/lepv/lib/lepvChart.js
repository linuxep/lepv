/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChart = function(divName = '') {
  this.chartDivName = divName;
  this.charts = null;
  this.chartTitle = null;
  this.chartHeaderColor = 'grey';

  this.controlElements = {};

  this.maxDataCount = 150;
  this.refreshInterval = 2; // in seconds
  
  this.isChartPaused = false;
  this.invervalId = null;
  
  this.server = null;
  
  this.requestId = null;
  this.responseId = null;
  
  this.config = 'release';
  
  this.data = {};
  this.dataUrl = null;

  this.initializeControlElements();
};

LepvChart.prototype.report = function() {
  console.log("Reporting from LepvChart");
  
  console.log("Max Data Count: " + this.maxDataCount);
  console.log("refresh interval: " + this.refreshInterval);
  
  console.log("");
};

LepvChart.prototype.initializeControlElements = function() {
  if (this.chartDivName == '') {
    return;
  }
  
  this.controlElements = createControlElements($('#' + this.chartDivName), this.chartHeaderColor);

  this.controlElements.pauseResumeLink.click(function(){
    this.isChartPaused = onPauseOrResume(this.controlElements.pauseResumeDiv, 
        this.isChartPaused, 
        this.controlElements.headingParentDiv, 
        this.chartHeaderColor);
  });
  
  this.controlElements.configLink.click(function(){
    onConfig(this.chartTitle + " Configuration",
        this.updateConfigs,
        this.refreshInterval,
        this.maxDataCount);
  });
};


LepvChart.prototype.updateConfigs = function(newConfigs) {
  this.maxDataCount = newConfigs.maxDataCount;

  var updatedRefreshInterval = newConfigs.refreshInterval;
  if (updatedRefreshInterval != this.refreshInterval) {
    this.refreshInterval = newConfigs.refreshInterval;

    clearInterval(this.invervalId);

    this.intervalId = setInterval(function () {
      this.refreshChart();
    }, this.refreshInterval * 1000);
  }
};

LepvChart.prototype.refreshChart = function() {
  // TODO:
};


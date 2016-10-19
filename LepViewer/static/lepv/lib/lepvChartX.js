/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChart = function(divName, dataUrlPrefix) {
  this.chartDivName = divName;
  this.chart = null;
  this.chartTitle = this.chartDivName + " Chart";

  this.controlElements = {};

  this.maxDataCount = 150;
  this.refreshInterval = 2; // in seconds
  this.isChartPaused = false;
  this.invervalId = null;
  
  this.server = Cookies.get('server');
  this.port = Cookies.get('port');
  this.dataUrl = dataUrlPrefix + this.server + "/" + this.port;

  this.initializeControlElements();
};

LepvChart.prototype.initializeControlElements = function() {
  //  create the control elements( config, resume, pause )
  // the element creation logic is in config.js
  this.controlElements = createControlElements($('#' + this.chartDivName),
      chartHeaderColor);

  this.controlElements.pauseResumeLink.click(function(){
    this.isChartPaused = onPauseOrResume(this.controlElements.pauseResumeDiv, this.isChartPaused);
  });

  this.controlElements.configLink.click(function(){
    onConfig(this.chartTitle + " Configuration",
        this.updateConfigs,
        this.refreshInterval,
        this.maxDataCount);
  });
};


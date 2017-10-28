/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChart = function(divName) {
  this.setDivName(divName);
  this.tableDivName = null;
  this.chartDiv = null;
  if (this.chartDivName != '') {
    this.chartDiv = $('#' + this.chartDivName);
  }
  
  this.charts = null;
  this.chart = null;
  this.table = null;
  this.chartTitle = null;
  this.chartHeaderColor = 'grey';

  this.controlElements = {};
  this.configDialog = null;

  this.maxDataCount = 150;
  this.refreshInterval = 2; // in seconds
  
  this.isChartPaused = false;
  this.intervalId = null;
  
  this.server = null;
  
  this.requestId = null;
  this.responseId = null;
  this.maxRequestIdGap = 2;
  
  this.executionConfig = 'release';
  
  this.chartData = {};
  this.timeData = ['x'];
  this.dataUrlPrefix = null;
  
  // if "proactive" is true, this chart will get data by sending out http requests "proactive"ly
  // otherwise, it waits for other source ( other leader chart ) to
  // get data by http and feed it with the data.
  this.proactive = true;

  this.initializeControlElements();
};

LepvChart.prototype.setDivName = function(divName) {
  if (divName.startsWith('#')) {
    this.chartDivName = divName.substr(1);
  } else {
    this.chartDivName = divName;
  }
};

LepvChart.prototype.setTableDivName = function(tableDivName) {
  if (tableDivName.startsWith('#')) {
    this.tableDivName = tableDivName;
  } else {
    this.tableDivName = '#' + tableDivName;
  }
};

LepvChart.prototype.updateChartHeader = function() {

  var divHeadingParentPanelColorClass = 'panel-' + this.chartHeaderColor;
  
  if (this.isChartPaused) {
    this.controlElements.pauseResumeDiv.removeClass("glyphicon-pause");
    this.controlElements.pauseResumeDiv.addClass("glyphicon-play");

    this.controlElements.pauseResumeDiv.tooltip('hide').attr("data-original-title", "点击以继续刷新");

    this.controlElements.headingParentDiv.removeClass(divHeadingParentPanelColorClass);
    this.controlElements.headingParentDiv.addClass('panel-grey');
    
  } else {
    this.controlElements.pauseResumeDiv.removeClass("glyphicon-play");
    this.controlElements.pauseResumeDiv.addClass("glyphicon-pause");

    this.controlElements.pauseResumeDiv.tooltip('hide').attr("data-original-title", "点击可暂停刷新");

    this.controlElements.headingParentDiv.removeClass('panel-grey');
    this.controlElements.headingParentDiv.addClass(divHeadingParentPanelColorClass);
  }
};

LepvChart.prototype.onPauseResume = function() {
  // Inside an event handler, "this" is the object that created the event!!!!!
  // unless we bind event???
  if (this.controlElements == null) {
    return;
  }
  
  this.isChartPaused = !this.isChartPaused;
  
  this.updateChartHeader();
};

LepvChart.prototype.onConfig = function() {

  if (this.controlElements == null) {
    return;
  }

  if (this.configDialog == null) {
    this.configDialog = new LepvChartConfig(this.updateConfigs, this);
    this.configDialog.saveButton.on("click", $.proxy(this.updateConfigs, this));
  }

  this.configDialog.show({'refreshInterval': this.refreshInterval, 'maxDataCount': this.maxDataCount});
  
};

LepvChart.prototype.updateConfigs = function(newConfigs) {
  if (newConfigs.maxDataCount != null) {
    this.maxDataCount = newConfigs.maxDataCount;
  }
  
  if (newConfigs.refreshInterval != null) {
    var updatedRefreshInterval = newConfigs.refreshInterval;
    if (updatedRefreshInterval != this.refreshInterval) {
      this.refreshInterval = newConfigs.refreshInterval;

      var thisChart = this;
      clearInterval(this.intervalId);
      this.intervalId = setInterval(function () {
        thisChart.refresh();
      }, this.refreshInterval * 1000);
    }
  }
};

LepvChart.prototype.initializeControlElements = function() {
  if (this.chartDiv == null) {
    return;
  }

  this.createControlElements();

  // IMPORTANT:  $.proxy() is the way to get the event bind work here
  this.controlElements.pauseResumeLink.on("click", $.proxy(this.onPauseResume, this));
  this.controlElements.configLink.on("click", $.proxy(this.onConfig, this));
};

LepvChart.prototype.createControlElements = function() {
  if (this.chartDiv == null) {
    return;
  }

  //  // navigate to the title div
  var panelBodyDiv = this.chartDiv.parent();
  if ( ! panelBodyDiv.hasClass('panel-body')) {
    panelBodyDiv = panelBodyDiv.parent();
  }

  var divHeadingPanel = panelBodyDiv.siblings("div").first();
  if ( ! divHeadingPanel.hasClass('panel-heading')) {
    console.log("Failed to locate panel-heading div, not able to create control elements for " + this.chartDiv.getId());
    return;
  }

  // remove all the "a" children of the heading panel
  divHeadingPanel.children('a').remove();

  var divHeadingParentPanel = divHeadingPanel.parent();
  if (this.chartHeaderColor != null) {
    var divHeadingParentPanelColorClass = 'panel-' + this.chartHeaderColor;
    if (!divHeadingParentPanel.hasClass(divHeadingParentPanelColorClass)) {
      divHeadingParentPanel.addClass(divHeadingParentPanelColorClass);
    }
  }

  this.controlElements = {};

  //// config button
  var elementConfigLink = $("<a></a>");
  var elementConfigDiv = $("<div></div>")
      .attr("data-toggle", "tooltip")
      .attr("data-placement", "auto bottom")
      .attr("title", '设置');

  elementConfigDiv.addClass("pull-right glyphicon glyphicon-cog glyphicon-white");
  elementConfigLink.append(elementConfigDiv);
  divHeadingPanel.append(elementConfigLink);

  this.controlElements['configLink'] = elementConfigLink;
  this.controlElements['configDiv'] = elementConfigDiv;

  // pause/resume button
  var elementPauseResumeLink = $("<a></a>").attr("isPaused", this.isChartPaused);
  var elementPauseResumeDiv = $("<div></div>")
      .attr("data-toggle", "tooltip")
      .attr("data-placement", "auto bottom");
  elementPauseResumeDiv.addClass("pull-right glyphicon glyphicon-white");

  elementPauseResumeDiv.addClass("glyphicon-pause");
  elementPauseResumeDiv.attr("title", "点击可暂停刷新");

  elementPauseResumeLink.append(elementPauseResumeDiv);
  divHeadingPanel.append(elementPauseResumeLink);

  this.controlElements['pauseResumeLink'] = elementPauseResumeLink;
  this.controlElements['pauseResumeDiv'] = elementPauseResumeDiv;
  this.controlElements['headingParentDiv'] = divHeadingParentPanel;

  // find the footer div
  var panelFooter = divHeadingParentPanel.children('.panel-footer').first();
  if (panelFooter != null) {
    this.controlElements['panelFooter'] = panelFooter;

    var footerSpan = panelFooter.children('span').first();
    if (footerSpan != null) {
        this.controlElements['footerSpan'] = footerSpan;
    }

    var footerIcon = panelFooter.children('i').first();
    if (footerIcon != null) {
        this.controlElements['footerIcon'] = footerIcon;
    }

  }

};

LepvChart.prototype.start = function(serverToMonitor) {
  if (!serverToMonitor) {
    console.log("Please specify the server to monitor for " + this.chartDivName);
    return;
  }
  if (serverToMonitor == this.server) {
    return;
  }

  this.server = serverToMonitor;
  this.requestId = 0;
  this.responseId = 0;
  
  this.initialize();
  this.refresh();

  var thisChart = this;
  this.intervalId = setInterval(function () {
    thisChart.refresh();
  }, this.refreshInterval * 1000);
};

LepvChart.prototype.initialize = function(server) {
  console.log("initialize() method needs to be overwritten by sub-classes!")
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

LepvChart.prototype.updateChartData = function(responseData) {
  console.log("updateChartData() method needs to be overwritten by sub-classes!")
};

LepvChart.prototype.refresh = function() {
  
  if (!this.proactive) {
    // this is NOT a "proactive" chart, it does not make http requests to feed data.
    return;
  }
  
  if (this.isChartPaused) {
    return;
  }

//  if (this.requestId - this.responseId >= this.maxRequestIdGap) {
//    return;
//  }

  this.requestId++;
  //var startTime= new Date().getTime();

  //this.controlElements.configLink.on("click", $.proxy(this.onConfig, this));
  var thisChart = this;
  var url = thisChart.dataUrlPrefix + thisChart.server; // + "?request_id=" + thisChart.requestId;
  
  $.get(url, function(responseData, status) {
    if (this.isChartPaused) {
      return;
    }

    thisChart.responseId++;

    var dataMessages = {}
    if ('messages' in responseData) {
        dataMessages = responseData['messages']
    }
    
    thisChart.updateChartData(responseData['data'], dataMessages);
  });
};


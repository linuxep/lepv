/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChart = function(divName = '') {
  this.chartDivName = divName;
  this.chartDiv = null;
  if (this.chartDivName != '') {
    this.chartDiv = $('#' + this.chartDivName);
  }
  
  this.charts = null;
  this.chartTitle = null;
  this.chartHeaderColor = 'grey';

  this.controlElements = {};
  this.configDialog = null;

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
  
  // if the config dialog was created once, we don't bother to create it again.
  if (this.configDialog != null) {
    this.configDialog.modal();
    return;
  }

  this.configDialog = $("<div></div>")
      .addClass("modal fade")
      .attr("tabindex", "-1")
      .attr("role", "dialog")
      .attr("aria-labelledby", "helpModalLabel")
      .attr("aria-hidden", "true");
  
  $("#wrapper").append(this.configDialog);

  var divModalDialog = $("<div></div>")
      .addClass("modal-dialog");
  this.configDialog.append(divModalDialog);

  var divModalContent = $("<div></div>")
      .addClass("modal-content");
  divModalDialog.append(divModalContent);

  var divModalHeader = $("<div></div>")
      .addClass("modal-header");
  divModalContent.append(divModalHeader);

  var btnClose = $('<button/>').addClass("close")
      .attr('type', "button")
      .attr('data-dismiss', "modal");
  divModalHeader.append(btnClose);

  var h4Title = $("<h4/>").addClass("modal-title").text('参数设置');
  divModalHeader.append(h4Title);

  var divModalBody = $("<div/>").addClass("modal-body");
  divModalContent.append(divModalBody);

  // for interval
  if (this.refreshInterval != null) {
    var divInputGroupForInterval = $("<div/>").addClass("input-group");
    divModalBody.append(divInputGroupForInterval);
    divModalBody.append($("<br>"));

    var spanForInterval = $("<span/>").addClass("input-group-addon").text("刷新频率 (单位: 秒)");
    divInputGroupForInterval.append(spanForInterval);

    var txtRefreshInterval = $("<input/>")
        .attr("type", "number")
        .attr("min", 1)
        .attr("max", 30)
        .attr("step", 1)
        .attr("aria-describedby", "basic-addon3")
        .addClass("form-control")
        .val(this.refreshInterval);
    divInputGroupForInterval.append(txtRefreshInterval);
  }

  // for max data count
  if (this.maxDataCount != null) {
    // for max count
    var divInputGroupForMaxCount = $("<div/>").addClass("input-group");
    divModalBody.append(divInputGroupForMaxCount);

    var spanForMaxCount = $("<span/>").addClass("input-group-addon").text("最多显示数据数量");
    divInputGroupForMaxCount.append(spanForMaxCount);

    var txtMaxCount = $("<input/>")
        .attr("type", "number")
        .attr("min", 20)
        .attr("max", 300)
        .attr("step", 5)
        .attr("aria-describedby", "basic-addon3")
        .addClass("form-control")
        .val(this.maxDataCount);
    divInputGroupForMaxCount.append(txtMaxCount);
  }

  var divModalFooter = $("<div/>").addClass("modal-footer");
  divModalContent.append(divModalFooter);

  var btnFooterCancel = $('<button/>').addClass("btn btn-warning")
      .attr('type', "button")
      .attr("data-dismiss", "modal")
      .text("取消");
  divModalFooter.append(btnFooterCancel);

  var btnFooterSave = $('<button/>').addClass("btn btn-success")
      .attr('type', "button")
      .attr("data-dismiss", "modal")
      .text("保存");
  divModalFooter.append(btnFooterSave);

  //this.controlElements.pauseResumeLink.on("click", $.proxy(this.onPauseResume, this));

  //btnFooterSave.click(function(){
  //  var updatedConfigs = {};
  //
  //  if (currentRefreshInterval != null) {
  //    updatedConfigs['refreshInterval'] = txtRefreshInterval.val();
  //  }
  //
  //  if (maxDataCount != null) {
  //    updatedConfigs['maxDataCount'] = txtMaxCount.val();
  //  }
  //
  //  callbackFunction(updatedConfigs);
  //});

  this.configDialog.modal();
};


LepvChart.prototype.SetEvent = function(){
  this.controlElements.pauseResumeLink.onclick = this.ClickEvent.bind(this);
};

LepvChart.prototype.ClickEvent = function(){
  console.log(this.foo); // logs undefined because 'this' is really 'this.bar'
};

LepvChart.prototype.initializeControlElements = function() {
  if (this.chartDiv == null) {
    return;
  }

  this.createControlElements();
  
  // bind click events
  // IMPORTANT:  $.proxy() is the way to get the event bind work here
  this.controlElements.pauseResumeLink.on("click", $.proxy(this.onPauseResume, this));

  this.controlElements.configLink.on("click", $.proxy(this.onConfig, this));
  //controlElements.configLink.click(function(){
  //  onConfig(chartTitle + " Configuration",
  //      updateConfigs,
  //      refreshInterval,
  //      maxDataCount);
  //});
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


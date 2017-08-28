/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvChartConfig = function(callback, thisContainer) {
    
    this.thisContainer = thisContainer;
    this.configDialog = null;
    this.configContainerDiv = null;
    this.refreshIntervalTxt = null;
    this.maxDataCountTxt = null;
    
    this.cancelButton = null;
    this.saveButton = null;
    
    this.createBasicElements();
};

LepvChartConfig.prototype.show = function(currentConfigData) {

    this.displayRefreshIntervalConfig(currentConfigData['refreshInterval']);
    this.displayMaxDataCountConfig(currentConfigData['maxDataCount']);

    this.configDialog.modal();
};

LepvChartConfig.prototype.save = function() {

    var updatedConfig = {};
    updatedConfig['refreshInterval'] = this.refreshIntervalTxt.val();
    updatedConfig['maxDataCount'] = this.maxDataCountTxt.val();

    this.thisContainer.updateConfigs(updatedConfig);
};

LepvChartConfig.prototype.displayMaxDataCountConfig = function(currentMaxCount) {
    if (this.maxDataCountTxt == null) {
        this.createMaxDataCountConfigElements();
    }

    this.maxDataCountTxt.val(currentMaxCount);
    this.maxDataCountTxt.text(currentMaxCount);
};

LepvChartConfig.prototype.createBasicElements = function() {
    
    if (this.configDialog != null) {
        return;
    }

    this.configDialog = $("<div></div>").addClass("modal fade")
        .attr("tabindex", "-1")
        .attr("role", "dialog")
        .attr("aria-labelledby", "helpModalLabel")
        .attr("aria-hidden", "true");

    $("#wrapper").append(this.configDialog);

    var divModalDialog = $("<div></div>").addClass("modal-dialog");
    this.configDialog.append(divModalDialog);

    var divModalContent = $("<div></div>").addClass("modal-content");
    divModalDialog.append(divModalContent);

    var divModalHeader = $("<div></div>").addClass("modal-header");
    divModalContent.append(divModalHeader);

    var btnClose = $('<button/>').addClass("close").attr('type', "button").attr('data-dismiss', "modal");
    divModalHeader.append(btnClose);

    var h4Title = $("<h4/>").addClass("modal-title").text(this.thisContainer.chartTitle + '参数设置');
    divModalHeader.append(h4Title);

    this.configContainerDiv = $("<div/>").addClass("modal-body");
    divModalContent.append(this.configContainerDiv);

    var divModalFooter = $("<div/>").addClass("modal-footer");
    divModalContent.append(divModalFooter);

    this.cancelButton = $('<button/>').addClass("btn btn-warning")
        .attr('type', "button")
        .attr("data-dismiss", "modal")
        .text("取消");
    divModalFooter.append(this.cancelButton);

    this.saveButton = $('<button/>').addClass("btn btn-success")
        .attr('type', "button")
        .attr("data-dismiss", "modal")
        .text("保存");
    divModalFooter.append(this.saveButton);

    this.saveButton.on("click", $.proxy(this.save, this));
};

LepvChartConfig.prototype.createRefreshIntervalConfigElements = function() {

    if (this.refreshInterval != null) {
    return;
    }
    
    var divInputGroupForInterval = $("<div/>").addClass("input-group");
    this.configContainerDiv.append(divInputGroupForInterval);
    this.configContainerDiv.append($("<br>"));
    
    var spanForInterval = $("<span/>").addClass("input-group-addon").text("刷新频率 (单位: 秒)");
    divInputGroupForInterval.append(spanForInterval);
    
    this.refreshIntervalTxt = $("<input/>")
      .attr("type", "number")
      .attr("min", 1)
      .attr("max", 30)
      .attr("step", 1)
      .attr("aria-describedby", "basic-addon3")
      .addClass("form-control")
      .val("1");
    divInputGroupForInterval.append(this.refreshIntervalTxt);
};

LepvChartConfig.prototype.createMaxDataCountConfigElements = function() {

    if (this.maxDataCount != null) {
    return;
    }
    
    var divInputGroupForMaxCount = $("<div/>").addClass("input-group");
    this.configContainerDiv.append(divInputGroupForMaxCount);
    
    var spanForMaxCount = $("<span/>").addClass("input-group-addon").text("最多显示数据数量");
    divInputGroupForMaxCount.append(spanForMaxCount);
    
    this.maxDataCountTxt = $("<input/>")
      .attr("type", "number")
      .attr("min", 50)
      .attr("max", 500)
      .attr("step", 5)
      .attr("aria-describedby", "basic-addon3")
      .addClass("form-control")
      .val("150");
    divInputGroupForMaxCount.append(this.maxDataCountTxt);
};

LepvChartConfig.prototype.displayRefreshIntervalConfig = function(currentInterval) {
    if (this.refreshIntervalTxt == null) {
    this.createRefreshIntervalConfigElements();
    }
    
    this.refreshIntervalTxt.val(currentInterval);
    this.refreshIntervalTxt.text(currentInterval);
};
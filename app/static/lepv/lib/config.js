/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

function createControlElements(chartElement, headingParentColor) {
    // navigate to the title div
    var panelBodyDiv = chartElement.parent();
    if ( ! panelBodyDiv.hasClass('panel-body')) {
        panelBodyDiv = panelBodyDiv.parent();
    }

    var divHeadingPanel = panelBodyDiv.siblings("div").first();
    if ( ! divHeadingPanel.hasClass('panel-heading')) {
        console.log("Failed to locate panel-heading div, not able to create control elements for " + chartElement.getId());
        return;
    }
    
    // remove all the "a" children of the heading panel
    divHeadingPanel.children('a').remove();

    var divHeadingParentPanel = divHeadingPanel.parent();
    if (headingParentColor != null) {
        var divHeadingParentPanelColorClass = 'panel-' + headingParentColor;
        if (!divHeadingParentPanel.hasClass(divHeadingParentPanelColorClass)) {
            divHeadingParentPanel.addClass(divHeadingParentPanelColorClass);
        }
    }

    var createdElements = {};
    
    //var langPack = eval(Cookies.get('languagePack'));

    //// config button
    var elementConfigLink = $("<a></a>");
    var elementConfigDiv = $("<div></div>")
        .attr("data-toggle", "tooltip")
        .attr("data-placement", "auto bottom")
        .attr("title", '设置');//Cookies.get('languagePack')['Configuration']);

    elementConfigDiv.addClass("pull-right glyphicon glyphicon-cog glyphicon-white");
    elementConfigLink.append(elementConfigDiv);
    divHeadingPanel.append(elementConfigLink);
    createdElements['configLink'] = elementConfigLink;
    createdElements['configDiv'] = elementConfigDiv;

    // pause/resume button
    var elementPauseResumeLink = $("<a></a>");
    var elementPauseResumeDiv = $("<div></div>")
        .attr("data-toggle", "tooltip")
        .attr("data-placement", "auto bottom");
    elementPauseResumeDiv.addClass("pull-right glyphicon glyphicon-white");

    elementPauseResumeDiv.addClass("glyphicon-pause");
    elementPauseResumeDiv.attr("title", "点击可暂停刷新");

    elementPauseResumeLink.append(elementPauseResumeDiv);
    divHeadingPanel.append(elementPauseResumeLink);
    createdElements['pauseResumeLink'] = elementPauseResumeLink;
    createdElements['pauseResumeDiv'] = elementPauseResumeDiv;
    createdElements['headingParentDiv'] = divHeadingParentPanel;

    return createdElements;
}

function createDivWithClass(classes) {
    var newDiv = $("<div></div>");
    newDiv.addClass(classes);
    
    return newDiv;
}

function onConfig(title, callbackFunction, currentRefreshInterval, maxDataCount) {
    var divModal = createDivWithClass("modal fade")
        .attr("tabindex", "-1")
        .attr("role", "dialog")
        .attr("aria-labelledby", "helpModalLabel")
        .attr("aria-hidden", "true");
    $("#wrapper").append(divModal);

    var divModalDialog = createDivWithClass("modal-dialog");
    divModal.append(divModalDialog);

    var divModalContent = createDivWithClass("modal-content");
    divModalDialog.append(divModalContent);
    
    var divModalHeader = createDivWithClass("modal-header");
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
    if (currentRefreshInterval != null) {
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
            .val(currentRefreshInterval);
        divInputGroupForInterval.append(txtRefreshInterval);
    }
    
    // for max data count
    if (maxDataCount != null) {
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
            .val(maxDataCount);
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

    btnFooterSave.click(function(){
        var updatedConfigs = {};

        if (currentRefreshInterval != null) {
            updatedConfigs['refreshInterval'] = txtRefreshInterval.val();
        }
        
        if (maxDataCount != null) {
            updatedConfigs['maxDataCount'] = txtMaxCount.val();
        }

        callbackFunction(updatedConfigs);
    });
  
    divModal.modal();
}

function onPauseOrResume(element, isCurrentlyPaused, headingParentDiv, activeColor) {

    if (isCurrentlyPaused) {
        element.removeClass("glyphicon-play");
        element.addClass("glyphicon-pause");

        element.tooltip('hide').attr("data-original-title", "点击可暂停刷新");
        
    } else {
        element.removeClass("glyphicon-pause");
        element.addClass("glyphicon-play");

        element.tooltip('hide').attr("data-original-title", "点击以继续刷新");
    }

    isCurrentlyPaused = !isCurrentlyPaused;

    var divHeadingParentPanelColorClass = 'panel-' + activeColor;
    if (isCurrentlyPaused) {
        headingParentDiv.removeClass(divHeadingParentPanelColorClass);
        headingParentDiv.addClass('panel-grey');
    } else {
        headingParentDiv.removeClass('panel-grey');
        headingParentDiv.addClass(divHeadingParentPanelColorClass);
    }

    return isCurrentlyPaused;
}

function setPauseOrResumeElementStatus(element, isPaused, headerParentDiv, chartHeaderColor) {

    if (isPaused) {
        element.removeClass("glyphicon-pause");
        element.addClass("glyphicon-play");

        element.tooltip('hide').attr("data-original-title", "点击以继续刷新");

        headerParentDiv.removeClass('panel-' + chartHeaderColor);
        headerParentDiv.addClass('panel-grey');
        
    } else {
        element.removeClass("glyphicon-play");
        element.addClass("glyphicon-pause");

        element.tooltip('hide').attr("data-original-title", "点击可暂停刷新");

        headerParentDiv.removeClass('panel-grey');
        headerParentDiv.addClass('panel-' + chartHeaderColor);
    }
}

function showConfigPage() {
    $('#divSettings').on('show.bs.modal', function () {
        $('#divPingResult').empty();
    })

    $('#divSettings').on('hidden.bs.modal', function () {
        startWatching();
    });

    $('#divSettings').modal();
}


function onPingButtonClicked(callbackFunctor) {
    var server = $("#txtServer").val();

    $('#divPingResult').empty();

    $.get("/ping/" + server).done(
        function(data, status) {
            if (data['connected']) {
                var resultButton = $("<button></button>").text("Connection succeeded!").addClass("btn btn-success");
                $('#divPingResult').append(resultButton);
    
                $('#divSettings').modal('hide');
    
                callbackFunctor(server, data);
    
            } else {
                var resultButton = $("<button></button>").text("Connection failed!").addClass("btn btn-danger");
                $('#divPingResult').append(resultButton);
            }
        }
    ).fail(
        function(data, status) {
            var resultButton = $("<button></button>").text("Connection failed!").addClass("btn btn-danger");
            $('#divPingResult').append(resultButton);
        }
    );

}
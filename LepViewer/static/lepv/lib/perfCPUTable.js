/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var PerfCPUTable = (function(){
    
    var chartDivName;
    var cpuTopTableDivName;
    var chartTitle = "Perf Table";
    var chartHeaderColor = 'blue';

    var controlElements = {};

    var tableElement;
    
    var maxDataCount = 25;
    var refreshInterval = 5; // in second
    var isChartPaused = false;
    var intervalId;

    var server;
    var requestId;
    var responseId = 0;

    function _init() {
        
        initTable();

        intervalId = setInterval(function () {
            refreshTable();
        }, refreshInterval * 1000);

        // create the control elements( config, resume, pause ), and cache them here.
        controlElements = createControlElements($('#' + chartDivName), chartHeaderColor);
        controlElements.pauseResumeLink.click(function(){
            isChartPaused = onPauseOrResume(controlElements.pauseResumeDiv, isChartPaused, controlElements.headingParentDiv, chartHeaderColor);
        });
        controlElements.configLink.click(function(){
            onConfig(chartTitle + " Configuration",
                updateConfigs,
                refreshInterval, 
                maxDataCount);
        });
    }

    function updateConfigs(newConfigs) {

        maxDataCount = newConfigs.maxDataCount;

        var refreshFlushInterval = newConfigs.refreshInterval;
        if (refreshFlushInterval != refreshInterval) {
            refreshInterval = newConfigs.refreshInterval;

            clearInterval(intervalId);

            intervalId = setInterval(function () {
                refreshTable();
            }, refreshInterval * 1000);
        }
    }

    function initTable() {
        tableElement = $(cpuTopTableDivName).DataTable( {
            destroy: true,
            paging: false,
            info: false,
            searching: true,
            columns: [
                { 
                    title: "Command",
                    orderable: false
                },
                { 
                    title: "Overhead",
                    orderable: false 
                },
                { 
                    title: "Shared Object",
                    orderable: false
                },
                { 
                    title: "Symbol",
                    orderable: false
                }
            ],
            order: [[ 1, "desc" ]],
        });

        refreshTable();
    }
    
    function refreshTable() {

        if (isChartPaused) {
            return;
        }

        if (requestId - responseId >= 2) {
            console.log("Perf CPU Chart request busy!");
            return;
        }

        $.get("/perfcpu/" + server, function(newData, status){

            if (isChartPaused) {
                return;
            }

            //console.log('perf CPU data count returned: ' + newData.result.length);
            
            tableElement.rows().remove().draw( true );
            var index = 0;

            if (newData != null) {
                $.each( newData['result'], function( index, lineValues ) {

                    if (isChartPaused) {
                        return;
                    }

                    if (index >= maxDataCount) {
                        return;
                    }

                    tableElement.row.add([
                        lineValues['Command'],
                        lineValues['Overhead'],
                        lineValues['Shared Object'],
                        lineValues['Symbol']
                    ]);
                    index = index + 1;
                });
            } else {
                while(index < maxDataCount) {
                    tableElement.row.add([
                        "--",
                        "--",
                        "--",
                        "--"
                    ]);
                    index = index + 1;
                }
            }
            tableElement.draw(true);
        });
    }

    function setDivName(divName) {
        chartDivName = divName;
    }
    function setTableDivName(divName) {
        cpuTopTableDivName = divName;
    }

    function start(serverToMonitor) {

        if (serverToMonitor == server) {
            return;
        }

        server = serverToMonitor;
        requestId = 0;
        responseId = 0;

        _init();
        refreshTable();
    }

    return {
        setChartDivName: setDivName,
        setTableName:setTableDivName,
        start: start
    };

})();
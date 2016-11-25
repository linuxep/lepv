/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CPUTopTable = (function(){
    
    var chartDivName;
    var cpuTopTableDivName;
    var chartTitle = "CPU Top Table";
    var chartHeaderColor = 'orange';

    var controlElements = {};

    var cpuTopTable;
    
    var maxDataCount = 25;
    var refreshInterval = 5; // in second
    var isChartPaused = false;
    var intervalId;

    var server;
    var requestId;
    var responseId = 0;

    function _init() {
        
        initCpuTopTable();

        intervalId = setInterval(function () {
            refreshCpuTopTable();
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

        var updatedFlushInterval = newConfigs.flushInterval;
        if (updatedFlushInterval != refreshInterval) {
            refreshInterval = newConfigs.flushInterval;

            clearInterval(intervalId);

            intervalId = setInterval(function () {
                refreshCpuTopTable();
            }, refreshInterval * 1000);
        }
    }

    function initCpuTopTable() {
        cpuTopTable = $(cpuTopTableDivName).DataTable( {
            destroy: true,
            paging: false,
            info: false,
            searching: true,
            columns: [
                { 
                    title: "PID",
                    orderable: false
                },
                { 
                    title: "User",
                    orderable: false 
                },
                { 
                    title: "PRI",
                    orderable: false
                },
                { 
                    title: "NI",
                    orderable: false
                },
                { 
                    title: "VSZ",
                    orderable: false
                },
                { 
                    title: "RSS",
                    orderable: false
                },
                { 
                    title: "S",
                    orderable: false
                },
                { 
                    title: "%CPU"
                },
                { 
                    title: "%MEM",
                    orderable: false
                },
                { 
                    title: "Time",
                    orderable: false
                },
                { 
                    title: "Command",
                    orderable: false
                }
            ],
            order: [[ 7, "desc" ]],
        });

        refreshCpuTopTable();
    }
    
    function refreshCpuTopTable() {

        if (isChartPaused) {
            return;
        }

        if (requestId - responseId >= 2) {
            //console.log("CPU Top Table request busy!");
            return;
        }

        requestId += 1;
        var ajaxTime= new Date().getTime();
        $.get("/cputop/" + server + "/" + requestId, function(data, status){

            if (isChartPaused) {
                return;
            }

            var currentTime = new Date().getTime();
            var totalTime = (currentTime - ajaxTime) / 1000;
            responseId = data['requestId'];

            cpuTopTable.rows().remove().draw( true );
            var index = 0;

            if (data != null) {
                $.each( data, function( processId, processData ) {

                    if (index >= maxDataCount) {
                        return;
                    }

                    cpuTopTable.row.add([
                        processId,
                        processData['user'],
                        processData['pri'],
                        processData['ni'],
                        processData['vsz'],
                        processData['rss'],
                        processData['s'],
                        processData['cpu'],
                        processData['mem'],
                        processData['time'],
                        processData['command']
                    ]);
                    index = index + 1;
                });
            } else {
                while(index < maxDataCount) {
                    cpuTopTable.row.add([
                        "--",
                        "--",
                        "--",
                        "--",
                        "--",
                        "--",
                        "--",
                        "--",
                        "--",
                        "--",
                        "--"
                    ]);
                    index = index + 1;
                }
            }
            cpuTopTable.draw(true);
        });
    }

    function setDivName(divName) {
        chartDivName = divName;
    }
    function setCputTopTableName(divName) {
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

        refreshCpuTopTable();
    }
    
    return {
        setChartDivName: setDivName,
        setTableName:setCputTopTableName,
        start: start
    };

})();
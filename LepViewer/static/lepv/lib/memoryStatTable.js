/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var MemoryStatTable = (function(){
    
    var tableDivName;
    var memoryStatTableDivName;
    var chartHeaderColor = 'green';

    var memoryStatTable;
    
    var memoryPssChartDivName;
    var memoryPssChart;

    var memoryFreeVsPssChartDivName;
    var memoryFreeVsPssChart;
    
    var totalMemorySize;

    // any process with pss value less than pssBenchmarkValue will not be shown.
    var pssBenchmarkValue = 200;

    var controlElements = {};
    var maxDataCount = 25;
    var refreshInterval = 5; // in second
    var isChartPaused = false;
    var intervalId;
    
    var server;
    var requestId;
    var responseId = 0;
    
    function init() {
        
        intializeCharts();
    }
    
    function intializeCharts() {
        initMemoryStatTable();
        initMemoryPssPieChart();
        initMemoryFreeVsPssPieChart();
    }

    function initMemoryStatTable() {
        memoryStatTable = $('#' + memoryStatTableDivName).DataTable( {
            destroy: true,
            paging: false,
            info: false,
            searching: true,
            columns: [
                { title: "PID", orderable: false },
                { title: "Vss", orderable: false },
                { title: "Rss", orderable: false },
                { title: "Pss", orderable: true },
                { title: "Uss", orderable: false },
                { title: "cmdline", orderable: false }
            ],
            order: [[ 4, "desc" ]]
        });

        memoryStatTable.
            on('mouseover', 'th', function() {
                //console.log("th mouse over");
                //console.log(this.textContent);
                //if (this.textContent == "USS") {
                //    this.attributes["title"] = 'bbbbb';
                //}
                //
                //this.tooltip('hide').attr("data-original-title", "Click to pause it.");
                //this.attributes["title"] = 'cccccc';

            }).
            on('mouseout', 'th', function() {
                //console.log("out");
                //jQuery(this).find('span:first').hide();
            });

        createAndConfigControlElements(tableDivName, 'Memory Consumption Table Configuration');
        refreshMemoryStatTable(null);
    }

    function initMemoryPssPieChart() {

        var memoryPssColumns = [];
        memoryPssChart = c3.generate({
            bindto: '#' + memoryPssChartDivName,
            data: {
                columns: memoryPssColumns,
                type : 'donut'
            },
            donut: {
                title: "PSS"
            },
            legend: {
                show: true,
                position: 'right'
            }
        });

        createAndConfigControlElements(memoryPssChartDivName, 'Memory PSS Pie Chart Configuration');
    }
    
    function createAndConfigControlElements(chartDivName, configDialogTitle) {
        controlElements[chartDivName] = {};

        var targetDivName = chartDivName;
        if (targetDivName.indexOf('#') != 0) {
            targetDivName = '#' + targetDivName;
        }
        controlElements[chartDivName] = createControlElements($(targetDivName), chartHeaderColor);

        controlElements[chartDivName].pauseResumeLink.click(function(){
            isChartPaused = onPauseOrResume(
                controlElements[chartDivName].pauseResumeDiv,
                isChartPaused,
                controlElements[chartDivName].headingParentDiv, 
                chartHeaderColor
            );

            syncupResumePauseElementStatus()
        });

        controlElements[chartDivName].configLink.click(function(){
            onConfig(configDialogTitle,
                updateConfigs,
                refreshInterval,
                maxDataCount);
        });
    }

    function syncupResumePauseElementStatus() {

        setPauseOrResumeElementStatus(controlElements[memoryPssChartDivName].pauseResumeDiv, 
            isChartPaused, 
            controlElements[memoryPssChartDivName].headingParentDiv, 
            chartHeaderColor);
        
        setPauseOrResumeElementStatus(controlElements[memoryFreeVsPssChartDivName].pauseResumeDiv, 
            isChartPaused, 
            controlElements[memoryFreeVsPssChartDivName].headingParentDiv, 
            chartHeaderColor);

        setPauseOrResumeElementStatus(controlElements[tableDivName].pauseResumeDiv,
            isChartPaused,
            controlElements[tableDivName].headingParentDiv,
            chartHeaderColor);
    }

    function updateConfigs(newConfigs) {

        maxDataCount = newConfigs.maxDataCount;

        var updatedRefreshInterval = newConfigs.refreshInterval;
        if (updatedRefreshInterval != refreshInterval) {
            refreshInterval = newConfigs.refreshInterval;

            clearInterval(intervalId);

            intervalId = setInterval(function () {
                refreshCharts();
            }, refreshInterval * 1000);
        }
    }

    function initMemoryFreeVsPssPieChart() {

        var memoryFreeVsPssColumns = [];
        
        memoryFreeVsPssChart = c3.generate({
            bindto: '#' + memoryFreeVsPssChartDivName,
            data: {
                columns: memoryFreeVsPssColumns,
                type : 'donut'
            },
            donut: {
                title: "PSS vs. Total"
            },
            legend: {
                show: true,
                position: 'bottom'
            }
        });

        createAndConfigControlElements(memoryFreeVsPssChartDivName);
    }
  
    function refreshMemoryStatTable(newData) {
        memoryStatTable.rows().remove().draw( true );

        var index = 0;
        if (newData == null) {
            while(index < maxDataCount) {
                memoryStatTable.row.add([
                    "--",
                    "--",
                    "--",
                    "--",
                    "--",
                    "--"
                ]);
                index = index + 1;
            }
            
        } else {
            $.each( newData, function( lineIndex, processData ) {

                if (index >= maxDataCount) {
                    return;
                }

                memoryStatTable.row.add([
                    processData['pid'],
                    processData['vss'],
                    processData['rss'],
                    processData['pss'],
                    processData['uss'],
                    //Math.round(processData['vss'] * totalMemorySize * 1000) / 1000,
                    //Math.round(processData['rss'] * totalMemorySize * 1000) / 1000,
                    //Math.round(processData['pss'] * totalMemorySize * 1000) / 1000,
                    //Math.round(processData['uss'] * totalMemorySize * 1000) / 1000,
                    processData['cmdline']
                ]);

                index = index + 1;
            });
        }

        memoryStatTable.draw(true);
    }

    function refreshMemoryPssStatChart(newData, sumData) {
        var pssDataColumns = [];

        $.each( newData, function( processId, processData ) {
            if (processData['cmdline'] != null) {
                
                if (processData['pss'] > pssBenchmarkValue ) {
                    pssDataColumns.push([processData['cmdline'], processData['pss']]);
                }
            }
        });

        memoryPssChart.unload();
        memoryPssChart.load({
            columns: pssDataColumns,
            keys: {
                value: ['']
            }
        });
    }

    function _flushMemoryPssVsTotalStatChart(sumData) {
        var dataColumn = [];
        
        // to show the correct % of pss against total in donut chart, we need to to set total as (total - pss)
        dataColumn.push(["Total Memory", sumData['total'] - sumData['pssTotal']]);
        dataColumn.push(["Total PSS", sumData['pssTotal']]);

        memoryFreeVsPssChart.load({
            columns: dataColumn,
            keys: {
                value: ['']
            }
        });
    }

    function setDivName(divName) {
        tableDivName = divName;
    }
    
    function setMemoryStatTableDivName(divName) {
        memoryStatTableDivName = divName;
    }
    
    function setMemoryPssChartDivName(divName) {
        memoryPssChartDivName = divName;
    }

    function setMemoryFreeVsPssChartDivName(divName) {
        memoryFreeVsPssChartDivName = divName;
    }
    
    function refreshCharts() {
        if (isChartPaused) {
            return;
        }

        if (requestId - responseId >= 2) {
            //console.log("Memory Stat Chart request busy!");
            return;
        }

        requestId += 1;
        var ajaxTime= new Date().getTime();
        $.get("/memstat/" + server + "/" + requestId, function(responseData, status){

            var data = responseData['data'];
            var currentTime = new Date().getTime();
            var totalTime = (currentTime - ajaxTime) / 1000;
            responseId = data['requestId'];
            
            if (isChartPaused) {
                return;
            }

            refreshMemoryStatTable(null);
            refreshMemoryStatTable(data);

            refreshMemoryPssStatChart(data, responseData['sum']);
            _flushMemoryPssVsTotalStatChart(responseData['sum']);
        });
    }

    function start(serverToMonitor) {

        if (serverToMonitor == server) {
            return;
        }

        server = serverToMonitor;
        requestId = 0;
        responseId = 0;
        
        totalMemorySize = Cookies.get(server + ".Memory.Total");

        init();

        refreshCharts();

        intervalId = setInterval(function () {
            refreshCharts();
        }, refreshInterval * 1000);
    }
    
    return {
        setChartDivName: setDivName,
        setMemoryStatTableDivName:setMemoryStatTableDivName,
        setMemoryPssChartDivName: setMemoryPssChartDivName,
        setMemoryFreeVsPssChartDivName: setMemoryFreeVsPssChartDivName,
        start: start
    };

})();
/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CPUCharts = (function(){

    var overallStatChartDivName;
    var overallStatChart;
    var chartHeaderColor = 'orange';
    
    var chartDivNameMap = {};

    var chartDivName;
    
    var chartIdle;
    var chartUserGroup;
    var chartIrqGroup;

    var timeData = ['x'];
    
    // we need this variable because we don't know the cores of the CPU in advance.
    var statDatas;

    // all the three charts share the same settings.
    // it makes no sense for them to be different.
    // but there are three sets of control elements on UI
    var controlElements = {};
    var maxDataCount = 150;
    var refreshInterval = 2; // in second
    var isChartPaused = false;
    var intervalId;

    var server;
    var cpuCoreCount = 1;

    function _getAllFieldNames() {
        return [ "user", "nice", "system", "idle", "iowait", "irq", "softirq", "steal", "guest", "guestnice"];
    }

    function initDonutChart() {
        var overallStatColumns = [];

        var fields = _getAllFieldNames();
        $.each( fields, function( i, field ) {
            overallStatColumns.push([field, 0]);
        });
        
        $('#' + overallStatChartDivName).empty();

        overallStatChart = c3.generate({
            bindto: '#' + overallStatChartDivName,
            data: {
                columns: overallStatColumns,
                type : 'donut',
                colors: {
                    idle: "green",
                    user: 'blue',
                    system: 'red',
                    nice: "orange"
                }
            },
            donut: {
                title: "CPU STAT"
            },
            legend: {
                show: true,
                position: 'right'
            }
        });

        controlElements[overallStatChartDivName] = {};
        controlElements[overallStatChartDivName] = createControlElements($('#' + overallStatChartDivName),
            chartHeaderColor);

        controlElements[overallStatChartDivName].pauseResumeLink.click(function(){
            isChartPaused = onPauseOrResume(
                controlElements[overallStatChartDivName].pauseResumeDiv,
                isChartPaused,
                controlElements[overallStatChartDivName].headingParentDiv,
                chartHeaderColor);

            syncupResumePauseElementStatus()
        });

        controlElements[overallStatChartDivName].configLink.click(function(){
            onConfig("CPU Stat Charts Configuration",
                updateConfigs,
                refreshInterval
            );
        });
    }

    function initializeDetailStatChart(chartGroupName) {
        var chartDivName = chartDivNameMap[chartGroupName];

        $('#' + chartDivName).empty();
        
        var chart = c3.generate({
            bindto: '#' + chartDivName,
            data: {
                x: 'x',
                columns: [timeData]
            },
            legend: {
                show: true,
                position: 'bottom',
                inset: {
                    anchor: 'top-right',
                    x: 20,
                    y: 10,
                    step: 2
                }
            },
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: '%H:%M:%S'
                    }
                },
                y: {
                    label: {
                        position: "inner-middle"
                    },
                    min: 0,
                    max: 100,
                    padding: {top:0, bottom:0}
                }
            },
            tooltip: {
                format: {
                    value: function (value, ratio, id) {
                        return value + " %";
                    }
                }
            }
        });

        controlElements[chartDivName] = {};
        controlElements[chartDivName] = createControlElements($('#' + chartDivName), chartHeaderColor);

        controlElements[chartDivName].pauseResumeLink.click(function(){
            isChartPaused = onPauseOrResume(
                controlElements[chartDivName].pauseResumeDiv,
                isChartPaused,
                controlElements[chartDivName].headingParentDiv,
                chartHeaderColor);

            syncupResumePauseElementStatus()
        });

        controlElements[chartDivName].configLink.click(function(){
            onConfig("CPU Stat Charts Configuration",
                updateConfigs,
                refreshInterval,
                maxDataCount 
                );
        });
        
        return chart;
    }
    
    function syncupResumePauseElementStatus() {
        $.each( controlElements, function( chartDivName, controlElementByType ) {
            setPauseOrResumeElementStatus(controlElementByType.pauseResumeDiv, 
                isChartPaused,
                controlElementByType.headingParentDiv,
                chartHeaderColor
            );
        });
    }

    function updateConfigs(newConfigs) {

        maxDataCount = newConfigs.maxDataCount;

        var updatedRefreshInterval = newConfigs.flushInterval;
        if (updatedRefreshInterval != refreshInterval) {
            refreshInterval = newConfigs.refreshInterval;

            clearInterval(intervalId);

            intervalId = setInterval(function () {
                refreshCharts();
            }, refreshInterval * 1000);
        }
    }

    function initDetailStatCharts() {
        if (chartIdle != null) {
            chartIdle.unload();
        }
        chartIdle = initializeDetailStatChart('idle');

        if (chartUserGroup != null) {
            chartUserGroup.unload();
        }
        chartUserGroup = initializeDetailStatChart("userGroup");

        if (chartIrqGroup != null) {
            chartIrqGroup.unload();
        }
        chartIrqGroup = initializeDetailStatChart("irqGroup");

        intervalId = setInterval(function () {
            refreshCharts();
        }, refreshInterval * 1000);
    
    }

    function init() {

        cpuCoreCount = getCpuCoreCount(server);

        statDatas = {};
        timeData = ['x'];
        
        statDatas['idle'] = {};
        statDatas['userGroup'] = {};
        statDatas['irqGroup'] = {};
        
        for ( var i = 0; i < cpuCoreCount; i++) {
            statDatas['idle']['cpu' + i] = ['CPU' + i];
            statDatas['userGroup']['cpu' + i] = ['CPU' + i];
            statDatas['irqGroup']['cpu' + i] = ['CPU' + i];
        }
        
        initDonutChart();
        initDetailStatCharts();
    }
    
    
    function refreshOverallChart(processedData) {
        if (processedData == null ) {
            return;
        }
        
        if (processedData['server'] != server) {
            return;
        }

        var resultData = processedData['data'];
        overallStatChart.load({
            columns: [
                ['user', resultData['all']['user']],
                ['nice', resultData['all']['nice']],
                ['system', resultData['all']['system']],
                ['idle', resultData['all']['idle']],
                ['iowait', resultData['all']['iowait']],
                ['irq', resultData['all']['irq']],
                ['softirq', resultData['all']['soft']],
                ['steal', resultData['all']['steal']],
                ['guest', resultData['all']['guest']],
                ['guestnice', resultData['all']['guest']]
            ],
            keys: {
                value: ['']
            }
        });
    }

    function refreshDetailCharts(processedData) {

        if (processedData['server'] != server) {
            return;
        }

        if (timeData.length > maxDataCount) {
            timeData.splice(1, 1);

            for (var i=0; i < cpuCoreCount; i++) {
                statDatas['idle'][i].splice(1, 1);
                statDatas['userGroup'][i].splice(1, 1);
                statDatas['irqGroup'][i].splice(1, 1);
            }
        }
        
        timeData.push(new Date());
        
        var idleChartData = [timeData];
        var userGroupChartData = [timeData];
        var irqGroupChartData = [timeData];
        
        var coreIndex = 0;
        while(true) {
            var coreName = coreIndex;
            
            var resultData = processedData['data'];
            if (coreName in resultData) {

                if (!(coreName in statDatas['idle'])) {
                    statDatas['idle'][coreName] = ['CPU-' + coreName];
                }
                statDatas['idle'][coreName].push(resultData[coreName]['idle']);

                if (!(coreName in statDatas['userGroup'])) {
                    statDatas['userGroup'][coreName] = ['CPU-' + coreName];
                }

                var userGroupData = (Math.round(resultData[coreName]['user'])) +
                    + (Math.round(resultData[coreName]['system'])
                    + (Math.round(resultData[coreName]['nice'])));
                statDatas['userGroup'][coreName].push(userGroupData);

                if (!(coreName in statDatas['irqGroup'])) {
                    statDatas['irqGroup'][coreName] = ['CPU-' + coreName];
                }
                var irqGroupData = (Math.round(resultData[coreName]['irq'])) +
                    + (Math.round(resultData[coreName]['soft']));
                statDatas['irqGroup'][coreName].push(irqGroupData);

                idleChartData.push(statDatas['idle'][coreIndex]);
                userGroupChartData.push(statDatas['userGroup'][coreIndex]);
                irqGroupChartData.push(statDatas['irqGroup'][coreIndex]);
                
                coreIndex += 1;
            } else {
                break;
            }
        }

        chartIdle.load({
            columns: idleChartData,
            keys: {
                value: ['']
            }
        });

        chartUserGroup.load({
            columns: userGroupChartData,
            keys: {
                value: ['']
            }
        });

        chartIrqGroup.load({
            columns: irqGroupChartData,
            keys: {
                value: ['']
            }
        });
    }
  
    function setOverallDivName(divName) {
        overallStatChartDivName = divName;
    }
    
    function setIdleStatDivName(divName) {
        var shortDivName = divName;
        if(divName.indexOf("#") == 0) {
            shortDivName = shortDivName.substring(1, shortDivName.length);
        }

        chartDivNameMap['idle'] = shortDivName; //document.getElementById(shortDivName);
    }
    
    function setUserStatDivName(divName) {
        var shortDivName = divName;
        if(shortDivName.indexOf("#") == 0) {
            shortDivName = shortDivName.substring(1, shortDivName.length);
        }

        chartDivNameMap['userGroup'] = shortDivName; //chartDivMap['user'];
    }
    
    function setIrqStatDivName(divName) {
        var shortDivName = divName;
        if(shortDivName.indexOf("#") == 0) {
            shortDivName = shortDivName.substring(1, shortDivName.length);
        }

        chartDivNameMap['irqGroup'] = shortDivName; //chartDivMap['irq']
    }

    function setDivName(divName) {
        chartDivName = divName;
    }
    
    function refreshCharts() {

        if (isChartPaused) {
            return;
        }
        
        $.get("/cpustat/" + server, function(data, status){

            if (isChartPaused) {
                return;
            }
            
            refreshOverallChart(data);
            refreshDetailCharts(data);
        });
    }

    function start(serverToMonitor) {

        if (serverToMonitor == server) {
            return;
        }
        
        server = serverToMonitor;
        init();
        refreshCharts();
    }

    return {
        setChartDivName: setDivName,
        setOverallDivName: setOverallDivName,
        setIdleStatDivName: setIdleStatDivName,
        setUserStatDivName: setUserStatDivName,
        setIrqStatDivName: setIrqStatDivName,
        start: start
    };

})();
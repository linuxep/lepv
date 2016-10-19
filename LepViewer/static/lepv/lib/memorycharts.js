/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var MemoryCharts = (function(){
    
    var chartDivName;
    var chartTitle = "RAM Chart";
    var chartHeaderColor = 'green';

    var controlElements = {};

    var timeData;
    var dataFree;
    var dataCached;
    var dataBuffers;
    var dataUsed;
    
    var chart;
    var refreshInterval; // in second
    var maxDataCount;
    var isChartPaused;
    var intervalId;
    
    var memoryTotal;
    
    var server;

    function _init() {

        timeData = ['x'];
        dataFree = ['Free'];
        dataCached = ['Cached'];
        dataBuffers = ['Buffers'];
        dataUsed = ['Used'];

        refreshInterval = 2; // in second
        maxDataCount = 150;
        isChartPaused = false;

        memoryTotal = getMemoryTotal(server);
        chart = c3.generate({
            bindto: '#' + chartDivName,
            data: {
                x: 'x',
                // the order matters: free -> cached -> buffers -> used
                columns: [timeData, dataUsed, dataBuffers, dataCached, dataFree],

                types: {
                    Used: 'area',
                    Buffers: "area",
                    Cached: "area",
                    Free: "area"
                },

                groups: [['Free', 'Cached', 'Buffers', 'Used']],
                order: null,

                colors: {
                    Free: '#2d862d',
                    Cached: "#ffb84d",
                    Buffers: "#4d94ff",
                    Used: "#ff6666"
                }
            },
            point: {
                show: false
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
                    padding: {top:0, bottom:0}
                }
            },
            tooltip: {
                format: {
                    value: function (value, ratio, id) {
                        return value + " MB";
                    }
                }
            }
        });

        intervalId = setInterval(function () {
            refreshChart();
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

        var updatedRefreshInterval = newConfigs.refreshInterval;
        if (updatedRefreshInterval != refreshInterval) {
            refreshInterval = newConfigs.refreshInterval;

            clearInterval(intervalId);

            intervalId = setInterval(function () {
                refreshChart();
            }, refreshInterval * 1000);
        }
    }
    
    function refreshChart() {

        if (isChartPaused) {
            return;
        }
        
        $.get("/status/memory/" + server, function(data, status){

            if (isChartPaused) {
                return;
            }

            if (timeData.length > maxDataCount) {
                timeData.splice(1, 1);
                dataUsed.splice(1, 1);
                dataBuffers.splice(1, 1);
                dataFree.splice(1, 1);
                dataCached.splice(1, 1);
            }
        
            timeData.push(new Date());
            dataUsed.push(data['used']);
            dataBuffers.push(data['buffers']);
            dataFree.push(data['free']);
            dataCached.push(data['cached']);

            chart.load({
                //// the order matters: free -> cached -> buffers -> used
                columns: [timeData, dataUsed, dataBuffers, dataCached, dataFree]
            });
        });
    }
    
    function setDivName(divName) {
        chartDivName = divName;
    }

    function start(serverToMonitor) {

        if (serverToMonitor == server) {
            return;
        }

        server = serverToMonitor;
        _init();
        refreshChart();
    }
    
    return {
        setChartDivName: setDivName,
        start: start
    };

})();
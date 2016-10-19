/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var IOStatCharts = (function(){

    var chartDivName;
    var chart;
    var chartTitle = "I/O Chart";
    var chartHeaderColor = 'yellow';

    var controlElements = {};

    var timeData = ['x'];
    
    var ioDatas = {};

    var maxDataCount = 150;
    var refreshInterval = 2; // in second
    var isChartPaused = false;
    var intervalId;

    var server;
    var requestId;
    var responseId = 0;

    function init() {

        //Sample: http://c3js.org/samples/timeseries.html
        chart = c3.generate({
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
                        text: "KB/S",
                        position: "inner-middle"
                    }
                }
            },
            tooltip: {
                format: {
                    value: function (value, ratio, id) {
                        return value + " kb/s";
                    }
                }
            }
        });

        intervalId = setInterval(function () {
            refreshChart();
        }, refreshInterval * 1000);

        //  create the control elements( config, resume, pause ), and cache them here.
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

        if (requestId - responseId >= 2) {
            console.log("requestId - responseId = " + (requestId - responseId));
            //return;
        }

        requestId += 1;
        var ajaxTime= new Date().getTime();
        var url = "/status/io/" + server + "/" + requestId;
        console.log(url + " ->");
        $.get(url).success(
            function(data) {

                var totalTime = (new Date().getTime()-ajaxTime) / 1000;
                responseId = data['requestId'];
                console.log(url + " <- in " + totalTime + " seconds; with lepd response time as " + data['lepdDuration']);
                if (isChartPaused) {
                    return;
                }

                var diskDatas = data['disks'];
                $.each( diskDatas, function( diskName, diskData ) {
                    if ( !(diskName in ioDatas)) {
                        ioDatas[diskName] = {};

                        ioDatas[diskName]['read'] = [diskName + ' read'];
                        ioDatas[diskName]['write'] = [diskName + ' write'];
                    }

                    if (ioDatas[diskName]['read'].length > maxDataCount ) {
                        timeData.splice(1, 1);

                        ioDatas[diskName]['read'].splice(1, 1);
                        ioDatas[diskName]['write'].splice(1, 1);
                    }

                    ioDatas[diskName]['read'].push(data['disks'][diskName]['rkbs']);
                    ioDatas[diskName]['write'].push(data['disks'][diskName]['wkbs']);

                });

                timeData.push(new Date());
                var columnDataToDisplay = [timeData];
                $.each( ioDatas, function( diskName, diskData ) {
                    columnDataToDisplay.push(ioDatas[diskName]['read']);
                    columnDataToDisplay.push(ioDatas[diskName]['write']);
                });

                chart.load({
                    columns: columnDataToDisplay,
                    keys: {
                        value: ['']
                    }
                });
            }
        ).error(
            function(jqXHR, textStatus, errorThrown) {
                console.log(textStatus + "; " + jqXHR.status + " " + errorThrown);
            }
        );
    }

    function setDivName(divName) {
        chartDivName = divName;
    }

    function start(serverToMonitor) {

        if (serverToMonitor == server) {
            return;
        }
        
        server = serverToMonitor;
        requestId = 0;
        responseId = 0;
        init();
        refreshChart();
    }

    return {
        setChartDivName: setDivName,
        start: start
    };

})();

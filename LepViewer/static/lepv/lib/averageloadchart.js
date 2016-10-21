/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var AverageLoadChart = (function(){

    var chartDivName;
    var chart;
    var chartTitle = "Average Load Chart";
    var chartHeaderColor = 'orange';

    var controlElements = {};
    
    var timeData;
    var dataLast1;
    var dataLast5;
    var dataLast15;
    var maxValues;

    var defaultMaxYValue;

    var yellowAlertValue;
    var redAlertValue;

    var maxDataCount;
    var refreshInterval; // in second
    var isChartPaused;
    var intervalId;

    var server;

    function _init() {

        timeData = ['x'];
        dataLast1 = ['Last minute'];
        dataLast5 = ['Last 5 minutes'];
        dataLast15 = ['Last 15 minutes'];
        maxValues = [];

        maxDataCount = 150;
        refreshInterval = 2; // in second
        isChartPaused = false;

        var cpuCoreCount = Cookies.get(server + ".Core.Count");

        yellowAlertValue = 0.7 * cpuCoreCount;
        redAlertValue = 0.9 * cpuCoreCount;

        defaultMaxYValue = 1 * cpuCoreCount;
        maxValues.push(defaultMaxYValue);

        chart = c3.generate({
            bindto: '#' + chartDivName,
            data: {
                x: 'x',
                columns: [timeData, dataLast1, dataLast5, dataLast15]

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
                    max: defaultMaxYValue,
                    padding: {top:0, bottom:0}
                }
            },
            tooltip: {
                format: {
                    value: function (value, ratio, id) {
                        return value;
                    }
                }
            }
        });

        intervalId = setInterval(function () {
            _flushChart();
        }, refreshInterval * 1000);

        // create the control elements( config, resume, pause ), and cache them here.
        controlElements = createControlElements($('#' + chartDivName), chartHeaderColor);

        controlElements.pauseResumeLink.click(function(){
            isChartPaused = onPauseOrResume(controlElements.pauseResumeDiv, 
                isChartPaused, 
                controlElements.headingParentDiv, 
                chartHeaderColor);
        });

        controlElements.configLink.click(function(){
            onConfig(chartTitle + " Configurations", updateConfigs, refreshInterval, maxDataCount);
        });
    }

    function updateConfigs(newConfigs) {

        maxDataCount = newConfigs.maxDataCount;

        var updatedFlushInterval = newConfigs.flushInterval;
        if (updatedFlushInterval != refreshInterval) {
            refreshInterval = newConfigs.flushInterval;

            clearInterval(intervalId);

            intervalId = setInterval(function () {
                _flushChart();
            }, refreshInterval * 1000);
        }
    }

    function _flushChart() {

        if (isChartPaused) {
            return;
        }

        var ajaxTime= new Date().getTime();
        $.get("/status/avgload/" + server, function(data, status){

            if (isChartPaused) {
                return;
            }
            
            if (dataLast1.length > maxDataCount) {
                timeData.splice(1, 1);
                dataLast1.splice(1, 1);
                dataLast5.splice(1, 1);
                dataLast15.splice(1, 1);
                maxValues.splice(1,1);
            }

            timeData.push(new Date());
            dataLast1.push(data['last1']);
            dataLast5.push(data['last5']);
            dataLast15.push(data['last15']);
            
            // max values are the max values of each group of data, it determines the max of y axis.
            maxValues.push(Math.max.apply(Math,[data['last1'], data['last5'], data['last15']]));

            // TODO: need to refactor the way to get the max value of current data currently shown on chart.

            var cpuCoreCount = Cookies.get(server + ".Core.Count");

            yellowAlertValue = 0.7 * cpuCoreCount;
            redAlertValue = 0.9 * cpuCoreCount;

            defaultMaxYValue = 1 * cpuCoreCount;
            maxValues[0] = defaultMaxYValue;

            chart.axis.max(Math.max.apply(Math, maxValues) + 0.1);
            chart.load({
                columns: [timeData, dataLast1, dataLast5, dataLast15],
                keys: {
                    value: ['']
                }
            });
        });
    }

    function setDivName(divName) {
        chartDivName = divName;
    }

    function start(serverToMonitor) {

        if (server == serverToMonitor) {
            return;
        }
        
        server = serverToMonitor;

        _init();

        _flushChart();
    }

    return {
        setChartDivName: setDivName,
        start: start
    };

})();
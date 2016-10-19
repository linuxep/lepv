/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var GaugeCharts = (function(){
    
    var chartDivName;
    
    var chartDivNameMap = {};
    var chartsMap = {};
    
    var refreshInterval = 2; // in second
    
    var server;

    function _init() {
        
        $.each( chartDivNameMap, function( component, divName ) {

            chartsMap[component] = c3.generate({
                                        bindto: chartDivNameMap[component],
                                        data: {
                                            columns: [
                                            ],
                                            type: 'gauge'
                                        },
                                        gauge: {
                                            label: {
                                                format: function(value, ratio) {
                                                    return value + "%";
                                                },
                                                show: true // to turn off the min/max labels.
                                            },
                                            min: 0, // 0 is default, //can handle negative min e.g. vacuum / voltage / current flow / rate of change
                                            max: 100, // 100 is default
                                            width: 30 // for adjusting arc thickness
                                        },
                                        color: {
                                            pattern: ['#60B044', '#F6C600', '#F97600', '#FF0000'], // the three color levels for the percentage values.
                                            threshold: {
                                                values: [30, 60, 90, 100]
                                            }
                                        },
                                        size: {
                                            height: 100
                                        }
                                    });

        });
    }
    
    
    
    function refreshData(chartToRefresh, newData) {

        chartToRefresh.load({
            json: [
                newData
            ],
            keys: {
                value: ['ratio']
            }
        });
    }
    
    function setDivName(divName) {
        chartDivName = divName;
        if(divName.indexOf("#") != 0) {
            chartDivName = divName.substring(1, divName.length);
        }
    }
    
    function setRefreshInterval(intervalInSeconds) {
        refreshInterval = intervalInSeconds;
    }
    
    function _prefixDivName(divName) {
        if(divName.indexOf("#") == 0) {
            return divName;
        } else {
            return '#' + divName;
        }
    }

    function setComponentDivName(component, divName) {
        chartDivNameMap[component.toLowerCase()] = _prefixDivName(divName);
    }

    function getDataAndFlush() {
        $.each( chartsMap, function( component, chart ) {
            var url = "/status/" + component + "/" + server;
            $.get(url, function(data, status){
                refreshData(chart, data);
            });
        });
    }

    function start(serverToMonitor) {

        if (serverToMonitor == server) {
            return;
        }
         
        server = serverToMonitor;

        _init();

        getDataAndFlush();

        setInterval(function () {
            getDataAndFlush();
        }, refreshInterval * 1000);
    }

    return {
        setChartDivName: setDivName,
        setComponentDivName: setComponentDivName,
        
        start: start
    };

})();
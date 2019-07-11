/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var IOStatChart = function(rootDivName, socket, server) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'io.status';

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};
    
    this.chartTitle = "IO Stat Chart";
    this.chartHeaderColor = 'yellow';

    this.maxDataCount = 150;
    this.refreshInterval = 3;

    // this.updateChartHeader();
    this.initializeChart();

    this.setupSocketIO();
};

IOStatChart.prototype = Object.create(LepvChart.prototype);
IOStatChart.prototype.constructor = IOStatChart;

IOStatChart.prototype.initializeChart = function() {
    
    this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            x: 'x',
            columns: [['x'], ['read'], ['write']]
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
                    position: "outter-middle"
                },
                padding: {
                    top:10,
                    bottom:10
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
};

IOStatChart.prototype.updateChartData = function(response) {
    var data = response['data'];
    if (!data && typeof(data)!='undefined' && data!=0) {
        return
    }
    if (typeof(data) == "undefined"){ 
        return
    }
    console.log(data)
    var diskDatas = data['disks'];
    // console.log(diskDatas)
    
    var thisChart = this;
    $.each(diskDatas, function( diskName, diskData ) {
        if ( !(diskName in thisChart.chartData)) {
            thisChart.chartData[diskName] = {};

            thisChart.chartData[diskName]['read'] = [diskName + ' read'];
            thisChart.chartData[diskName]['write'] = [diskName + ' write'];
        }

        if (thisChart.chartData[diskName]['read'].length > thisChart.maxDataCount ) {
            thisChart.timeData.splice(1, 1);

            thisChart.chartData[diskName]['read'].splice(1, 1);
            thisChart.chartData[diskName]['write'].splice(1, 1);
        }

        thisChart.chartData[diskName]['read'].push(diskData['rkbs']);
        thisChart.chartData[diskName]['write'].push(diskData['wkbs']);

    });

    thisChart.timeData.push(new Date());
    var columnDataToDisplay = [thisChart.timeData];
    $.each( thisChart.chartData, function( diskName, diskData ) {
        columnDataToDisplay.push(diskData['read']);
        columnDataToDisplay.push(diskData['write']);
    });

    this.chart.load({
        columns: columnDataToDisplay,
        keys: {
            value: ['']
        }
    });

    // this.requestData();
};

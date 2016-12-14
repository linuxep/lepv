/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvIOChart = function(divName) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    console.log("I'm initialized in LepvIO");
    
    this.maxDataCount = 500;
    this.refreshInterval = 10;
    this.chartHeaderColor = 'yellow';

    this.dataUrlPrefix = "/status/io/";

    this.updateChartHeader();
    this.initializeChart();
};

LepvIOChart.prototype = Object.create(LepvChart.prototype);
LepvIOChart.prototype.constructor = LepvIOChart;

LepvIOChart.prototype.initializeChart = function() {
    
    console.log("chart initialized in lepvIO");
    console.log(this.isChartPaused);
    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
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

    console.log("IO chart initialization done.");
};

LepvIOChart.prototype.reloadChartData = function(data) {
    
    console.log("data reloaded in LepvIOChart");

};

LepvIOChart.prototype.updateChartData = function(data) {
    var diskDatas = data['disks'];
    
    var thisChart = this;
    $.each( diskDatas, function( diskName, diskData ) {
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

        thisChart.chartData[diskName]['read'].push(data['disks'][diskName]['rkbs']);
        thisChart.chartData[diskName]['write'].push(data['disks'][diskName]['wkbs']);

    });

    thisChart.timeData.push(new Date());
    var columnDataToDisplay = [thisChart.timeData];
    $.each( thisChart.chartData, function( diskName, diskData ) {
        columnDataToDisplay.push(thisChart.chartData[diskName]['read']);
        columnDataToDisplay.push(thisChart.chartData[diskName]['write']);
    });

    this.chart.load({
        columns: columnDataToDisplay,
        keys: {
            value: ['']
        }
    });
};

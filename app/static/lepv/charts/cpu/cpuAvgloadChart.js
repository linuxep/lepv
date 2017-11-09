/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuAvgLoadChart = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.socket_message_key = 'cpu.avgload';
    
    this.chartTitle = "Average Load Chart";
    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;

    this.chart = null;
    this.chartData['last1'] = ['Last minute'];
    this.chartData['last5'] = ['Last 5 minutes'];
    this.chartData['last15'] = ['Last 15 minutes'];

    this.cpuCoreCount = 0;
    this.yellowAlertValue = 0.7;
    this.redAlertValue = 0.9;
    
    this.defaultMaxValue = 1;
    this.maxValues = [1];

    this.initializeChart();
    this.setupSocketIO();
};

CpuAvgLoadChart.prototype = Object.create(LepvChart.prototype);
CpuAvgLoadChart.prototype.constructor = CpuAvgLoadChart;

CpuAvgLoadChart.prototype.initializeChart = function() {

    var thisChart = this;

    thisChart.socketIO.on("cpu.count.res", function(response) {
        console.log("  <- " + thisChart.socket_message_key + ".res(" + response['response_id'] + ")");
        console.log(response)
        // responseData = response['data']
        this.cpuCoreCount = response['count'];
    });
    thisChart.socketIO.emit("cpu.count.req", {'server': thisChart.serverToWatch, "request_id": thisChart.socket_request_id});

    console.log(thisChart.cpuCoreCount)
    while (thisChart.cpuCoreCount == 0){
        var t = Date.now();
        while(Date.now - t <= d); 
    }
    // console.log(thisChart.cpuCoreCount)
 
    thisChart.yellowAlertValue = 0.7 * thisChart.cpuCoreCount;
    thisChart.redAlertValue = 0.9 * thisChart.cpuCoreCount;

    thisChart.maxValues = [thisChart.cpuCoreCount];

    thisChart.chart = c3.generate({
        bindto: '#' + thisChart.chartDivName,
        data: {
            x: 'x',
            columns: [thisChart.timeData,
                thisChart.chartData['last1'],
                thisChart.chartData['last5'],
                thisChart.chartData['last15']]

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
                max: thisChart.cpuCoreCount,
                padding: {
                    top:10,
                    bottom:10
                }
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

};

CpuAvgLoadChart.prototype.updateChartData = function(responseData) {
    data = responseData['data'];
    // console.log(data);
    if (this.chart == null) {
        return;
    }

    if (this.chartData['last1'].length > this.maxDataCount) {
        this.timeData.splice(1, 1);
        this.chartData['last1'].splice(1, 1);
        this.chartData['last1'].splice(1, 1);
        this.chartData['last1'].splice(1, 1);
        this.maxValues.splice(1,1);
    }

    this.timeData.push(new Date());
    this.chartData['last1'].push(data['last1']);
    this.chartData['last5'].push(data['last5']);
    this.chartData['last15'].push(data['last15']);

    // max values are the max values of each group of data, it determines the max of y axis.
    this.maxValues.push(Math.max.apply(Math,[data['last1'], data['last5'], data['last15'], this.cpuCoreCount]));

    this.chart.axis.max(Math.max.apply(Math, this.maxValues) + 0.1);
    this.chart.load({
        columns: [this.timeData,
            this.chartData['last1'],
            this.chartData['last5'],
            this.chartData['last15']],
        keys: {
            value: ['']
        }
    });
    this.requestData();
};

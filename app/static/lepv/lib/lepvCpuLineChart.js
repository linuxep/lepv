/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var LepvCpuLineChart = function(divName, chartTitle) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, divName);
    
    this.chartTitle = chartTitle;
    this.chartHeaderColor = 'orange';
    
    this.proactive = false;
    
    this.maxDataCount = 150;
    this.refreshInterval = 2;
    this.timeData = ['x'];

    this.panelFooter = this.controlElements['panelFooter'];
    this.loadBalanceWatcher = {
        "balanced": true,
        "count": 0
    };  // true or false, where true for load balance, and false for NOT balance

    this.loadBalanceLimit = 10;
    this.UnBalanceHappened = false;
    
    this.updateChartHeader();
    this.initialize();
};

LepvCpuLineChart.prototype = Object.create(LepvChart.prototype);
LepvCpuLineChart.prototype.constructor = LepvCpuLineChart;

LepvCpuLineChart.prototype.initialize = function() {
    
    this.chart = c3.generate({
        bindto: '#' + this.chartDivName,
        data: {
            x: 'x',
            columns: [this.timeData]
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
                    text: ' %',
                    position: "outter-middle"
                },
                min: 0,
                max: 100,
                padding: {
                    top:10,
                    bottom:10
                }
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
};

LepvCpuLineChart.prototype.updateChartData = function(data, messages=[]) {

    var thisChart = this;
    if ( !( 'CPU-0' in this.chartData) ) {
        this.chartData = {};
        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName] = ['CPU-' + coreName];
        });
        
    }
    if (this.timeData.length > this.maxDataCount) {
        this.timeData.splice(1, 1);

        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName].splice(1, 1);
        });
    }

    this.timeData.push(new Date());
    $.each( data, function( coreName, statValue ) {
        thisChart.chartData['CPU-' + coreName].push(statValue);
    });
    
    var columnDatas = [];
    columnDatas.push(this.timeData);
    $.each( data, function( coreName, statValue ) {
        columnDatas.push(thisChart.chartData['CPU-' + coreName]);
    });
    
    this.chart.load({
        columns: columnDatas
    });

    // temp logic, not every chart has a footer yet.
    if (this.panelFooter == null) {
        return;
    }

    if (this.chartDivName != 'div-cpu-stat-irqGroup') {
        return;
    }

    console.log("Irq+SoftIrq: " + data['0'] + "-" + data['1']);

    if (messages.length > 0) {
        console.log("    - Load NOT Balanced snapshot, warning detected");

        // if current snapshot has warning, and 10+ previous snapshots in a row have warning too, the system is considered load NOT balanced.
        if (this.loadBalanceWatcher['balanced'] == false) {

            this.loadBalanceWatcher['count'] = this.loadBalanceWatcher['count'] + 1;
            console.log("    - Load NOT Balanced snapshot - " + this.loadBalanceWatcher['count'] + " occurrences in a row");
            if (this.loadBalanceWatcher['count'] == this.loadBalanceLimit) {

                if (this.panelFooter.children('i').length == 0 ) {
                    var icon = $("<i></i>").addClass("glyphicon glyphicon-bell");
                    this.panelFooter.append(icon);
                    thisChart.controlElements['footerIcon'] = icon;
                }

                if (this.panelFooter.children('span').length == 0 ) {
                    var span = $("<span></span>").addClass("spanTitle");
                    this.panelFooter.append(span);
                    thisChart.controlElements['footerSpan'] = span;
                }
                thisChart.controlElements['footerSpan'].text(' ' + messages[0].message);

                this.UnBalanceHappened = true;
                alert(messages[0].message);
            }

        } else {
            // previous snapshots are "balanced"
            this.loadBalanceWatcher = {
                "balanced": false,
                 "count": 1
            }
        }

        console.log("Load is NOT balanced!");
        if (!thisChart.isWarningAlerted) {
            console.log("    -- alert now!");
            thisChart.isWarningAlerted = true;

            alert(messages[0].message + ", Please check CPU Stat: Irq+SoftIrq chart");
        } else {
            console.log("    -- alerted already");
        }
    } else {

        console.log("    ~ Load Balanced snapshot");

        // if current snapshot has warning, and 10+ previous snapshots in a row have warning too, the system is considered load NOT balanced.
        if (this.loadBalanceWatcher['balanced'] == true) {

            this.loadBalanceWatcher['count'] = this.loadBalanceWatcher['count'] + 1;
            console.log("    ~ Load Balanced snapshot - " + this.loadBalanceWatcher['count'] + " occurrences in a row");
            if (this.loadBalanceWatcher['count'] == this.loadBalanceLimit && this.UnBalanceHappened) {
                this.panelFooter.empty();
                this.UnBalanceHappened = false;   // clear the flag
                alert("Load is now balanced!");
            }
        } else {
            // previous snapshots are "NOT balanced", this is a status switch
            this.loadBalanceWatcher = {
                "balanced": true,
                 "count": 1
            }
        }
    }
};

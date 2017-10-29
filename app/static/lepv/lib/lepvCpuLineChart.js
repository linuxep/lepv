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
    this.warningOccurrences = 0;
    
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

    if (messages.length > 0) {

        thisChart.warningOccurrences++;

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

    } else {

        console.log("Load is balanced, no warning, will clear alert on UI");
        this.panelFooter.empty();
    }


};

"use strict";
exports.__esModule = true;
var $ = require("jquery");
var TSLepvChart = /** @class */ (function () {
    function TSLepvChart(rootDiv, socket, server) {
        this.rootDivName = rootDiv;
        this.socketIO = socket;
        this.serverToWatch = server;
        this.locateUIElements();
    }
    TSLepvChart.prototype.locateUIElements = function () {
        // locate the UI elements, like the header, footer, control buttons etc.
        console.log("Locating UI elements");
        var hsdf = $("#container-div-memory-chart");
        console.log(hsdf);
        console.log("sdfs");
    };
    return TSLepvChart;
}());

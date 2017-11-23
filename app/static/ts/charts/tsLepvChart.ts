
import * as $ from "jquery";

class TSLepvChart {

    rootDivName:string;
    rootDiv:object;

    chartDiv: string;
    headerDiv: string;
    footerDiv: string;
    
    socketIO: object;

    serverToWatch:string;

    socketMessageKey:string;
    socketRequestId:number;

    chart:object;

    chartData:object;

    isLeadingChart:boolean;

    constructor(rootDiv:string, socket:object, server:string) {
        this.rootDivName = rootDiv;
        this.socketIO = socket;
        this.serverToWatch = server;

        this.locateUIElements();
    }

    locateUIElements(): void {
        // locate the UI elements, like the header, footer, control buttons etc.
        console.log("Locating UI elements");

        var hsdf = $("#container-div-memory-chart");
        console.log(hsdf);
        console.log("sdfs");
    }


}
class TsLepvChart {

    public rootDivName: string;
    public chartDivName: string;

    public isLeadingChart: boolean;

    public socketIO: object;
    public headerDiv: object;
    public serverToMonitor: string;

    public socketMessageKey: string;
    public requestId: number;
    public responseId: number;

    public chart: object;
    public timeSeries: string[];

    constructor(rootDivName: string, socket: object, server: string) {
        console.log("constructing " + rootDivName);
        this.rootDivName = rootDivName;
        this.socketIO = socket;
        this.serverToMonitor = server;

        this.socketMessageKey = 'cpu.stat';
        this.isLeadingChart = true;

        this.setupSocketIO();
    }

    /**
     * setupSocketIO
     */
    public setupSocketIO() {

        this.socketIO.on( this.socketMessageKey + ".res", function(response) {
            console.log("  <- " + this.socketMessageKey + ".res");
            this.updateChartData(response);
        })

        if (this.isLeadingChart) {
            this.requestData();
        }
    }

    /**
     * requestData
     */
    public requestData() {

        if (this.socketMessageKey == null) {
            return;
        }
    
        if (! this.isLeadingChart) {
            return;
        }

        this.socketIO.emit(this.socketMessageKey + ".req", {'server': this.serverToMonitor})
        
    }

    /**
     * initialize
     */
    public initializeChart() {
        
    }

    /**
     * refreshData
     */
    public refreshData() {
        
    }

    /**
     * locateControlElements
     */
    public locateControlElements() {
        
    }

    /**
     * alert
     */
    public alert(message:string) {
        
    }

    /**
     * name
     */
    public clearAlert() {
        
    }

}

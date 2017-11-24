
function lepvFlameGraph(divName,jsonUrl,flameGraphWidth=960) {
    divName='#'+divName;
    var flamegraph = d4.flameGraph().width(flameGraphWidth);

    d4.json(jsonUrl, function(error, data) {
        if (error) return console.warn(error);
        d4.select(divName)
          .datum(data)
          .call(flamegraph);
    });
}


function barchart_withlegend(data, chartid, ylabel, margin, widthdivisor, rotation) {
 
    var chartDiv = document.getElementById(chartid + 'div');
    
    var svg = d3.select("#" + chartid),
        x = d3.scaleBand().padding(0.2).rangeRound([0, width]).paddingInner(0.07).align(0.1),
        y = d3.scaleLinear();

    //Get max length of xval (so it can be used to increase width size). The widthmultiplier may need to be adjustable/customisable:
    var widthmultiplier = 4;
    labelwidth = d3.max(data.map(function (d) { return d.xval.length * widthmultiplier; }))
    margin.right = margin.right + labelwidth

    x.domain(data.map(function (d) { return d.xval; }));
    y.domain([0, d3.max(data, function (d) { return d.yval; })]);
    
    var width = chartDiv.clientWidth / widthdivisor - margin.left - margin.right,
        height = chartDiv.clientHeight - margin.top - margin.bottom;

    legendcolours = d3.scaleOrdinal(d3.schemeCategory10);
//    legendlabels = data.map(function (d) { return d.xval; }).sort(function (a, b) { return a.toLowerCase().localeCompare(b.toLowerCase()) })
//    console.log(legendlabels)
    
    svg.attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom)

    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    g.append("g")
        .attr("class", "axis axis--x");

    g.append("g")
        .attr("class", "axis axis--y");

    x.rangeRound([0, width]);
    y.rangeRound([height, 0]);
    
    //X Axis
    g.select(".axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
            .selectAll("text").remove();

    g.select(".axis--y")
        .call(d3.axisLeft(y).ticks(2, "s"));

    var bars = g.selectAll(".bar2")
        .data(data);

    // Enter for bars
    bars.enter().append("rect")
        .attr("class", "bar2")
        .attr('style', function(d, i){
            return 'fill: ' + legendcolours(i) + ';';
        })
        .attr("x", function (d) { return x(d.xval); })
        .attr("y", height)
        .attr("width", x.bandwidth())
        .attr("height", 0 )
        .transition()
        .duration(300)
        .attr("y", function (d) { return y(d.yval); })
        .attr("height", function (d) { return height - y(d.yval); })
        ;

    //Enter for bar values
    bars.enter().append("text")
        .text(function(d) { return d.yval; })
        .attr("text-anchor", "middle")
        .attr("y", height)
        .attr('x', function(d) { return x(d.xval) + x.bandwidth() / 2; })
        .attr("class","label")
        .attr("dy", "1.2em")
        .transition()
        .duration(300)
        .attr("y", function(d) { return y(d.yval); })
        ;

    // Update
    bars.attr("x", function (d) { return x(d.xval); })
        .attr("y", function (d) { return y(d.yval); })
        .attr("width", x.bandwidth())
        .attr("height", function (d) { return height - y(d.yval); })
        ;

    // Exit
    bars.exit()
        .remove();
    
    
    var legend = svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("text-anchor", "end")
        .selectAll("g")
            .data(data)
            .enter().append("g")
                .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width + margin.right + 5)
        .attr("width", 19)
        .attr("height", 19)
        .attr("fill", function(d, i){
            return legendcolours(i);
        });
    
    legend.append("text")
        .attr("x", width + margin.right)
        .attr("y", 9.5)
        .attr("dy", "0.32em")
        .text(function(d) { return d.xval; });


}


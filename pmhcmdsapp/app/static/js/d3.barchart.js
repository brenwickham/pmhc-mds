

function barchart(data, chartid, ylabel, margin, widthdivisor, rotation) {
 
    var chartDiv = document.getElementById(chartid + 'div');
    
    var width = chartDiv.clientWidth / widthdivisor - margin.left * 2,
        height = chartDiv.clientHeight - margin.top - margin.bottom;

    var svg = d3.select("#" + chartid),
        x = d3.scaleBand().padding(0.1).rangeRound([0, width]).paddingInner(0.07).align(0.1),
        y = d3.scaleLinear();

    svg.attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom)

    x.domain(data.map(function (d) { return d.xval; }));
    y.domain([0, d3.max(data, function (d) { return d.yval; })]);

    
    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    g.append("g")
        .attr("class", "axis axis--x");

    g.append("g")
        .attr("class", "axis axis--y");

    g.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text(ylabel);

    x.rangeRound([0, width]);
    y.rangeRound([height, 0]);
    
    //X Axis
    g.select(".axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
            .selectAll("text") //Use to set x axis labels
                .attr("y", 0)
                .attr("x", 9)
                .attr("dy", ".35em")
                .attr("transform", "rotate(" + rotation + ")")
                .style("text-anchor", "start");

    g.select(".axis--y")
        .call(d3.axisLeft(y).ticks(2, "s"));

    var bars = g.selectAll(".bar")
        .data(data);

    // Enter for bars
    bars.enter().append("rect")
        .attr("class", "bar")
        .attr("x", function (d) { return x(d.xval); })
        .attr("y", height)
        .attr("width", x.bandwidth())
        .attr("height", 0 )
        .transition()
        .duration(300)
        .attr("y", function (d) { return y(d.yval); })
        .attr("height", function (d) { return height - y(d.yval); })
        ;

    // Enter for bars to add labels (optional value).
    bars.enter()
        .append("svg:title")
            .text(function(d) { return d.barlabel; });


    //Enter for bar values
    bars.enter().append("text")
        .text(function(d) { return d.yval; })
        .attr("text-anchor", "middle")
        .attr("y", height)
        .attr('x', function(d) { return x(d.xval) + x.bandwidth() / 2; })
        .attr("class","label")
        .attr("dy", "1em")
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

    // EXIT
    bars.exit()
    .remove();
    


}


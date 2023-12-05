class PieChart {
    constructor(selector, dataUrl) {
        this.selector = selector;
        this.dataUrl = dataUrl;

        this.width = 128;
        this.height = 128;
        this.radius = Math.min(this.width, this.height) / 2;
        this.colors = d3.scaleOrdinal(d3.schemeCategory10);

        this.svg = d3.select(selector).append("svg")
            .attr("width", this.width)
            .attr("height", this.height)
            .append("g")
            .attr("transform", `translate(${this.width / 2},${this.height / 2})`);

        this.tooltip = d3.select(selector).append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        this.arc = d3.arc()
            .innerRadius(0)
            .outerRadius(this.radius);

        this.pie = d3.pie()
            .sort(null)
            .value(d => d.value);

        this.init();
    }

    loadData() {
        return d3.csv(this.dataUrl);
    }

    init() {
        this.loadData().then(data => {
            this.update(data);
            this.render();
        });
    }

    // update(data) {
    //     console.log(data)
    //     const arcs = this.svg.selectAll(".arc")
    //         .data(this.pie(data));

    //     arcs.enter().append("path")
    //         .attr("class", "arc")
    //         .merge(arcs)
    //         .attr("d", this.arc)
    //         .attr("fill", (d, i) => this.colors(i))
    //         .on("mouseover", d => {
    //             this.tooltip.transition()
    //                 .duration(200)
    //                 .style("opacity", 0.9);
    //             this.tooltip.html(`${data.map(d => d.label)}: ${data.map(d => d.value)}`)
    //                 .style("left", `${d3.event.pageX}px`)
    //                 .style("top", `${d3.event.pageY - 28}px`);
    //         })
    //         .on("mouseout", () => {
    //             this.tooltip.transition()
    //                 .duration(500)
    //                 .style("opacity", 0);
    //         });

    //     arcs.exit().remove();
    // }
    update(data) {
        console.log(data);
    
        const arcs = this.svg.selectAll(".arc")
            .data(this.pie(data));
    
        arcs.enter().append("path")
            .attr("class", "arc")
            .merge(arcs)
            .attr("d", this.arc)
            .attr("fill", (d, i) => this.colors(i));
    
        arcs.exit().remove();
    
        // ラベル表示用のtext要素を追加
        const labels = this.svg.selectAll(".label")
            .data(this.pie(data));
    
        labels.enter().append("text")
            .attr("class", "label")
            .merge(labels)
            .attr("transform", d => `translate(${this.arc.centroid(d)})`)
            .attr("dy", "0.35em")
            .attr("text-anchor", "middle")
            .text(d => d.data.label);  // ラベルの表示
    
        labels.exit().remove();
    }
    

    render() {
        // Additional rendering options (e.g., legend, title) can be added here.
    }
}

// Usage example
const chart=new PieChart('#drawing_region', 'https://OkamiNaoki.github.io/simulationVis/W08/a.csv');
chart.init();
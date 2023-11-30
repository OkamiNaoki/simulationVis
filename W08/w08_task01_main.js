class BarChart {
    constructor(selector, dataUrl) {
        this.selector = selector;
        this.dataUrl = dataUrl;

        this.width = 256;
        this.height = 128;
        this.margin = { top: 10, right: 10, bottom: 20, left: 60 };

        this.svg = d3.select(selector).append("svg")
            .attr("width", this.width)
            .attr("height", this.height);

        this.chart = this.svg.append("g")
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);

        this.inner_width = this.width - this.margin.left - this.margin.right;
        this.inner_height = this.height - this.margin.top - this.margin.bottom;

        this.xscale = d3.scaleLinear().range([0, this.inner_width]);
        this.yscale = d3.scaleBand().range([0, this.inner_height]).paddingInner(0.1);

        this.xaxis = d3.axisBottom(this.xscale).ticks(5).tickSizeOuter(0);
        this.yaxis = d3.axisLeft(this.yscale).tickSizeOuter(0);

        this.drawAxes();
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

    update(data) {
        this.xscale.domain([0, d3.max(data, d => +d.value)]);
        this.yscale.domain(data.map(d => d.label));
        console.log(data.map(d => d.label))
        const xaxis_group = this.chart.select(".x-axis")
            .attr("transform", `translate(0, ${this.inner_height})`)
            .call(this.xaxis);

        const yaxis_group = this.chart.select(".y-axis")
            .call(this.yaxis);

        const bars = this.chart.selectAll("rect").data(data);

        bars.enter().append("rect")
            .merge(bars)
            .attr("x", 0)
            .attr("y", d => this.yscale(d.label))
            .attr("width", d => this.xscale(+d.value))
            .attr("height", this.yscale.bandwidth());

        bars.exit().remove();
    }

    render() {
        // Additional rendering options (e.g., chart title and axis labels) can be added here.
    }

    drawAxes() {
        this.chart.append("g").attr("class", "x-axis");
        this.chart.append("g").attr("class", "y-axis");
    }
}

// Usage example
const chart = new BarChart('#drawing_region', 'https://OkamiNaoki.github.io/simulationVis/W08/a.csv');
chart.init();

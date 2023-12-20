d3.csv('https://OkamiNaoki.github.io/simulationVis/W08/a.csv')
    .then(data => {
        data.forEach(d => { d.x = +d.value; d.y = d.label; });
        var config = {
            parent: '#drawing_region',
            width: 512,
            height: 512,
            margin: { top: 10, right: 10, bottom: 10, left: 30 }
        };

        const barchart = new BarChart(config, data);
        barchart.update();
        d3.select('#reverse')
            .on('click', d => {
                data.reverse();
                barchart.update();
            });
    })
    .catch(error => {
        console.log(error);
    });

class BarChart {
    constructor(config, data) {
        this.config = {
            parent: config.parent,
            width: config.width || 512,
            height: config.height || 512,
            margin: config.margin || { top: 10, right: 10, bottom: 10, left: 30 }
        }
        this.data = data;
        this.init();
    }
    init() {
        let self = this;

        self.svg = d3.select(self.config.parent)
            .attr('width', self.config.width)
            .attr('height', self.config.height);

        self.chart = self.svg.append('g')
            .attr('transform', `translate(${self.config.margin.left}, ${self.config.margin.top})`);

        self.inner_width = self.config.width - self.config.margin.left - self.config.margin.right;
        self.inner_height = self.config.height - self.config.margin.top - self.config.margin.bottom;

        self.xscale = d3.scaleLinear()
            .range([0, self.inner_width]);
        self.yscale = d3.scaleBand().range([0, self.inner_height]).paddingInner(0.1);

        self.xaxis = d3.axisBottom(self.xscale).ticks(5).tickSizeOuter(0);
        self.yaxis = d3.axisLeft(self.yscale).ticks(5).tickSizeOuter(0);

        self.xaxis_group = self.chart.append('g')
            .attr('transform', `translate(0, ${self.inner_height + self.config.margin.top})`);
        self.yaxis_group = self.chart.append('g')
            .attr('transform', `translate(0, ${self.config.margin.left})`);
    }

    update() {
        let self = this;

        const xmin = d3.min(self.data, d => d.x);
        const xmax = d3.max(self.data, d => d.x);
        self.xscale.domain([xmin, xmax]);

        self.yscale.domain(self.data.map(d => String(d.y)));

        self.render();
    }

    render() {

        let self = this;

        let padding = 80;
        let height = 40;
        console.log(self.data);

        self.chart.selectAll("rect")
            .data(self.data)
            .join("rect")
            .transition().duration(1000)
            .attr("x", 30)
            .attr("y", (d, i) => padding - 30 + i * (height + padding - 20))
            .attr("width", d => self.xscale(d.x))
            .attr("height", height);

        self.xaxis_group
            .call(self.xaxis);

        self.yaxis_group
            .call(self.yaxis);
    }
}

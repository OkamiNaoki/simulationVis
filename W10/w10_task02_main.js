d3.csv('https://OkamiNaoki.github.io/simulationVis/W08/a.csv')
    .then(data => {
        data.forEach(d => { d.x = +d.x; d.y = +d.y; });
        var config = {
            parent: '#drawing_region',
            width: 512,
            height: 512,
            margin: { top: 10, right: 10, bottom: 10, left: 30 }
        };

        const barchart = new BarChart(config, data);
        barchart.update();

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

        const ymin = d3.min(self.data, d => d.y);
        const ymax = d3.max(self.data, d => d.y);
        self.yscale.domain([ymin, ymax]);

        self.render();
    }

    render() {
        let self = this;

        let padding = 80;
        let height = 40;

        // ツールチップを表示するためのdiv要素を追加
        const tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0);

        // バーチャートを描画
        self.chart.selectAll("circle")
            .data(self.data)
            .join("circle")
            .transition().duration(1000)
            .attr('x', d => d.x)
            .attr('y', d => d.y)
            .attr('r', 10);
            // .on('mouseover', function (event, d) {
            //     // マウスがバーに乗ったときにツールチップを表示
            //     tooltip.transition().duration(200)
            //         .style('opacity', 0.9);
            //     tooltip.html(`X: ${d.x}<br>Y: ${d.y}`)
            //         .style('left', (event.pageX) + 'px')
            //         .style('top', (event.pageY - 28) + 'px');
            // })
            // .on('mouseout', function (event, d) {
            //     // マウスがバーから離れたときにツールチップを非表示
            //     tooltip.transition().duration(500)
            //         .style('opacity', 0);
            // });


            // .on('mouseover', (e,d) => {
            //     d3.select('#tooltip')
            //         .style('opacity', 1)
            //         .html(`<div class="tooltip-label">Position</div>(${d.x}, ${d.y})`);
            // })
            // .on('mousemove', (e) => {
            //     const padding = 10;
            //     d3.select('#tooltip')
            //         .style('left', (e.pageX + padding) + 'px')
            //         .style('top', (e.pageY + padding) + 'px');
            // })
            // .on('mouseleave', () => {
            //     d3.select('#tooltip')
            //         .style('opacity', 0);
            // });
        

        self.xaxis_group
            .call(self.xaxis);

        self.yaxis_group
            .call(self.yaxis);
    }
}

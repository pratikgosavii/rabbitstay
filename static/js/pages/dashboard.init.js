function getChartColorsArray(r) {
    r = $(r).attr("data-colors");
    r = JSON.parse(r);
    return r.map(function(r) {
        r = r.replace(" ", "");
        if (r.indexOf("--") == -1) return r;
        r = getComputedStyle(document.documentElement).getPropertyValue(r);
        return r || void 0;
    });
}

var barchartColors = getChartColorsArray("#mini-chart1");

var options = {
    series: [60, 40],
    chart: {
        type: "donut",
        height: 110
    },
    colors: barchartColors,
    legend: {
        show: false
    },
    dataLabels: {
        enabled: false
    }
};
var chart = new ApexCharts(document.querySelector("#mini-chart1"), options);
chart.render();
ChartColorChange(chart, "#mini-chart1");

options = {
    series: [30, 55],
    chart: {
        type: "donut",
        height: 110
    },
    colors: barchartColors = getChartColorsArray("#mini-chart2"),
    legend: {
        show: false
    },
    dataLabels: {
        enabled: false
    }
};
chart = new ApexCharts(document.querySelector("#mini-chart2"), options);
chart.render();
ChartColorChange(chart, "#mini-chart2");

options = {
    series: [65, 45],
    chart: {
        type: "donut",
        height: 110
    },
    colors: barchartColors = getChartColorsArray("#mini-chart3"),
    legend: {
        show: false
    },
    dataLabels: {
        enabled: false
    }
};
chart = new ApexCharts(document.querySelector("#mini-chart3"), options);
chart.render();
ChartColorChange(chart, "#mini-chart3");

options = {
    series: [50, 50],
    chart: {
        type: "donut",
        height: 110
    },
    colors: barchartColors = getChartColorsArray("#mini-chart4"),
    legend: {
        show: false
    },
    dataLabels: {
        enabled: false
    }
};
chart = new ApexCharts(document.querySelector("#mini-chart4"), options);
chart.render();
ChartColorChange(chart, "#mini-chart4");

options = {
    series: [{
        name: "Profit",
        data: [12.45, 16.2, 8.9, 11.42, 12.6, 18.1, 18.2, 14.16, 11.1, 8.09, 16.34, 12.88]
    }, {
        name: "Loss",
        data: [-11.45, -15.42, -7.9, -12.42, -12.6, -18.1, -18.2, -14.16, -11.1, -7.09, -15.34, -11.88]
    }],
    chart: {
        type: "bar",
        height: 400,
        stacked: true,
        toolbar: {
            show: false
        }
    },
    plotOptions: {
        bar: {
            columnWidth: "20%"
        }
    },
    colors: barchartColors = getChartColorsArray("#market-overview"),
    fill: {
        opacity: 1
    },
    dataLabels: {
        enabled: false
    },
    legend: {
        show: false
    },
    yaxis: {
        labels: {
            formatter: function(r) {
                return r.toFixed(0) + "%";
            }
        }
    },
    xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        labels: {
            rotate: -90
        }
    }
};

ChartColorChange(chart, "#market-overview");

var vectormapColors = getChartColorsArray("#sales-by-locations");

$("#sales-by-locations").vectorMap({
    map: "world_mill_en",
    normalizeFunction: "polynomial",
    hoverOpacity: 0.7,
    hoverColor: false,
    regionStyle: {
        initial: {
            fill: "#e9e9ef"
        }
    },
    markerStyle: {
        initial: {
            r: 9,
            fill: vectormapColors,
            "fill-opacity": 0.9,
            stroke: "#fff",
            "stroke-width": 7,
            "stroke-opacity": 0.4
        },
        hover: {
            stroke: "#fff",
            "fill-opacity": 1,
            "stroke-width": 1.5
        }
    },
    backgroundColor: "transparent",
    markers: [{
        latLng: [41.9, 12.45],
        name: "USA"
    }, {
        latLng: [12.05, -61.75],
        name: "Russia"
    }, {
        latLng: [1.3, 103.8],
        name: "Australia"
    }]
});
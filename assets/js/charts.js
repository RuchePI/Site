(function ($) {

    "use strict";

    function tooltipText(t, unit) {
        return Highcharts.dateFormat("<i>%d/%m/%Y à %H:%M:%S</i>", new Date(t.x)) +
            "<br><span style=\"font-weight: bold; color: " +
            t.series.options.color + "\">" + t.series.name + " :</span> " +
            t.y.toFixed(2).replace(".", ",").replace("-", "−") + " " + unit;
    }

    /* Test if readerings variable exists. */
    if (typeof readerings !== "undefined") {

        /* Global options. */
        Highcharts.setOptions({
            chart: {
                backgroundColor: "transparent",
                style: {
                    fontFamily: "inherit"
                },
                zoomType: "x"
            },
            credits: {
                enabled: false
            },
            lang: {
                decimalPoint: ","
            },
            title: {
                text: ""
            },
            xAxis: {
                type: "datetime",
                labels: {
                    formatter: function () {
                        return Highcharts.dateFormat("%d/%m/%y<br>%H:%M:%S", this.value);
                    }
                },
                minTickInterval: 60 * 60 * 1000
            },
            yAxis: {
                labels: {
                    formatter: function () {
                        return this.value.toString().replace("-", "−");
                    }
                }
            },
            legend: {
                layout: "vertical",
                align: "right",
                verticalAlign: "middle"
            },
            tooltip: {
                useHTML: true,
                backgroundColor: "#fafafa",
                borderColor: "#ddd",
                shadow: false
            }
        });

        /* Temperatures chart. */
        $("#temperatures_chart").highcharts({
            yAxis: {
                title: {
                    text: "Température (°C)"
                }
            },
            tooltip: {
                formatter: function () {
                    return tooltipText(this, "°C");
                }
            },
            series: [{
                name: "extérieure",
                color: "#222d32",
                data: readerings.outdoorTemperatures
            }, {
                name: "intérieure",
                color: "#3c8dbc",
                data: readerings.indoorTemperatures
            }, {
                name: "essaim",
                color: "#ffe245",
                data: readerings.swarmTemperatures
            }]
        });

        /* Humidities chart. */
        $("#humidities_chart").highcharts({
            yAxis: {
                title: {
                    text: "Humidité (%)"
                }
            },
            tooltip: {
                formatter: function () {
                    return tooltipText(this, "%");
                }
            },
            series: [{
                name: "extérieure",
                color: "#222d32",
                data: readerings.outdoorHumidities
            }, {
                name: "intérieure",
                color: "#3c8dbc",
                data: readerings.indoorHumidities
            }]
        });

        /* Weight chart. */
        $("#weight_chart").highcharts({
            yAxis: {
                title: {
                    text: "Masse (kg)"
                }
            },
            legend: {
                enabled: false
            },
            tooltip: {
                formatter: function () {
                    return tooltipText(this, "kg");
                }
            },
            series: [{
                name: "globale",
                color: "#3c8dbc",
                data: readerings.weight
            }]
        });

    }

}(jQuery));

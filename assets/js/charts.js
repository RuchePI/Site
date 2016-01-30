(function ($) {

    "use strict";

    /* Test if readerings variable exists. */
    if (typeof readerings !== "undefined") {

        /* Global options. */
        Highcharts.setOptions({
            chart: {
                backgroundColor: "transparent",
                style: {
                    fontFamily: "\"Open Sans\", Helvetica, Arial, sans-serif"
                }
            },
            credits: {
                enabled: false
            },
            title: {
                text: ""
            },
            xAxis: {
                categories: readerings.dates,
                labels: {
                    formatter: function () {
                        return Highcharts.dateFormat("%d/%m/%y<br>%H:%M:%S", this.value);
                    }
                }
            },
            legend: {
                layout: "vertical",
                align: "right",
                verticalAlign: "middle",
                borderWidth: 0
            },
            tooltip: {
                borderWidth: 0

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
                    return Highcharts.dateFormat("%d/%m/%Y à %H:%M:%S", new Date(this.x)) + "<br><strong>" + this.series.name + " :</strong> " + this.y + " °C";
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
                    return Highcharts.dateFormat("%d/%m/%Y à %H:%M:%S", new Date(this.x)) + "<br><strong>" + this.series.name + " :</strong> " + this.y + " %";
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

        /* Weigth chart. */
        $("#weigth_chart").highcharts({
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
                    return Highcharts.dateFormat("%d/%m/%Y à %H:%M:%S", new Date(this.x)) + "<br><strong>" + this.series.name + " :</strong> " + this.y + " kg";
                }
            },
            series: [{
                name: "globale",
                color: "#3c8dbc",
                data: readerings.weigth
            }]
        });

    }

}(jQuery));
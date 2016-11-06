$(function () {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    var needRAM = true;
    CPUChart();

    $("#ram-tab").click(function () {
        $("#cpu-tab").removeClass("is-active");
        $("#cpu-tab a").removeAttr("aria-selected");
        $("#cpu-panel").removeClass("is-active");
        $("#ram-tab").addClass("is-active");
        $("#ram-tab a").attr("aria-selected", "true");
        $("#ram-panel").addClass("is-active");
        if (needRAM) {
            RAMChart();
            needRAM = false
        }

    });
    $("#cpu-tab").click(function () {
        $("#ram-tab").removeClass("is-active");
        $("#ram-tab a").removeAttr("aria-selected");
        $("#ram-panel").removeClass("is-active");
        $("#cpu-tab").addClass("is-active");
        $("#cpu-tab a").attr("aria-selected", "true");
        $("#cpu-panel").addClass("is-active");
    });
    $("#leave-btn").click(function () {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/leave.do",
            dataType: "json",
            success: function (data) {
                if (data == "success") {
                    location.href = "http://127.0.0.1:5000/signin";
                }
            }
        });
    });
});
function CPUChart() {
    $('#cpu-chart').highcharts({
        chart: {
            type: 'line',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        $.ajaxSettings.async = false;
                        $.getJSON("http://127.0.0.1:5000/cpu/percent?t=" + (new Date()).getTime(), function (result) {
                            $.ajaxSettings.async = true;
                            var x = (new Date()).getTime(), // current time
                                y = result;
                            series.addPoint([x, y], true, true);
                        });
                    }, 1000);
                }
            }
        },
        title: {
            text: 'CPU Usage Rate'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'Rate(%)'
            },
            max: 100,
            min: 0,
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'CPU Usage Rate',
            data: (function () {
                // generate an array of random data
                var _data = [],
                    time = (new Date()).getTime(),
                    i;
                for (i = -19; i <= 0; i += 1) {
                    _data.push({
                        x: time + i * 1000,
                        y: i == 0 ? 0 : -100
                    });
                }
                return _data;
            } ())
        }]
    });
}
function RAMChart() {
    $.ajaxSettings.async = false;
    $.getJSON("http://127.0.0.1:5000/ram/total?t=" + (new Date()).getTime(), function (result) {
        $.ajaxSettings.async = true;
        RAMChartR(result)
    });
}
function RAMChartR(total) {
    $('#ram-chart').highcharts({
        chart: {
            type: 'line',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        $.ajaxSettings.async = false;
                        $.getJSON("http://127.0.0.1:5000/ram/used?t=" + (new Date()).getTime(), function (result) {
                            $.ajaxSettings.async = true;
                            var x = (new Date()).getTime(), // current time
                                y = result;
                            series.addPoint([x, y], true, true);
                        });
                    }, 1000);
                }
            }
        },
        title: {
            text: 'RAM Usage (Total: ' + total + 'GB)'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'Usage(GB)'
            },
            max: total,
            min: 0,
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'RAM Usage (Total: ' + total + 'GB)',
            data: (function () {
                // generate an array of random data
                var _data = [],
                    time = (new Date()).getTime(),
                    i;
                for (i = -19; i <= 0; i += 1) {
                    _data.push({
                        x: time + i * 1000,
                        y: i == 0 ? 0 : -100
                    });
                }
                return _data;
            } ())
        }]
    });
}
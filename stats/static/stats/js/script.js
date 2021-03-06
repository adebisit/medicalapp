options = {
    responsive: true,
    maintainAspectRatio: false,
    layout: {
        padding: {
            left: 25,
            right: 25,
            top: 10,
            bottom: 10
        }
    },
    legend: {
        display: true,
        position: 'bottom',
        align: 'center',
        fullWidth: true,
        labels: {
            boxWidth: 20,
            fontSize: 11,
        }
    },
    pointLabels: {
        fontSize: 14
    },
}

function generateBarChartConfig(chart_type, labels, data, colors){
    chartOption = $.extend({}, options)
    if (chart_type == "horizontalBar") {
        chartOption.scales = {
            xAxes: [{
                display: false,
                stacked: true
            }],
            yAxes: [{
                display: true,
                position: "left",
                gridLines: {display: false},
            }]
        }
    }


    config = {
        type: chart_type,
        data: {
            labels: labels,
            datasets: [{
                borderWidth: 0.5,
                barPercentage: 0.5,
                categoryPercentage: 15,
                data: data,
                backgroundColor: colors
            }]
        },
        options: chartOption
    }

    return config
}

function getPieChartConfig(chart_type, labels, data) {
    config = {
        type: chart_type,
        data: {
            labels: labels,
            datasets: [{
                borderWidth: 0.5,
                barPercentage: 0.5,
                categoryPercentage: 15,
                data: data
            }]
        },
        options: options
    }

    return config
}

console.log(age_dict)
config = generateBarChartConfig("horizontalBar", Object.keys(age_dict), Object.values(age_dict), "green")
canvas = document.getElementById("age-dist")
var chart = canvas.getContext('2d');
var ageDist = new Chart(chart, config)

config = generateBarChartConfig("doughnut", Object.keys(weight_status_dict), Object.values(weight_status_dict), ["red", "blue", "yellow", "black", "ash", "purple"])
canvas = document.getElementById("weight-dist")
var chart = canvas.getContext('2d');
var weightDist = new Chart(chart, config)

config = generateBarChartConfig("doughnut", ["A", "B", "C", "D", "E", "F"], [15, 20, 20, 30, 20, 15], ["red", "blue", "yellow", "black", "ash", "purple"])
canvas = document.getElementById("diet-dist")
var chart = canvas.getContext('2d');
var dietDist = new Chart(chart, config)

config = generateBarChartConfig("horizontalBar", Object.keys(blood_groups_dict), Object.values(blood_groups_dict), "red")
canvas = document.getElementById("blood-dist")
var chart = canvas.getContext('2d');
var bloodChart = new Chart(chart, config)

config = generateBarChartConfig("doughnut", Object.keys(genotypes_dict), Object.values(genotypes_dict), ["red", "blue", "yellow", "black", "ash", "purple"])
canvas = document.getElementById("genotype-dist")
var chart = canvas.getContext('2d');
var bloodChart = new Chart(chart, config)



thechart = null;
function initChart(element){
    thechart = echarts.init(element);
    return thechart;
}

function drawLineChart(title, name, xAxisValue, yAxisValue){
    var option = {
        title: {
            text: title,
        },
        tooltip: {},
        toolbox: {
            show: true,
            feature: {
                magicType: {
                    show: true,
                    type: ['line', 'bar', 'stack', 'tiled']
                },
            }
        },
        legend: {
            data:[name]
        },
        xAxis: {
            data: xAxisValue,
        },
        yAxis: {},
        series: [{
            name: name,
            type: 'line',
            data: yAxisValue,
        }],
        dataZoom: [{
                type: 'inside',
                xAxisIndex:0, 
                start: 0,
                end:50,
            },{
                type: 'slider',
                xAxisIndex: 0,
                start: 0,
                end: 50,
            }
        ]
    }
    thechart.clear();
    thechart.setOption(option)
}

function drawBarChart(title, name, xAxisValue, yAxisValue){
    var option = {
        title: {
            text: title
        },
        tooltip: {},
        toolbox: {
            show: true,
            feature: {
                magicType: {
                    show: true,
                    type: ['line', 'bar', 'stack', 'tiled']
                },
            }
        },
        legend: {
            data:[name]
        },
        xAxis: {
            data: xAxisValue,
        },
        yAxis: {},
        series: [{
            name: name,
            type: 'bar',
            data: yAxisValue
        }],
        dataZoom: [{
                type: 'inside',
                xAxisIndex:0, 
                start: 0,
                end:50,
            },{
                type: 'slider',
                xAxisIndex: 0,
                start: 0,
                end: 50,
            }
        ]
    }
    thechart.clear();
    thechart.setOption(option);
}

function drawPieDoughnutChart(title, name, legendData, seriresData){
    var option = {
        title : {
            text: title,
            x:'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data:legendData,
        },
        series: [
            {
                name:name,
                type:'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:seriresData
            }
        ]
    };
    thechart.clear();
    thechart.setOption(option);
}

function drawPieSimpleChart(title, name, legendData, seriresData){
    var option = {
        title : {
            text: title,
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: legendData,
        },
        series : [
            {
                name: name,
                type: 'pie',
                radius : '55%',
                center: ['50%', '60%'],
                data:seriresData,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    thechart.clear();
    thechart.setOption(option);
}

var typeRouter = {
    'line': drawLineChart,
    'bar': drawBarChart,
    'pie-doughnut': drawPieDoughnutChart,
    'pie-simple': drawPieSimpleChart,
}

function drawChart(option){
    var drawFunc = typeRouter[option['type']];
    drawFunc(option['title'], option['name'], option['xAxis'], option['yAxis']);
}
thechart = null;
function initChart(element){
    thechart = echarts.init(element);
    return thechart;
}

function drawLineChart(title, name, xAxisValue, yAxisValue, count){
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
            data: name
        },
        grid: [],
        xAxis: [],
        yAxis: [],
        series: [],
        dataZoom: [],
    }
    var h = (85/(count==0?1:count))-5;
    for (var i = 0; i < count; i++){
        option.grid.push({x:'5%',y:(i*(h+5)+10)+'%',width:'100%',height:h+'%'});
        option.xAxis.push({data:xAxisValue[i], gridIndex: i});
        option.yAxis.push({gridIndex: i});
        option.series.push({
            name: name[i],
            type: 'line',
            data: yAxisValue[i],
            xAxisIndex: i,
            yAxisIndex: i,
        });
    }
    option.dataZoom.push({
        type: 'inside',
        xAxisIndex: Array.apply(null, {length:count}).map(Number.call, Number), 
        start: 0,
        end:50,
    });
    option.dataZoom.push({
        type: 'slider',
        xAxisIndex: Array.apply(null, {length:count}).map(Number.call, Number),
        start: 0,
        end: 50,
    });
    thechart.clear();
    thechart.setOption(option);
}

function drawBarChart(title, name, xAxisValue, yAxisValue, count){
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
            data: name
        },
        grid: [],
        xAxis: [],
        yAxis: [],
        series: [],
        dataZoom: [],
    }
    var h = (85/(count==0?1:count))-5;
    for (var i = 0; i < count; i++){
        option.grid.push({x:'5%',y:(i*(h+5)+10)+'%',width:'100%',height:h+'%'});
        option.xAxis.push({data:xAxisValue[i], gridIndex: i});
        option.yAxis.push({gridIndex: i});
        option.series.push({
            name: name[i],
            type: 'bar',
            data: yAxisValue[i],
            xAxisIndex: i,
            yAxisIndex: i,
        });
    }
    option.dataZoom.push({
        type: 'inside',
        xAxisIndex: Array.apply(null, {length:count}).map(Number.call, Number), 
        start: 0,
        end:50,
    });
    option.dataZoom.push({
        type: 'slider',
        xAxisIndex: Array.apply(null, {length:count}).map(Number.call, Number),
        start: 0,
        end: 50,
    });
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
    drawFunc(option['title'], option['name'], option['xAxis'], option['yAxis'], option['count']);
}
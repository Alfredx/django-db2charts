<style type="text/css">
    .v-link-active {
        color: red;
        text-decoration: none;
    }
    .router-view-container{
        width: 100%;
        text-align: center;
        vertical-align: middle;
        height: 700px;
        position: relative;
    }
    .router-view-container .body{
        position: absolute;
        top: 40px;
        left: 0;
        right: 0;
        bottom: 0;
    }
    .footer{
        width: 100%;
        text-align: center;
        clear: both;
    }
    .data-source, .data-table{
        height: 200px;
        font-size:25px;
        margin: 25px 0px;
    }
    .data-source div, .data-table div {
        text-align: center;
        vertical-align: middle;
        width: 100%;
        border: 1px solid #999;
        padding: 5px 5px;
        line-height: 190px;
    }
    .data-chart {
        height: 200px;
        margin: 25px 0px;
    }
    .data-chart div {
        width: 100%;
        text-align: center;
        vertical-align: middle;
        border: 1px solid #999;
        padding: 5px 5px;
        line-height: 190px;
    }
    .data-chart img {
        max-height: 190px;
    }
    .selected-data-source {
        background-color: #cc3333;
    }
    .selected-data-table {
        background-color: #33cc33;
    }
    .selected-data-chart {
        background-color: #3399cc;
    }

    .leftTable {
        width: 18%;
        margin-right: 2%;
        position: absolute;
        top: 0px;
        left: 0px;
        right: 0px;
        bottom: 0px;
    }
    .leftTable .tableCols {
        top: 20px;
        left: 0px;
        right: 0px;
        bottom: 0px;
        overflow: auto;
        position: absolute;
    }
    .rightChartPreview{
        width: 80%;
        position: absolute;
        top: 0;
        left: 20%;
        right: 0;
        bottom: 0;
    }
    .rightChartPreview .chartOptions {
        width: 100%;
        height: 60px;
        margin-bottom: 10px;
    }
    .rightChartPreview .chartOptions .xAxis {
        width: 59%;
        float: left;
        height: 100%;
        vertical-align: middle;
    }
    .rightChartPreview .chartOptions .yAxis {
        width: 40%;
        float: left;
        height: 100%;
        vertical-align: middle;
    }
    .rightChartPreview .chartOptions .group-item {
        border: 1px solid #ddd;
        background-color: white;
        border-radius: 4px;
        padding: 0px 5px;
        line-height: 34px;
        font-size: 18px;
        height: 34px;
        float: left;
        min-width: 50px;
    }
    .rightChartPreview #chart {
        background-color: gray;
        position: absolute;
        top: 82px;
        left: 0px;
        right: 0px;
        bottom: 0px;
    }
    .dragging-item{
        background-color: gray;
    }
    .dragging-over-border {
        border: 2px dashed gray;
    }
    .seperator {
        border: 1px solid #ddd;
        margin: 10px 0px;
    }

</style>
<script type="text/javascript" src="/static/db2charts/js/vue.js"></script>
<script type="text/javascript" src="/static/db2charts/js/vue-router.js"></script>
<script type="text/javascript" src="/static/db2charts/js/echarts.min.js"></script>
<script type="text/javascript" src="/static/db2charts/js/echarts_component.js"></script>

<div style="display:none"><img src="/static/db2charts/image/loading.gif"></div>

<div id="app">
  <h1>请按步骤创建你的图表</h1>
  <p>
    <span class="{{$route.path=='/1'?'v-link-active':''}}">Step 1</span>&nbsp;&gt;&nbsp;
    <span class="{{$route.path=='/2'?'v-link-active':''}}">Step 2</span>&nbsp;&gt;&nbsp;
    <span class="{{$route.path=='/3'?'v-link-active':''}}">Step 3</span>&nbsp;&gt;&nbsp;
    <span class="{{$route.path=='/4'?'v-link-active':''}}">Step 4</span>
  </p>
  <div class="router-view-container">
    <router-view></router-view>
  </div>
  <div class="seperator"></div>
  <div class="footer">
    <button class="btn btn-primary btn-large" v-show="$route.path!='/1'" @click="onPrevClicked($route.path, $event)">上一步</button>
    <button class="btn btn-primary btn-large" @click="onNextClicked($route.path, $event)">{{$route.path=='/4'?'完成':'下一步'}}</button>
  </div>
</div>

<template id="s4-template">
<h3>Here you see step 4: select chart data</h3>
<div class="body">
    <div class="leftTable">
        <div>table:</div>
        <div class="tableCols">
            <div class="list-group"> 
                <span class="list-group-item" v-for="item in translatedCols" :value="$index" draggable="true" @dragstart="onDragStart(item, $event)">{{item.translated_col_name}}</span>
            </div>
        </div>
    </div>
    <div class="rightChartPreview">
        <div class="chartOptions">
            <div class="xAxis" @drop="onTypePush" @dragleave="onRemoveDragLeave" @dragover.prevent="onRemoveDragOver">
                <span>分类项:</span>
                <div>
                    <span class="group-item" v-for="item in selectedDataSource.chartOptions.selectedTypes" draggable="true" @dragend="onRemoveDragEnd(selectedDataSource.chartOptions.selectedTypes, item, $event)" @dragover.prevent="onRemoveDragOver">{{item.translated_col_name}}</span>
                </div>
            </div>
            <div class="yAxis" @dragover.prevent @drop="onDataPush" @dragleave="onRemoveDragLeave" @dragover="onRemoveDragOver">
                <span>统计项:</span>
                <div>
                    <span class="group-item" v-for="item in selectedDataSource.chartOptions.selectedData" draggable="true" @dragend="onRemoveDragEnd(selectedDataSource.chartOptions.selectedData, item, $event)">{{item.translated_col_name}}</span>
                </div>
            </div>
        </div>
        <div class="seperator"></div>
        <div id="chart">
    </div>
</div>
</template>

<script type="text/javascript">

    var userChartOptions = {
        selectedDB: '',
        selectedTable: '',
        selectedChart: '',
        chartOptions: {
            selectedTypes: [],
            selectedData: [],
        },
    }

    $.get = function(url, success){
        $.ajax({
            url: url,
            dataType: 'json',
            type: 'GET',
            success: success,
        });
    }

    var chartView = undefined;

    var loadingComponentDefinition = {
        template: '<img src="/static/db2charts/image/loading.gif">'
    }

    // Create a router instance.
    // You can pass in additional options here, but let's
    // keep it simple for now.
    var router = new VueRouter();

    var s1 = function(resolve){
        resolve(loadingComponentDefinition);
        $.get('/db2charts/api/analysis/create/db/', function(res){
            resolve({
                template: '<h3>Here you see step 1: select data source</h3>\
                            <div>\
                                <div v-for="db in availableDBs" class="col-xs-12 col-sm-6 col-md-4 col-lg-4 data-source" @click="onDataSourceClicked(db, $event)">\
                                    <div :class="selected(db)"><p>{{db}}</p></div>\
                                </div>\
                            </div>',
                data: function(){
                    return {
                        availableDBs: res,
                        selectedDataSource: userChartOptions,
                    }
                },
                methods: {
                    onDataSourceClicked: function(dataSource, event){
                        this.selectedDataSource.selectedDB = dataSource;
                        console.log(userChartOptions.selectedDB);
                    },
                    selected: function(db){
                        if (this.selectedDataSource.selectedDB == db){
                            return 'selected-data-source';
                        } else {
                            return '';
                        }
                    }
                },
                ready: function(){
                    console.log('s1 ready');
                }
            });
        });
    }

    var s2 = function(resolve){
        resolve(loadingComponentDefinition);
        $.get('/db2charts/api/analysis/create/table/?db='+userChartOptions.selectedDB, function(res){
            resolve({
                template: '<h3>Here you see step 2: select table</h3>\
                            <div>\
                                <div v-for="item in availableTables" class="col-xs-12 col-sm-6 col-md-4 col-lg-4 data-table" @click="onDataTableClicked(item.model_name, $event)">\
                                    <div :class="selected(item.model_name)"><p>{{item.translated_name}}</p></div>\
                                </div>\
                            </div>',
                data: function(){
                    return {
                        availableTables: res,
                        selectedDataSource: userChartOptions,
                    }
                },
                methods: {
                    onDataTableClicked: function(dataTable, event){
                        this.selectedDataSource.selectedTable = dataTable;
                        console.log(userChartOptions.selectedTable);
                    },
                    selected: function(model_name){
                        if (this.selectedDataSource.selectedTable == model_name){
                            return 'selected-data-table';
                        } else {
                            return '';
                        }
                    }
                },
                ready: function(){
                    if (!this.selectedDataSource.selectedDB){
                        router.go('/1');
                    }
                    $.get('/db2charts/api/analysis/create/table/?db='+userChartOptions.selectedDB, (function(res){
                        this.availableTables = res;
                    }).bind(this));
                    console.log('s2 ready');
                }
            });
        });
    }

    var s3 = Vue.extend({
        template: '<h3>Here you see step 3: select chart type</h3>\
                    <div v-for="item in supportedCharts">\
                        <div class="col-xs-12 col-sm-6 col-md-4 col-lg-4 data-chart" @click="onChartClicked(item.name, $event)">\
                            <div :class="selected(item.name)"><img :src="item.url"></div>\
                        </div>\
                    </div>',
        data: function() {
            return {
                supportedCharts: [
                    {name: 'line',url:'/static/db2charts/image/line.png'},
                    {name: 'bar', url:'/static/db2charts/image/bar.png'},
                    {name: 'pie-doughnut', url:'/static/db2charts/image/pie-doughnut.png'},
                    {name: 'pie-simple', url:'/static/db2charts/image/pie-simple.png'}
                ],
                selectedDataSource: userChartOptions,
            }
        },
        methods: {
            onChartClicked: function(chartName, event){
                this.selectedDataSource.selectedChart = chartName;
                console.log(userChartOptions.selectedChart);
            },
            selected: function(chartName){
                if (this.selectedDataSource.selectedChart == chartName){
                    return 'selected-data-chart';
                } else {
                    return '';
                }
            }
        },
        ready: function(){
            if (!this.selectedDataSource.selectedDB){
                router.go('/1');
            } else if (!this.selectedDataSource.selectedTable) {
                router.go('/2');
            }
            console.log('s3 ready');
        }
    })

    var s4 = function(resolve){
        resolve(loadingComponentDefinition);
        $.get('/db2charts/api/analysis/create/tablecols/?model_name='+userChartOptions.selectedTable, function(res){
            resolve({
                template: '#s4-template',
                data: function() {
                    return {
                        translatedCols: res.data?res.data:[],
                        selectedDataSource: userChartOptions,
                        selectedCol: 0,
                        selectedType: NaN,
                        selectedData: NaN,
                        removeCol: null,
                        willRemove: false,
                        draggingData: null,
                    }
                },
                methods: {
                    onTypePush: function(event){
                        $('.dragging-item').removeClass('dragging-item');
                        $('.dragging-over-border').removeClass('dragging-over-border');
                        var colData = this.draggingData;
                        if (colData && this.selectedDataSource.chartOptions.selectedTypes.indexOf(colData) == -1){
                            this.selectedDataSource.chartOptions.selectedTypes.push(colData);
                            this.renderChart();
                        }
                        this.draggingData = null;
                    },
                    onDataPush: function(event){
                        $('.dragging-item').removeClass('dragging-item');
                        $('.dragging-over-border').removeClass('dragging-over-border');
                        var colData = this.draggingData;
                        if (colData && this.selectedDataSource.chartOptions.selectedData.indexOf(colData) == -1){
                            this.selectedDataSource.chartOptions.selectedData.push(colData);
                            this.renderChart();
                        }
                        this.draggingData = null;
                    },
                    onRemoveDragLeave: function(event){
                        this.willRemove = true;
                        $(event.target).removeClass('dragging-over-border');
                    },
                    onRemoveDragOver: function(event){
                        this.willRemove = false;
                        if ($(event.target).hasClass('group-item')){
                            $(event.target).parent().parent().addClass('dragging-over-border');
                        } else {
                            $(event.target).addClass('dragging-over-border');
                        }
                    },
                    onDragStart: function(item, event){
                        $(event.srcElement).addClass('dragging-item');
                        this.draggingData = item;
                    },
                    onRemoveDragEnd: function(list, item, event){
                        if (this.willRemove){
                            list.$remove(item);
                            this.renderChart();
                        }
                    },
                    renderChart: function(){
                        var t = [];
                        for (var i in userChartOptions.chartOptions.selectedTypes){
                            t.push(userChartOptions.chartOptions.selectedTypes[i].col_name);
                        }
                        t = t.join(',');
                        var d = [];
                        for (var i in userChartOptions.chartOptions.selectedData){
                            d.push(userChartOptions.chartOptions.selectedData[i].col_name);
                        }
                        d = d.join(',');
                        $.get('/db2charts/api/analysis/create/preview/?model_name='+userChartOptions.selectedTable+'&xAxis='+t+'&yAxis='+d, function(res){
                            drawChart({
                                type: userChartOptions.selectedChart, 
                                title: res.legend,
                                name: res.serie_name,
                                xAxis: res.data.xAxis,
                                yAxis: res.data.yAxis,
                                count: res.count,
                            });
                        });
                    }
                },
                ready: function(){
                    if (!this.selectedDataSource.selectedDB){
                        router.go('/1');
                    } else if (!this.selectedDataSource.selectedTable) {
                        router.go('/2');
                    } else if (!this.selectedDataSource.selectedChart) {
                        router.go('/3');
                    } else {
                        console.log('s4 ready');
                        chartView = initChart(document.getElementById('chart'));
                        $.get('/db2charts/api/analysis/create/tablecols/?model_name='+userChartOptions.selectedTable, (function(res){
                            this.translatedCols = res.data;
                            this.renderChart();
                        }).bind(this));
                    }
                }
            });
        });
    }

    // The router needs a root component to render.
    // For demo purposes, we will just use an empty one
    // because we are using the HTML as the app template.
    var App = Vue.extend({
        methods: {
            onNextClicked: function(currentPath, event){
                switch(currentPath){
                    case '/1':
                        router.go('/2');
                        break;
                    case '/2':
                        router.go('/3');
                        break;
                    case '/3':
                        router.go('/4');
                        break;
                    case '/4':
                        alert('you have finished all 4 steps');
                        console.log(userChartOptions.selectedDataSource);
                        console.log(userChartOptions.selectedTable);
                        console.log(userChartOptions.selectedChart);
                        console.log(userChartOptions.chartOptions);
                        $.ajax({
                            url: '/db2charts/api/analysis/create/submit/',
                            type: 'POST',
                            dataType: 'json',
                            data: JSON.stringify({'options':userChartOptions}),
                            success: function(res){
                                console.log(res);
                            }
                        })
                        break;
                }
            },
            onPrevClicked: function(currentPath, event){
                switch(currentPath){
                    case '/2':
                        router.go('/1');
                        break;
                    case '/3':
                        router.go('/2');
                        break;
                    case '/4':
                        router.go('/3');
                        break;
                }
            }
        },
    })

    // Define some routes.
    // Each route should map to a component. The "component" can
    // either be an actual component constructor created via
    // Vue.extend(), or just a component options object.
    // We'll talk about nested routes later.
    router.map({
        '/': {
            component: {
                ready: function(){
                    router.go('/1');
                }
            }
        },
        '/1': {
            component: s1
        },
        '/2': {
            component: s2
        },
        '/3': {
            component: s3
        },
        '/4': {
            component: s4
        }
    })

    // Now we can start the app!
    // The router will create an instance of App and mount to
    // the element matching the selector #app.
    router.start(App, '#app')

</script>
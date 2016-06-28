<style type="text/css">
</style>

<script type="text/javascript" src="/static/db2charts/js/vue.js"></script>
<script type="text/javascript" src="/static/db2charts/js/vue-router.js"></script>
<script type="text/javascript" src="/static/db2charts/js/echarts.min.js"></script>
<script type="text/javascript" src="/static/db2charts/js/echarts_component.js"></script>

<div id="app">
    <div style="text-align:center;margin-top:20%;margin-left:auto;margin-right:auto;" v-show="showLoading">
        <img src="/static/db2charts/image/loading.gif">
    </div>
    <div id="chart" :style="chartStyle"></div>
    <table class="table" id="mtable" style="background-color:white;">
        <thead id="table_head">
            <tr></tr>
        </thead>
        <tbody></tbody>
    </table>
</div>

<script type="text/javascript">
    function prepareTableHeader(tableCols) {
        $('thead tr').empty();
        var dtColumns = [];
        for (var i in tableCols){
            var th = document.createElement('th');
            $(th).html(tableCols[i].split('.')[2]);
            $('thead tr').append($(th));
            dtColumns.push({'data': tableCols[i].split('.')[2]});
        }
        return dtColumns;
    }
    function setupDataTable(dtColumns, data) {
        var t = $('#mtable').DataTable({
            'language': {
                url: '/static/db2charts/locale/zh_CN.json',
            },
            'data': data,
            'deferRender': true,
            'columns': dtColumns,
            'scrollY': '600px',
            'scrollX': '100%',
            'scrollCollapse': true,
            'pageLength': '50',
            fixedColumns: {
                leftColumns: 1
            }
        });
        return t;
    }
    $(document).ready(function(){
        var App = new Vue({
            el: '#app',
            data: {
                showLoading: true,
            },
            methods: {

            },
            computed: {
                chartStyle: function(){
                    return {
                        width: '95%',
                        height: window.innerHeight - $('#app').position().top - 100 + 'px',
                        'margin-bottom': '50px',
                    }
                }
            },
            ready: function(){
                initChart($('#chart')[0]);
                var report_id = window.location.pathname.match(/\/\d\/$/)[0].replace(/\//g,'');
                var vueInstance = this;
                $.ajax({
                    url: '/db2charts/api/analysis/report/?report_id='+report_id,
                    type: 'GET',
                    dataType: 'json',
                    success: function(result){
                        var dtColumns = prepareTableHeader(result.table_cols);
                        var table = setupDataTable(dtColumns, result.table_data);
                        console.log(result);
                        drawChart({
                            type: result.chart_type, 
                            title: result.legend,
                            name: result.serie_name,
                            xAxis: result.data.xAxis,
                            yAxis: result.data.yAxis,
                            count: result.count,
                        });
                        vueInstance.showLoading = false;
                    }
                });
            }
        })
    });
    
</script>
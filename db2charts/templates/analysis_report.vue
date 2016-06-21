<style type="text/css"></style>

<script type="text/javascript" src="/static/db2charts/js/vue.js"></script>
<script type="text/javascript" src="/static/db2charts/js/vue-router.js"></script>
<script type="text/javascript" src="/static/db2charts/js/echarts.min.js"></script>
<script type="text/javascript" src="/static/db2charts/js/echarts_component.js"></script>

<div id="app">
    <div id="chart" :style="chartStyle"></div>
    <table class="table">
        <thead></thead>
        <tbody></tbody>
    </table>
    <input>
</div>

<script type="text/javascript">
    $.ajax({
        url: '/db2charts/api/analysis/report/?report_id=1',
        type: 'GET',
        dataType: 'json',
        success: function(result){
            console.log(result);
        }
    })
    var App = new Vue({
        el: '#app',
        methods: {

        },
        computed: {
            chartStyle: function(){
                return {
                    width: '100%',
                    height: window.innerHeight - $('#app').position().top - 100 + 'px',
                }
            }
        },
        ready: function(){
            initChart($('#chart')[0]);
        }
    })
</script>
var availableTable, allTable = null;
$(document).ready(function(){

    availableTable = $('#available_model_table').DataTable({
        language: {
            url: '/static/db2charts/locale/zh_CN.json'
        },
        ajax: {
            url: '/db2charts/api/analysis/manage/available/',
        },
        columns: [
            {'data': null},
            {'data': 'model_name'},
            {'data': 'translated_name'},
            {
                'render': function(data, type, row, meta){
                    return '<button type="button" class="btn btn-primary btn-func-update">修改</button>';
                }
            },
            {
                'data': 'active',
                'render': function(data, type, row, meta){
                    var active = row.active;
                    var btnClass = (active?'btn-danger':'btn-success');
                    var actionDesc = (active?'停用':'启用');
                    return '<button type="button" class="btn '+btnClass+' btn-func-active">'+actionDesc+'</button>';
                }
            }
        ],
    });
    allTable = $('#all_model_table').DataTable({
        language: {
            url: '/static/db2charts/locale/zh_CN.json'
        },
        processing: true,
        ajax: {
            url: '/db2charts/api/analysis/manage/all/',
        },
        columns: [
            {'data': null,}, 
            {'data': 'model_name',}, 
            {
                'data': 'active',
                'render': function(data, type, row, meta){
                    return data?'是':'否';
                }
            },
            {
                'data': null,
                'render': function(data, type, row, meta){
                    var active = row.active;
                    var btnClass = (active?'btn-danger':'btn-primary');
                    var actionDesc = (active?'删除':'添加');
                    var funcClass = (active?'btn-func-delete':'btn-func-add')
                    return '<button type="button" class="btn '+btnClass+' '+funcClass+'">'+actionDesc+'</button>';
                },
            },
        ],
        pageLength: 25,
        scrollX: true,
    });
    allTable.on('order.dt search.dt',
        function() {
            allTable.column(0, {
                search: 'applied',
                order: 'applied'
            }).nodes().each(function(cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    availableTable.on('order.dt search.dt',
        function() {
            availableTable.column(0, {
                search: 'applied',
                order: 'applied'
            }).nodes().each(function(cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    function createTranslateNode(desc, preName, inputValue){
        var placeholder = preName.split('.');
        placeholder = placeholder[placeholder.length-1];
        var html = '<tr><th>'+desc+'</th><td>'+preName+'</td><td><input id="translate_input_'+preName.replace(/\./g,'_')+'" placeholder="'+placeholder+'" value="'+(inputValue?inputValue:'')+'"></td></tr>';
        return html;
    }
    function prepareTranslateModal(labelData, ajaxOption, inputData){
        var row_data = labelData;
        var model_name = row_data.model_name;
        var active = row_data.active;
        $('#translate_modal_table').empty();
        var translated_cols = {};
        var translated_model_name = ''
        if (inputData){
            for (var i in inputData.cols) {
                translated_cols[inputData.cols[i].col_name] = inputData.cols[i].translated_col_name;
            }
            translated_model_name = inputData.model_name;
        }
        $('#translate_modal_table').append(createTranslateNode('表名',model_name, translated_model_name));
        for (var i in row_data.cols){
            $('#translate_modal_table').append(createTranslateNode('列', row_data.cols[i], translated_cols[row_data.cols[i]]));
        }
        $('#translate_use_origin').unbind('click').click(function(){
            var inputs = $('#translate_modal_table input');
            for (var i in inputs){
                if (!$(inputs[i]).val()){
                    $(inputs[i]).val($(inputs[i]).attr('placeholder'));
                }
            }
        });
        $('#translate_submit').unbind('click').click(function(modalClickEvent){
            var translated_model_name = $('#translate_input_'+model_name.replace(/\./g,'_')).val();
            if (!translated_model_name){
                console.log('请给你的表名一个可阅读的名字');
                return;
            }
            var ajaxData = {
                model_name: model_name,
                translated_model_name: translated_model_name,
                cols: [],
            }
            for (var i in row_data.cols){
                var translated_col_name = $('#translate_input_'+row_data.cols[i].replace(/\./g,'_')).val();
                if (translated_col_name){
                    ajaxData.cols.push({
                        col_name: row_data.cols[i],
                        translated_col_name: translated_col_name,
                    });
                }
            }
            $.ajax({
                url: ajaxOption.url,
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify(ajaxData),
                success: ajaxOption.success,
            })
        });
        return $('#translate_modal_table');
    }
    function onAddAvailableClicked(e){
        var row_data = allTable.row( $(e.currentTarget).parents('tr') ).data();
        prepareTranslateModal(row_data, {
            url: '/db2charts/api/analysis/manage/submit/',
            success: function(data){
                if (data.status != 0){
                    console.log('Error: '+data.message);
                } else {
                    $('#translate_available_modal').modal('hide');
                    availableTable.ajax.reload().draw();
                    row_data.active = true;
                    allTable.row($(e.currentTarget).parents('tr')).data(row_data).draw();
                }
            }
        });
        $('#translate_available_modal').modal();
    }
    function onRemoveAvailableClicked(e){
        var row_data = allTable.row( $(e.currentTarget).parents('tr') ).data();
        var model_name = row_data.model_name;
        bootbox.confirm('确认删除 '+model_name+' ?', function(result){
            if (!result)
                return;
            $.ajax({
                url: '/db2charts/api/analysis/manage/delete/',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify({model_name:model_name}),
                success: function(data){
                    if (data.status != 0){
                        console.log('Error: '+data.message);
                    } else {
                        availableTable.ajax.reload().draw();
                        row_data.active = false;
                        allTable.row($(e.currentTarget).parents('tr')).data(row_data).draw();
                    }
                }
            });
        });
    }
    function onAvailableActiveClicked(e){
        var row_data = availableTable.row($(e.currentTarget).parents('tr')).data();
        $.ajax({
            url: '/db2charts/api/analysis/manage/active/',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                model_name: row_data.model_name,
                active:!row_data.active
            }),
            success: function(data){
                if (data.status != 0){
                    console.log('Error: '+data.message);
                } else {
                    row_data.active = !row_data.active;
                    availableTable.row($(e.currentTarget).parents('tr')).data(row_data).draw();
                }
            }
        });
    }
    function onAvailableUpdateClicked(e){
        var available_row_data = availableTable.row($(e.currentTarget).parents('tr')).data();
        var all_row_data = allTable.data().filter(function(value, index){
            return value.model_name == available_row_data.model_name;
        })[0];
        prepareTranslateModal(all_row_data, {
            url: '/db2charts/api/analysis/manage/update/',
            success: function(data){
                if (data.status != 0){
                    console.log('Error: '+data.message);
                } else {
                    availableTable.ajax.reload().draw();
                    $('#translate_available_modal').modal('hide');
                }
            }
        }, {
            model_name: available_row_data.translated_name,
            cols: available_row_data.cols,
        });
        $('#translate_available_modal').modal();
    }
    $('#translate_available_modal').on('shown.bs.modal', function () {
      $(this).find('input:text:visible:first').focus();
    });
    $('#available_model_table tbody').on('click', '.btn-func-update', onAvailableUpdateClicked);
    $('#available_model_table tbody').on('click', '.btn-func-active', onAvailableActiveClicked);
    $('#all_model_table tbody').on('click', '.btn-func-add', onAddAvailableClicked);
    $('#all_model_table tbody').on('click', '.btn-func-delete', onRemoveAvailableClicked);
});
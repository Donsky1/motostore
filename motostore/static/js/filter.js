$('select#mark').change(function(){
    $('select#mark option:selected').each(function(){
        var selected_mark = $(this).text()

    $.ajax({
        url: '/get-model-filter/',
        data: {'model_name': selected_mark},
        success: function (data) {
            console.log(data)
            $('#test').html('<b>'+ data[0].name +'</b>')
            $('select#model').empty()
            for (i in data){
                var mark_id = data[i].id
                var mark_name = data[i].name
                $('select#model').append('<option value=' + mark_id + '>' + mark_name + '</option>')
            }
        }
        });
     });
    $('#model').prop('disabled', false);
});
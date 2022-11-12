let searchParams = new URLSearchParams(window.location.search)

$( document ).ready(function() {
    save_data();
});

async function save_data(){
    if (searchParams.has('mark')){
        var selected_mark = searchParams.get('mark');
        $('select#mark').val(selected_mark);
        await get_data(selected_mark)
        $('#model').prop('disabled', false);
        if (searchParams.has('model')){
            var selected_model = searchParams.get('model');
            console.log(selected_model);
            $('select#model').val(selected_model)
        }
    }
};

$('select#mark').change(function(){
    $('select#mark option:selected').each(function(){
        var selected_mark = $(this).text()
        get_data(selected_mark)
    });
    $('#model').prop('disabled', false);
});


function get_models_from_db(selected_mark){
    return $.ajax({
        url: '/get-model-filter/',
        data: {'selected_mark': selected_mark},
        success: function (data) {
            console.log(data)
            $('select#model').empty()
            $('select#model').append('<option disabled selected>Выберите модель</option>')
            for (i in data){
                var mark_name = data[i].name
                $('select#model').append('<option value="' + mark_name + '">' + mark_name + '</option>')
            }
        }
        });
};


async function get_data(selected_mark){
    return await get_models_from_db(selected_mark)
};
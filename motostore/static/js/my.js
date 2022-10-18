//generation token to access by api
$(document).on('click', '#ajax_gen_token', function(event) {
        $.ajax({
          url: "/users/generate-token-ajax/",
          success: function(data){
            $('#token').html(data.key)
          },
        });
});
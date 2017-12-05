  $(document).ready(function() {
    $("#copyright_end").text(moment().format("YYYY"));
    function goalCallback () {
        console.log('запрос в Метрику успешно отправлен');
    }

    function CloseItemMenu(data) {
        if (data){
            $('.hide_block_login').addClass('hide');
        }
    };

   $("[data-startloginbyclick]").keydown(function(event) {
        if (event.keyCode == 13) {
            $('#alogin2').click();
            event.preventDefault();
         }
    });

    /*CloseItemMenu({% if session.logged_in %}0{% else %}0{% endif %});*/

  });
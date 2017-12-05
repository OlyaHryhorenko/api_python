
$(document).ready(function() {
    $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });

        var dateToday = new Date();
         $('#deadlineDate').datepicker({
            minDate: dateToday,
            dateFormat: 'yy-mm-dd'
         });//jquery Ui



    $("#phone").intlTelInput({
      initialCountry: "auto",
      geoIpLookup: function(callback) {
        $.get('http://ipinfo.io', function() {}, "jsonp").always(function(resp) {
          var countryCode = (resp && resp.country) ? resp.country : "";
          callback(countryCode);
      });
    }

});



    $(".tab_item").not(":first").hide();
    $(".tab_suere").not(":last").show();
    $(".tab p").not(":last").addClass("act-p");
    $(".wrapper .tab").not(":last").addClass("act");
    $(".wrapper .tab").click(function() {
        $(".wrapper .tab").removeClass("act").eq($(this).index()).addClass("act");
        $(".tab p").removeClass("act-p").eq($(this).index()).addClass("act-p");
        $(".tab_item").hide().eq($(this).index()).fadeIn()
        $(".tab_suere").hide().eq($(this).index()).fadeIn();

        if ($('.tab-one').hasClass('act')){
             $('#orderForm').attr("onclick","aregister()");
        } else {
            $('#orderForm').attr("onclick","alogin()");
        };
    });
});


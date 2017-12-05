function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : 0;
  }

  if(typeof currentDiscount != 'undefined') {
    if(getCookie('delayDiscount')) {
      window.delayD = getCookie('delayDiscount');
    }else{
      window.delayD = 60000;
    }

    $('#discount-modal .close').on('click', function() {
      $('#discount-modal').removeClass('open-discount');
      document.cookie = 'delayDiscount=240000';//
      window.delayD = 240000;
      setTimeout(function() {
        $('#discount-modal').addClass('open-discount');
      }, delayD);
    });

    setTimeout(function() {
      $('#discount-modal').addClass('open-discount');
    }, delayD);
  }

  var isMobile = {
    Android: function(){
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function(){
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function(){
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function(){
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function(){
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function(){
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
    }
  };


  $("#calc1AcadLevel, #calc1Essay").on('change', function() {
    runCalc();
  });

  $(function() {

    var offsetTop = {};

    $('.hidden-for-animation').each(function(e) {
      var top = $(this).css('top').replace(/[^0-9]/g, ''),
          offset = $(this).offset().top,
          key = (top) ? offset - top : offset;

      offsetTop[key] = $(this);
    });

    if( $(window).width() < 750 || isMobile.any() ) {
      $('.hidden-for-animation').removeClass('hidden-for-animation');
      $('.steps-item.hidden').removeClass('hidden');
    }

    if(Object.keys(offsetTop).length != 0) {
      var scrollFunction = function(current) {
        var scrolled = window.pageYOffset || document.documentElement.scrollTop,
            height = $(window).height();

        scrolled = scrolled + height / 2;

        for(var key in offsetTop) {
          var m = offsetTop[key].data('margin');
          m = (m) ? m : 0;

          scrolled = scrolled + m;

          if(scrolled >= key) {
            if(offsetTop[key].data('current')) {
              stepsAnim(offsetTop[key]);
            }else{
              offsetTop[key].removeClass('hidden-for-animation');
            }
            delete offsetTop[key];
          }
        }
      };
      window.onscroll = scrollFunction;
      scrollFunction(true);
    }
  });
  if($('#global-logout').length != 0) {
    $('#glob-header .glob-nav .header-nav').append('<li class="opened-item dashboard-link"><a href="/dashboard">Dashboard</a></li>');
  }
  function stepsAnim(el) {
    var i = 0,
        items = el.find('.steps-item'),
        interval = setInterval(function() {
          if(!items.eq(i).length) {
            clearInterval(interval);
          }

          items.eq(i).removeClass('hidden');
          i++;
        }, i + 200);
/*
    el.find('.steps-item').each(function() {
      var l = $(this);
      l.removeClass('hidden').hide(0).delay(i + 500);
    });*/
  }


   var calc = {
  type : '#calc1Essay',
  page : '#pagesLength',
  academ : '#calc1AcadLevel',
  deadline : 'calc1Calendar'
};


$('#pagesLength').on('keyup', function(event) {
  var charKey = event.keyCode;
  if(charKey >= 49 && charKey <= 57 || charKey == 8 || charKey == 40 || charKey == 38) {}else{
    var t = /[^\d]/gi;
    var c = $(this).val().replace(t, '');
    $(this).val(c);
    return false;
  }
  switch(charKey) {
    case 40 : $(this).parents('.order-input-with-button').find('.inline-button.prev').click();
      break;
    case 38 : $(this).parents('.order-input-with-button').find('.inline-button.next').click();
      break;
  }
  if($(this).val() > $(this).data('max')){
    $(this).val($(this).data('max'));
  }
  runCalc()
}).focusout(function() {
  if($(this).val() == '') {
    $(this).val( $(this).data('min') );
  }
  if($(this).val() > $(this).data('max')){
    $(this).val($(this).data('max'));
  }
}).on('change', function() {
  runCalc();
});

$("#calc1Calendar").val(gettomorrowdate());

$("#calc1Calendar").datepicker({
  showAnim: "slideDown",
  dateFormat: 'yy-mm-dd',
  defaultDate : new Date(),
  minDate : '+1d',
  maxDate : '+1y',
  onSelect: function(date) {
        runCalc();
    }
}).on('keydown', function() {
  return false;
});




$('#calc1Increase, #calc1Decrease').click(function() {
  var el = $(this).parent().children('input');

  if( $(this).is('#calc1Increase') && el.data('min') >= el.val() ) {
    return false;
  }

  var i = ( $(this).is('#calc1Increase') ) ? +el.val() - 1 : +el.val() + 1;
  el.val(i);
  runCalc();
});

function gettomorrowdate() {
  return moment().add('days', 1).format('YYYY-MM-DD');
}

$('#pages').on('keyup', function() {
    var str = $(this).val(),
        reg = /[^0-9]/gi;

    str = str.replace(reg, '');
    $(this).val(str);
    runCalc();
}).blur(function() {
    if( !$(this).val() ) {
        $(this).val( $(this).data('default') );
    }
});

var urgencyData = [43200, 86400, 86400 * 2, 86400 * 3, 86400 * 5, 86400 * 7, 86400 * 9, 86400 * 10],
        $prc_data = [];



    function runCalc() {
        academicLevel = $("#calc1AcadLevel").val();
        pages = $('#pagesLength').val();
        deadline = moment(  $("#calc1Calendar").val() );
        spaced = 2;
        typeOfWork = 1;
        if (academicLevel >= 0 && pages > 0 && deadline) {
            var res = orderCalc(academicLevel, deadline, pages, typeOfWork, spaced).toFixed(2);
            $('#totalPrice i').html(res);
        }
    };

    function setPagesCount(inputValue, pagesCount) {
        var wordsCount = 300;
        if ($("[name=spaced]:checked").val() == 1) {
            wordsCount = 600;
        }

        $("#words").html(wordsCount * inputValue + " words");
    }

    function getUrgency(deadline) {
        var time = +new Date(deadline).getTime(),
          urgency = 0,
          urgencyLength = urgencyData.length - 1;

        time2 = +new Date().getTime();
        time = (time - (+new Date)) / 1000;
        time = (time < 0) ? 0 : time;

        if (time > urgencyData[urgencyLength]) {
            urgency = urgencyLength;
        }
        else {
            $.each(urgencyData, function (key, value) {
                if (time < value) {
                    urgency = parseInt(key);
                    return false;
                }
            });
        }
        return urgency;
    }

  function orderCalc(level, deadline, pages, typeOfWork, spaced) {
      var urgency, totalPrice, new_urgency, new_typeOfWork;

      urgency = getUrgency(deadline);
          new_urgency=urgency;

      if (spaced == 1) {
          totalPrice *= 2;
      }
      if (urgency == 4) new_urgency=5;
      if (urgency == 5) new_urgency=7;
      if (urgency == 6) new_urgency=9;
      if (urgency == 7) new_urgency=30;
      if (typeOfWork == 2) new_typeOfWork=1;
      if (typeOfWork == 1) new_typeOfWork=2;
      if (typeOfWork == 3) {new_typeOfWork=3; spaced=2;}

      totalPrice=(PrcWrk(level, new_urgency, pages, new_typeOfWork))*(PrcSpace(spaced));
      return totalPrice;
  };

  function GetListPrise () {
      var data = {};
      data['price_on_date'] = moment().format('YYYY-MM-DD');
      $.ajax({
          url: '/utils',
          type: 'POST',
          async: false,
          data: JSON.stringify(data),
          contentType: 'application/json;charset=UTF-8',
          success: function(datarecived){
              $prc_data=datarecived;
          },
          error: function(error) {
          }
      });
  };

  GetListPrise();
  runCalc();

  function PrcWrk(level, deadline, pages, typeOfWork) {
      if ( !jQuery.isEmptyObject($prc_data) ) {
          for ( var i=0; i<$prc_data.result.length; i++ ){
              if ( ($prc_data.result[i].id_table == typeOfWork) && ($prc_data.result[i].format == level) && ($prc_data.result[i].urgenc == deadline) ) {
                  return pages*$prc_data.result[i].price;
              }
          }
      }
      return 0;
  }

  function PrcSpace (space) {
      if ( !jQuery.isEmptyObject($prc_data) ) {
          for ( var i=0; i<$prc_data.result2.length; i++ ) {
              if( $prc_data.result2[i].countspace == space ) {
                  return $prc_data.result2[i].kof;
              }
          }
      }
      return 1;
  }
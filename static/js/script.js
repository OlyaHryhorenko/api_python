var reg_valid = {
  'email': /^([a-z0-9_\.-]+)@([a-z0-9_\.-]+)\.([a-z\.]{2,6})$/,
  'password': /^[\w_]{4,18}$/
},
current_mobile_sample = 2;
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
function animateNav(btn, items, status) {
	var delay = 0;

	$(items).each(function() {
		var t = $(this);
		setTimeout(function() {
			if(status) {
				t.addClass('opened-item');
			}else{
				t.removeClass('opened-item');
			}
		}, delay);
		delay += 50;
	});

	if(status) {
		btn.addClass('open').parents('#glob-header').addClass('open-menu');
	}else{
		setTimeout(function() {
			btn.removeClass('open').parents('#glob-header').removeClass('open-menu');
		}, delay);
	}
}



$(function() {
  if(!isMobile.any()) {
    addImgForDesktop();
  }
  $('.dublicate-link').click(function() {
    location.pathname = $(this).parents('.post-item').find('footer').find('a').attr('href');
  });
  $(window).on('scroll', function() {
    var scrolled = window.pageYOffset || document.documentElement.scrollTop;

    if(scrolled > 50) {
      if( $('#fixed-header').is('.main-header') ) {
        $('#fixed-header').find('.header-logo').css({'opacity' : 1});
      }
      $('#fixed-header').addClass('opened');
    }else{
      if( $('#fixed-header').is('.main-header') ) {
        $('#fixed-header').find('.header-logo').css({'opacity' : 0});
      }
      $('#fixed-header').removeClass('opened');
    }
  });
  $(window).trigger('scroll');
  $('.anchor-link').click(function(e){
    e.preventDefault();

    var attr = $(this).attr('href'),
      el = attr.split('#'),
      pathname = attr.replace("#"+el[1], ''),
      margin = '';

    if(location.pathname == pathname){
      
    }else{
      location.href = attr;
      return false;
    }
    animateScroll("#" + el[1]);
  });

  $('.glob-toogle').click(function() {
    var cur = ( $(this).is('.open') ) ? false: true,
      navigationCont = ['#glob-header .header-nav li', '#glob-header .glob-contact a'];

    for(var key in navigationCont) {
      animateNav( $(this), navigationCont[key], cur );
    }

    return false;
  });

  

  $('.menu-container').each(function() {
    $(this).find('a').each(function() {
      if($(this).attr('href') == location.pathname) {
        $(this).parent('li').addClass('active-page');
      }
    });
  });

  $('.sub-menu-info').on('click', function() {
    var parent = $(this).parents('.sub-menu-container');
    if(parent.is('.open')) {
      parent.removeClass('open');
      return false;
    }else{
      parent.addClass('open');
      $('html').addClass('menu-hidden').attr('data-clicked', $(this).attr('id'));
      return false;
    }
  });

  $('html').on('click', function() {
    if( $('html').is('.menu-hidden') ) {
      $('#' + $('html').attr('data-clicked')).trigger('click');

      $('html').removeClass('menu-hidden');
      if(!$(this).is('a')) {
       
      }
    }
  });

  samplesHeight();
  fixFooter('#glob-footer');

  $(window).resize(function() {
    samplesHeight();
    fixFooter('#glob-footer');

    if($(window).width() <= 750) {
      current_mobile_sample = 1;
      $('#glob-samples .samples_header .slider-view:not("#active-samples-view")').trigger('click');
    }else{
      current_mobile_sample = 2;
      $('#glob-samples .samples_header .grid-view:not("#active-samples-view")').trigger('click');
    }

  });

  $('#log-in-button').click(function (event) {
      event.preventDefault();

      $('#global-modal input').each(function() {
        checkLoginOnvalid($(this));
      });

      var form = $(this).parents('form');
      if ( !$('#global-modal input.unsend').length ) {
        $.post(form.attr('action'), form.serialize(), function (data) {
          if (data == '1') {
            form.addClass('invalid');
          } else {
            document.location.pathname = '/dashboard';
          }
        });
      }else{
        $('#global-modal form').addClass('invalid');
      }
  });

  $('#global-modal input').blur(function() {
      checkLoginOnvalid($(this));
    }).each(function() {
      if(!$(this).val()) {
        $(this).addClass('unsend');
      }
    });

  $('#global-login, .footer-button').click(modalWindow);
});


$(function() {
  $('.glob-contact a.chat').click(function(event){
    event.preventDefault();
    $zopim(function(){
      $zopim.livechat.window.show();
    });
  });

  setTimeout(function() {
    if($(window).width() >= 750) {
      $('.glob-toogle').trigger('click');
    }
  },  1000);


  parseFaq();

  $('.glob-faqs .question').click(function() {
    if($(this).parent('.faq-item').is('.open')) {
      return false;
    }

    $('.faq-item').removeClass('open').find('.answer').slideUp(200);
    $(this).parent('.faq-item').addClass('open').find('.answer').slideDown(200);
  });

  $('#glob-samples .samples_header .control-samples-view').click(function() {
    if($(this).is('#active-samples-view')) {
      return false;
    }

    var samplesLength = $('#glob-samples .samples-item');

    if($(this).data('to') == 'slider-samples-list') {
      var samplesLength = $('#glob-samples .samples-item'),
          i = (samplesLength.length / 2);

      samplesLength.each(function() {
        $(this).css({'zIndex' :  (samplesLength.length - $(this).index()) });
      });
      
      var interval = setInterval(function() {
        if(i > 1) {
          samplesLength.eq(i * 2 - 1).addClass('hidden').css({
            'marginTop' : -( samplesLength.eq(i * 2 - 1).height() + 2 )
          }).prev('.samples-item').addClass('hidden').css({
            'marginTop' : -( samplesLength.eq(i * 2 - 1).height() + 2 )
          });

          i--;
        }else{
          clearInterval(interval);

          sliderOn(samplesLength);
        }
      }, 200);
      
    }else{
      $('#glob-samples').css({'overflow' : 'hidden'});
      $('#glob-samples .samples_header').css({'zIndex' : 102, 'position' : 'relative'});

      setTimeout(function() {
        sliderOff(samplesLength);
      }, 50);
      
    }

    $('#glob-samples .samples-list').removeClass( $('#active-samples-view').data('to') );
    $('#glob-samples .samples_header .control-samples-view').removeAttr('id');
    $(this).attr('id', 'active-samples-view');
    $('#glob-samples .samples-list').addClass( $(this).data('to') );
  });

  if($(window).width() <= 750) {
    current_mobile_sample = 1;
    $('#glob-samples .samples_header .slider-view').trigger('click');
  }else{
    current_mobile_sample = 2;
    $('#glob-samples .samples_header .grid-view:not("#active-samples-view")').trigger('click');
  }

});

function sliderOn(item) {
  if(current_mobile_sample == 2) {
    item.not( item.eq(0) ).not(item.eq(1)).hide(0);  
  }else{
    item.not( item.eq(0) ).hide(0);
  }
  
  item.removeClass('hidden').css({'marginTop' : 0});

  var markerCont = $('#samples-marker'),
      slideId = '';

  if(!markerCont.find('button').length) {
    for (var i = 0; i < (item.length / current_mobile_sample); i++) {
      if(i == 0) {
        markerCont.append('<button id="act-btn">');  
      }else{
        markerCont.append('<button>');
      }
    }
  }
  $('#samples-marker button').on('click', markerEvent).removeAttr('id').eq(0).attr('id', 'act-btn');
  markerCont.slideDown(300);
  $('#glob-samples .samples-item').css({'zIndex' : 1});
  $('.hidden-for-animation').each(function(e) {
      var top = $(this).css('top').replace(/[^0-9]/g, ''),
          offset = $(this).offset().top,
          key = (top) ? offset - top : offset;

      offsetTop[key] = $(this);
    });
}

function markerEvent() {
  var id = $(this).index();

  if( $(this).is('#act-btn') ) {
    return false;
  }

  $('#glob-samples .samples-item').addClass('rotate-hidden');
  var next = '',
      animateSpeed = parseFloat( $('#glob-samples .samples-item.rotate-hidden').css('transitionDuration').replace('s', '') ) * 1000;

  switch(id) {
    case 0 : 
      if(current_mobile_sample == 2) {
        next = $('#glob-samples .samples-item:eq('+0+'), #glob-samples .samples-item:eq('+1+')');
      }else{
        next = $('#glob-samples .samples-item:eq('+id+')');
      }
      break;
    case 1 : 
      if(current_mobile_sample == 2) {
        next = $('#glob-samples .samples-item:eq('+2+'), #glob-samples .samples-item:eq('+3+')');
      }else{
        next = $('#glob-samples .samples-item:eq('+id+')');
      }
      break;
    case 2 :
      if(current_mobile_sample == 2) {
        next = $('#glob-samples .samples-item:eq('+4+'), #glob-samples .samples-item:eq('+5+')');
      }else{
        next = $('#glob-samples .samples-item:eq('+id+')');
      }
      break;
    default : 
      next = $('#glob-samples .samples-item:eq('+id+')');
      break;
  }

  setTimeout(function() {
    $('#glob-samples .samples-item').hide(0);
    next.show(0).removeClass('rotate-hidden');
  }, animateSpeed);

  $('#samples-marker button').removeAttr('id');
  $(this).attr('id', 'act-btn');
}

function sliderOff(item) {
  var item = $('#glob-samples .samples-item'),
      animateSpeed = parseFloat( $('#glob-samples .samples-item').css('transitionDuration').replace('s', '') ) * 1000,
      i = item.length;

  item.removeClass('rotate-hidden').css({'zIndex' : 99});  

  $('#samples-marker').slideUp(300).children('button').off('off');


  item.each(function() {
    if( $(this).css('display') == 'none' ) {
      $(this).css({'marginTop' : - $(this).height(), 'zIndex' : 0}).slideDown(100, function() {
        $(this).css({'marginTop' : 0});
      });
    }
  });

  setTimeout(function() {
    $('#glob-samples .samples-item').css({'zIndex' : 1});
    $('#glob-samples').css({'overflow' : 'visible'});
    $('#glob-samples .samples_header').css({'zIndex' : 1, 'position' : 'static'});
  }, animateSpeed * 2);
  
  $('.hidden-for-animation').each(function(e) {
      var top = $(this).css('top').replace(/[^0-9]/g, ''),
          offset = $(this).offset().top,
          key = (top) ? offset - top : offset;

      offsetTop[key] = $(this);
    });
}

var chatColor = '#000000';

window.$zopim||(function(d,s){
    var z = $zopim = function(c) {
        z._.push(c);
    },
    $ = z.s = d.createElement(s),
    e = d.getElementsByTagName(s)[0];
    z.set = function(o) {
        z.set._.push(o);
    };
    z._ = [];
    z.set._ = [];
    $.async =! 0;
    $.setAttribute("charset","utf-8");
    $.src = "//v2.zopim.com/?4v4bzZ5oAmwMWZJohG2uLy6LDejcKugP";
    z.t =+ new Date;
    $.type = "text/javascript";
    e.parentNode.insertBefore($,e)
})(document,"script");

$zopim(function() {
   $zopim.livechat.window.hide();
   $zopim.livechat.theme.setTheme('simple')
   $zopim.livechat.theme.setColor(chatColor);
    $zopim.livechat.theme.reload();
    $zopim.livechat.window.setTitle('Support');
});

function animateScroll(el) {
  el = (el) ? el : location.hash;
  var obj = $(el);
  
  if(!obj.length) {
    return false;
  }
   console.log(obj);
  console.log(obj.offset().top);

  $('body,html').animate({
      scrollTop: obj.offset().top
  }, 1500);
}

var pagesFooterFix = ['/forgot', '/dashboard', '/orderinfo', '/profile', '/transaction', '/blog'];
function fixFooter(to) {
  var el = $(to),
      htmlCss,
      elCss,
      height = el.outerHeight(true);

    for (var i = 0; i > pagesFooterFix.length; i++) {
      if( pagesFooterFix[i] == location.pathname ) {
        return false;
      }
    }
    
  if( $(window).width() < 850 ) {
    htmlCss = {
      'paddingBottom' : 0
    };
    elCss = {
      'position' : 'static'
    }
  }else{
    htmlCss = {
      'paddingBottom' : (height),
      'position' : 'relative',
      'minHeight' : '100%',
      '-webkit-box-sizing' : 'border-box',
      '-moz-box-sizing' : 'border-box',
      '-webkit-box-sizing' : 'border-box',
      'box-sizing' : 'border-box'
    };
    elCss = {
      'position' : 'absolute',
      'left' : 0,
      'right' : 0,
      'bottom' : 0
    };
  }

  $('html').css(htmlCss);
  el.css(elCss);
}

function modalWindow(event) {
  event.preventDefault();
  $('#global-modal').addClass('open');

  $('html').on('keyup', function (event) {
    if (event.keyCode === 27) {
      closeModal();
      return false;
    }
  });

  $('.bg-modal, .modal .close').click(function () {
    closeModal();
  });
}

function closeModal() {
  $('.modal').removeClass('open');
  $('html').off('keyup');
}

function samplesHeight() {
  $('#glob-samples .samples-list .samples-item').each(function() {
   
    $(this).height($(this).width());
  });
  $('.samples-preload').removeClass('samples-preload');
}

function parseFaq() {
  var faqContent = $('#hidden-faq li'),
      example = $('#faq-example').html();
 
  if(!faqContent.length) {
    return false;
  }

  faqContent.each(function() {
    var w = $(this).html(),
        id = $(this).index();
    
    w = w.split('/-/');
    var appExample = example.replace(/\/\/\\(.*?)\\\/\//gim, function(match, contents) {
      var out = '';
      switch(contents) {
        case 'id' :
          out = ++id;
          break;
        case 'question' : 
          out = w[0];
          break;
        case 'answer' :
          out = w[1];
          break;
        case 'open' :
          out = (id == 0) ? 'open' : '';
          break;
      } 
      return out;
    });
    delete appExample;
    $('.glob-faqs .faq-container').append(appExample);
  });
  delete faqContent, example;
}

function checkLoginOnvalid(el) {
  if( reg_valid[el.attr('type')].test(el.val()) ) {
    el.removeClass('unsend invalid');
  }else{
    el.addClass('invalid');
  }
}

function addImgForDesktop() {
  $('#glob-header .glob-first-screen .left_first').html('<img src="/static/img/globals1.png" alt="" />');
  $('#glob-bg-desctop').prepend('<img src="/static/img/bg-glob.jpg" alt="" id="bg-header" />');
}
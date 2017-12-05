$.fn.customSlider = function(el) {

	this.each(function() {
		var defaultParams = {
			speed : 1000,
			delay : 3000,
			style : "slide",
			auto : false,
			autoDelay : 1000,
			control : true
		},
		DOC = document,
		userParams;

		if(el && Object.keys(el).length) {
			userParams = el;
		}else{
			userParams = $(this).data();
		}

		if(!Object.keys(userParams).length) {
			console.error( 'Please select params for: ' + $(this).attr('class') + '; index: ' + ($(this).index() + 1) );
			return false;
		}

		for( var key in userParams ) {
			defaultParams[key] = userParams[key];
		}
		var t = $(this),
			getlengthOnSlide = function() {
				var w = $(window).width(),
					ret = (w < 1020) ? (w < 750) ? 1 : 2 : (defaultParams['max']) ? +defaultParams['max'] : 3;
					console.log();
				return ret;
			},
			items = t.find('[data-item]');
			var markerCont;
			if( t.find('[data-marker]').length ) {
				markerCont = t.find('[data-marker]');

			}else{
				$('<div/>', {
					class : 'allSlider-hidden',
					style : "display: none!important;"
				}).appendTo(t);
				markerCont = $('.allSlider-hidden');
			}

		var bgSlider = t.find('[data-bg]'),
			controlls = t.find('[data-controll]'),
			current_animate = true,
			autoSlide = function() {
				controlls.filter('[data-next]').trigger('click');
			},
			hidden = t.find('[data-hidden]'),
			slideAnimate = function() {
				if(!current_animate) {
					return false;
				}
				current_animate = false;
				var items = t.find('[data-item]'),
					w = items.width();
				console.log(w + (+items.css('marginRight').replace('px', '')));
				if( $(this).is('[data-next]') ) {
					bgSlider.animate({
						'marginLeft' : -(w + (+items.css('marginRight').replace('px', '')) )
					}, defaultParams.speed, function() {
						items.eq(0).appendTo(bgSlider);
						current_animate = true;
						$(this).css({
							'marginLeft' : 0
						});
					});
				}else{
					items.eq(-1).prependTo(bgSlider);

					bgSlider.css({
						'marginLeft' : -(w + (+items.css('marginRight').replace('px', '')) )
					}).animate({
						'marginLeft' : 0
					}, defaultParams.speed, function() {
						current_animate = true;
					});
				}

				if(defaultParams.auto == true) {
					autoSlideFun = setInterval(autoSlide, defaultParams.delay);
				}

			},
			changeWidth = function() {
				var w = hidden.width() / getlengthOnSlide();
				items.width( Math.floor( w - (items.css('marginRight').replace('px', '') * 2) ) );
				bgSlider.width( items.length * w + (items.css('marginRight').replace('px', '') * 2 * items.length) );
			}

		switch(defaultParams.style) {
			case 'slide' :
				controlls.on('click', slideAnimate);
				changeWidth();
				$(window).resize(changeWidth);
				break;
			case 'fade' :
				items.fadeOut(0).eq(0).fadeIn(0);
				controlls.on('click', function() {
					clearInterval(autoSlideFun);
					var cur = t.find('.active-item'),
						next = ( $(this).is('[data-next]') ) ? ( cur.next().length ) ? cur.next() : items.eq(0) : ( cur.prev().length ) ? cur.prev() : items.eq(-1);
					markerCont.children(markerTag).eq(next.index()).trigger('click');

				});
				break;
		}

		var markerParams = ( markerCont.data() ) ? markerCont.data() : {},
			markerTag = ( markerParams['btntag'] ) ? markerParams['btntag'] : 'button',
			autoSlideFun,
			acMarkerId = ( markerParams['act'] ) ? markerParams['act'] : ( 'active-slide-marker' + t.index() ),
			fadeAnimate = function(index, callback) {
				items.css({
					'position' : 'absolute',
					'top' : 0
				});
				items.fadeOut(defaultParams).removeClass('active-item').eq(index).css({'position' : 'relative'}).fadeIn(defaultParams).addClass('active-item');
				if(callback) {
					callback();
				}
			},

			markerEvent = function(e) {
				console.log(current_animate);
				e.preventDefault();
				var el = $(this);
				if( el.is( '#' +acMarkerId ) ) {
					return false;
				}
				if(!current_animate) {
					return false;
				}

				current_animate = false;

				switch(defaultParams.style) {
					case 'slide' :
						slideAnimate(function() {
							if(defaultParams.auto == true) {
								autoSlideFun = setInterval(autoSlide, defaultParams.delay);
							}
						});
						break;
					case 'fade' :
						clearInterval(autoSlideFun);
						fadeAnimate( el.index(), function() {

							markerCont.children(markerTag).removeAttr('id', acMarkerId);
							el.attr('id', acMarkerId);
							if(defaultParams.auto == true) {
								autoSlideFun = setInterval(autoSlide, defaultParams.delay);
								current_animate = true;
							}

						});
						break;
					default :
						slideAnimate(function() {
							if(defaultParams.auto == true) {
								autoSlideFun = setInterval(autoSlide, defaultParams.delay);
							}
						});
						console.error('animate method: ' + defaultParams.style + '; Not found. Defaul animate "slide". Please use: "slide" or "fade"');
				}
				current_animate = true;
				//if(defaultParams.style== ) 

			};


		items.each(function() {
			var btnParam;
			if( !$(this).index() ) {
				$(this).addClass('active-item');
				btnParam = {
					class : markerCont.data('class'),
					id : acMarkerId
				}
			}else{
				btnParam = {
					class : markerCont.data('class')
				}
			}
			$('<'+markerTag+'/>', btnParam).bind('click', markerEvent).appendTo(markerCont);
		});

		if(defaultParams.auto == true) {
			autoSlideFun = setInterval(autoSlide, defaultParams.delay);
		}
	});
};
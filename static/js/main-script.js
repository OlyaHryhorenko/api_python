
var slideIndex=1;
showSlides(slideIndex);




function currentSlide(n){
	showSlides(slideIndex = n);
}

function showSlides(n){
	var i;
	var slides = $(".slide-part");
	var dots = $(".dot");

	for(i=0; i<slides.length; i++){
		slides[i].style.display = "none";
	}
	for(i=0; i < dots.length; i++){
		dots[i].className = dots[i].className.replace("act-dot","");
	}
	slides[slideIndex-1].style.display = "block";
	dots[slideIndex-1].className+= " act-dot";
}


	new WOW().init();



$(document).ready(function(){
	$(".read-more").click(function(){


		$('.read-more').not(this).removeClass('act-more');
		$(this).toggleClass('act-more');



	//$('.span-p').text('+');


	if($('.more-p',this).text() == 'Read More') {
		$('.more-p').not(this).text('Read More');
		$('.more-p',this).text('Less');
	} else {
		$('.more-p',this).text('Read More');
	}

	if($('.span-p',this).text() == '+') {
		$('.span-p').not(this).text('+');
		$('.span-p',this).text('-');
	} else {
		$('.span-p',this).text('+');
	}






	$('.read-more').not(this).siblings().removeClass("standart-text-open");
	$(this).siblings().toggleClass("standart-text-open");




});
});

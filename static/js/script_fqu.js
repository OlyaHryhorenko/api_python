$(document).ready(function(){
	$('.accardeon dd').hide().prev().click(function(){
		$('.accardeon dd').not(this).slideUp();
		$(this).next().not(":visible").slideDown();
	});
});

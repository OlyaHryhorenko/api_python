$(document).ready(function(){
	$('.sample').each(function(i) {
		$(this).delay((i++) * 500).fadeTo(400, 1);
	});
});

$(document).ready(function(){
	$(".tab_item").not(":first").hide();
	$(".wrapper .tab").not(":last").addClass("act");
		$(".wrapper .tab").click(function() {
		$(".wrapper .tab").removeClass("act").eq($(this).index()).addClass("act");
		$(".tab_item").hide().eq($(this).index()).fadeIn()
	});
});	
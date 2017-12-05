
$(document).ready(function(){
	$(".tab_item").not(":first").hide();
	$(".tab_suere").not(":last").show();
		$(".wrapper .tab").click(function() {
		/*$(".wrapper .tab").removeClass("act").eq($(this).index()).addClass("act");*/
		$(".tab_item").hide().eq($(this).index()).fadeIn()
		$(".tab_suere").removeClass("act").eq($(this).index()).addClass("act");
	})/*.eq(0).addClass("act")*/;
});	
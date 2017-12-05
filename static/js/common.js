$(document).ready(function(){
 
//Datepicker
//$("#date_input").pickadate();
//


//Count in forms
 $("#pages_counter .set").click(function(){
 	 var inp = $("#pages_num");
   var inp_val = $(inp).val();
   if(inp_val <= 1 && $(this).hasClass("minus")){
   	return true;
   }
   if($(this).hasClass("plus")){
   	inp_val++;
   	$(inp).val(inp_val);
   }
   else if($(this).hasClass("minus")){
   	inp_val--;
   	$(inp).val(inp_val);
   }
 });
 $("#source_counter .set").click(function(){
 	 var inp = $("#source_num");
   var inp_val = $(inp).val();
   if(inp_val <= 1 && $(this).hasClass("minus")){
   	return true;
   }
   if($(this).hasClass("plus")){
   	inp_val++;
   	$(inp).val(inp_val);
   }
   else if($(this).hasClass("minus")){
   	inp_val--;
   	$(inp).val(inp_val);
   }
 });
 //


 //More text
 $(".home_third .more").click(function(e){
 	e.preventDefault();
 	$(this).toggleClass("active").prev().toggleClass("active");
 	if($(this).hasClass("active")){
 		$(this).html("hide");
 	}
 	else if(!$(this).hasClass("active")){
 		$(this).html("more");
 	}
 });
 //


 //mobile menu
 $("#mobile_menu_toggler").click(function(){
 	$(this).toggleClass("is-active");
 	$("header .top > div.menu_wrap .site_menu").slideToggle(700);
 })
 //



}); //end doc ready
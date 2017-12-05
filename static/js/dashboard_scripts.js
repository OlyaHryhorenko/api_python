$(function(){
    $("[data-dismiss]").on("click", function(){
        $(this).closest("." + $(this).attr("data-dismiss")).hide();
        return false;
    });
});

//Fucking wraperr for work this block code!
( function($) {

$(document).ready(function() {
		$('#load_content').hide();

	var Example = (function() {
        "use strict";

        var elem,
            hideHandler,
            that = {};

        that.init = function(options) {
            elem = $(options.selector);
        };

        that.show = function(text) {
            clearTimeout(hideHandler);

            elem.find("span").html(text);
            elem.delay(200).fadeIn().delay(4000).fadeOut();
        };

        return that;
    }());

    $(function () {
            Example.init({
                "selector": ".bb-alert"
            });
        });

		$(document).on('click','.paypalbutton',function(){
			var targ=$(this).parent().parent().find('#id_ord2').text();
		    var data = {}; // data

	            data['price'] = parseFloat($(this).parent().parent().find('#sum_ord2').text().replace(/[^0-9\.]+/g, ""));
			    data['id'] = $(this).parent().parent().find('#id_ord2').text();
			    if (parseFloat($(this).parent().parent().find('#typeWork2').text()) == 1) {
			             data['variant'] = "Writing from scratch";
			         }
			         else {
			             data['variant'] = "Editing";
			         }
			    data['category'] = $(this).parent().parent().find('#assigmenttype2').text();
			    data['name'] = $(this).parent().parent().find('#title2').text();
			    data['brand'] = $(this).parent().parent().find('#paperformat2').text();
			    data['coupon'] =$(this).parent().parent().find('#coupon2').text();
                //console.log(data);
	        SendYandMetrik(targ,data);
		 });

	$('#bt_rev.revision').click(function() {
        var box = bootbox.dialog({
                        title: "Submit for Revision.",
                        message: '<div class="row">  ' +
                                    '<div class="col-md-12"> ' +
                                        '<form class="form-horizontal" id="claimform"> ' +
                                            '<div class="form-group"> ' +
                                                '<label class="col-md-4 control-label">Select Category</label> ' +
                                                '<div class="col-md-8"> ' +
                                                    '<div class="btn-group" data-toggle="buttons"> '+
                                                        '<label class="btn btn-warning btn-sm chkbtn"> '+
                                                            '<input name="selcat2" type="checkbox" autocomplete="off" value="My insructions were not met"> My insructions were not met '+
                                                        '</label> '+
                                                        '<label class="btn btn-warning btn-sm chkbtn"> '+
                                                            '<input name="selcat2" type="checkbox" autocomplete="off" value="Language issues"> Language issues '+
                                                        '</label> '+
                                                        '<label class="btn btn-warning btn-sm chkbtn"> '+
                                                            '<input name="selcat2" type="checkbox" autocomplete="off" value="Plagiarism"> Plagiarism '+
                                                        '</label> '+
                                                        '<label class="btn btn-warning btn-sm chkbtn"> '+
                                                            '<input name="selcat2" type="checkbox" autocomplete="off" value="Incorrect format"> Incorrect format '+
                                                        '</label> '+
                                                        '<label class="btn btn-warning btn-sm chkbtn"> '+
                                                            '<input name="selcat2" type="checkbox" autocomplete="off" value="Poor content quality"> Poor content quality '+
                                                        '</label> '+
                                                        '<label class="btn btn-warning btn-sm chkbtn"> '+
                                                            '<input name="selcat2" type="checkbox" autocomplete="off" value="Other"> Other '+
                                                        '</label> '+
                                                    '</div> ' +
                                                '</div> ' +
                                            '</div> ' +

                                            '<div class="form-group info_label" title="How much do you expect the paper to change after the revision?"> ' +
                                                '<label class="col-md-4 control-label">My paper must be:</label> ' +
                                                '<div class="col-md-8"> ' +
                                                    '<div class="btn-group" data-toggle="buttons"> '+
                                                        '<label class="btn btn-info btn-sm chkbtn"> '+
                                                            '<input name="aftrerrevision" type="radio" autocomplete="off" value="Slightly adjusted"> Slightly adjusted '+
                                                        '</label> '+
                                                        '<label class="btn btn-info btn-sm chkbtn active"> '+
                                                            '<input name="aftrerrevision" type="radio" checked autocomplete="off" value="Corrected here and there"> Corrected here and there '+
                                                        '</label> '+
                                                        '<label class="btn btn-info btn-sm chkbtn"> '+
                                                            '<input name="aftrerrevision" type="radio" autocomplete="off" value="Changed substantially"> Changed substantially '+
                                                        '</label> '+
                                                        '<label class="btn btn-info btn-sm chkbtn"> '+
                                                            '<input name="aftrerrevision" type="radio" autocomplete="off" value="Redone"> Redone '+
                                                        '</label> '+
                                                    '</div> ' +
                                                '</div> ' +
                                            '</div> ' +

                                            '<!-- <div class="form-group"> ' +
                                                '<label class="col-md-4 control-label">Select Category</label> ' +
                                                '<div class="col-md-8"> ' +
                                                    '<select class="form-control" id="selcat" name="selcat"> '+
                                                        '<option>Incorrect Format</option> '+
                                                        '<option>Plagiarism</option> '+
                                                        '<option>Poor content quality</option> '+
                                                        '<option>Language issues</option> '+
                                                        '<option>Other</option> '+
                                                    '</select> '+
                                                '</div> ' +
                                            '</div> -->' +
                                            '<div class="form-group"> '+
                                                '<label class="col-md-4 control-label">Please, describe your claim in detail:</label> '+
                                                '<div class="col-md-8"> ' +
                                                    '<textarea class="form-control" rows="10" id="describeproblem" name="describeproblem" required></textarea> '+
                                                '</div> '+
                                            '</div> '+
                                            '<div class="form-group"> '+
                                                '<label class="col-md-4 control-label">Attach Files</label> '+
                                                '<div class="col-md-8"> ' +
                                                    '<input id="inputfl" type="file" class="file" multiple data-show-preview="false" name="inputfl[]"> '+
                                                '</div> '+
                                            '</div> '+
                                        '</form> '+
                                    '</div>  '+
                                '</div>',
                        buttons: {
                            success: {
                                label: "Submit",
                                className: "btn-success",
                                callback: function () {
                                    if( $("#describeproblem").val().length === 0 ) 
                                    {
                                        Example.show("Please, let us know what exactly is wrong with the paper you received!");
                                        return false;
                                    }
                                    else
                                    {
                                        $('#load_content').show();
                                        var FormData1 = new FormData($('#claimform')[0]);
    									FormData1.append('idorder',$(this).parent().parent().find('#id_ord2').text());
                                        console.log(FormData1);
                                        //alert("Hello " + name + ". You've chosen <b>" + answer + "</b>");
                                        $.ajax({
                                                url: "/utils",
                                                type: "POST",
                                                data:  FormData1,
                                                contentType: false,
                                                cache: false,
                                                processData:false,
                                                success: function(data){
                                                    $('#load_content').hide();
                                                    ExampleSuccess.show("Your revision request has been succesfully submitted.");
                                                },
                                                beforeSend: function(){
                                                    $('#load_content').hide();
                                                    Example.show("Your revision request is being processed.");
                                                },
                                                error: function() {
                                                    $('#load_content').hide();
                                                    ExampleDanger.show("Oops something went wrong... Please contact us via email or live chat for resolution.");
                                                }
                                           });
                                    }
                                }
                            },
                            cancel: {
                                label: "Cancel",
                                className: "btn-default",
                                callback: function () {
                                    //var name = $('#selcat').val();
                                    //var answer = $('#describeproblem').val()
                                    //var fl = $('#inputfl').val()
                                    //alert("Hello " + name + ". You've chosen <b>" + answer + "</b>");
                                    console.log($(this).parent().parent().find('#id_ord2').text());
                                    Example.show("Revision request has been canceled.");
                                }
                            }
                        }
                    }
                );
        box.on("shown.bs.modal", function() {
            $('#load_content').hide();

            $("#inputfl").fileinput({
                showUpload: false
            });

            $('.info_label').tooltip({
                animation: true,
                placement: 'bottom',
                container: 'body'}).on('shown.bs.tooltip', function (e) {
                    var trg = e.target
                    if('ontouchstart' in window)
                    {
                        setTimeout(function() {
                            $(trg).tooltip('hide');
                        }, 3000);
                    }
                });
        });
    });

		if (getParameterByName("ppec", $.url())){
			if (parseFloat(getParameterByName("ppec", $.url())) > 0)
			{
				var data = {}; // data
	            data['ppe'] = getParameterByName("ppec", $.url());

		        $.ajax({
		            url: "/utils",
		            type: "POST",
		            data: JSON.stringify(data),
		            contentType: "application/json",
		            dataType: 'json',
		            success: function(data){
		                var long_msg=data.result;
		                //console.log(data);
		                if ($.isEmptyObject(long_msg)) long_msg='Some errors occurred! Please contact customer support!';
		                var err_pp__pg = bootbox.alert('<div class="row"> ' +
						                        '<div class="col-sm-12"> '+
													'<h1 style="font-size: 1em;">PayPal Error</h1> '+
												'</div> '+
												'<hr> '+
											  '</div> '+
											  	'<br> '+
											  '<div class="row"> ' +
												'<div class="col-sm-12" style="text-align: center;"> '+
												' <b>'+long_msg+'</b> '+
												'</div> '+
											  '</div> '
								, function() {
								  
								});
		               
						$('#load_content').hide();
		            },
		            complete: function(err) {
		            	$('#load_content').hide();
		            },
		            error: function(err) {
		            	$('#load_content').hide();
		                //Example.show("Oops something wrong... Please contact with us by email!");
		            }
		        });
	    	}
	    	else
	    	{
	    		var err_pp__pg = bootbox.alert('<div class="row"> ' +
						                        '<div class="col-sm-12"> '+
													'<h1 style="font-size: 1em;">PayPal Error</h1> '+
												'</div> '+
												'<hr> '+
											  '</div> '+
											  	'<br> '+
											  '<div class="row"> ' +
												'<div class="col-sm-12" style="text-align: center;"> '+
												' <b>Some errors occurred! Please contact customer support!</b> '+
												'</div> '+
											  '</div> '
								, function() {
								  
								});
	    	}
		}


		if (getParameterByName("orderid", $.url()))
		{
			var show_windows_thnks=0;
			var data1 = {}; // data
            data1['id'] = getParameterByName("orderid", $.url());
            data1['getpriceorder'] = 1;

		        $.ajax({
		            url: "/utils",
		            type: "POST",
		            data: JSON.stringify(data1),
		            contentType: "application/json",
		            dataType: 'json',
		            success: function(data){
		                var status_order=data.status_order;
		                	//console.log(data);

						    if (data.status_order == 1) {
								var thnks_pg = bootbox.alert('<div class="row"> ' +
										                        '<div class="col-sm-12"> '+
																	'<h1>Order <span class="ord_id"></span></h1> '+
																'</div> '+
															  '</div> '+
															  '<div class="row"> ' +
																'<div class="col-sm-12"> '+
																	'Thank you! Your order <span class="ord_id"></span> - $<span id="sum_ord">0.0</span> has been created. '+
																	'We are ready to start working on your paper as soon as the payment is made. Kindly proceed to PayPal secure page.'+
																	'<span id="typeWork3" class="hide"></span> '+
																	'<span id="paperformat3" class="hide"></span> '+
																	'<span id="coupon3" class="hide"></span> '+
																	'<span id="assigmenttype3" class="hide"></span> '+
																	'<span id="title3" class="hide"></span> '+
																'</div> '+
															  '</div> '+
															  	'<br> '+
															  '<div class="row"> ' +
																'<div class="col-sm-12" style="text-align: center;"> '+
																	'<a href="#" role="button" class="btn btn-orange btn-blockf paypalbutton" id="paypalbutton" target="_blank">Pay now with <span id="textonbutton"></span></a> '+
																	'<div id="textbottombutton">The safer, easier way to pay</div> '+
																'</div> '+
															  '</div> '+
															  '<div class="row"> ' +
																'<div class="col-sm-12" style="text-align: center;"> '+
																	'<a href="#" id="edit_order"><span class="icospan  glyphicon glyphicon-pencil"></span>Edit your order</a> '+
																'</div> '+
															  '</div> '
												, function() {
												  
												});
								thnks_pg.on("shown.bs.modal", function() {
								thnks_pg.attr("id", "thnks_page");
									//console.log(getParameterByName("orderid", $.url()));
									//console.log(getParameterByName("price", $.url()));

								$('#load_content').show();

								$(document).on('click','#paypalbutton',function(){
									var targ=getParameterByName("orderid", $.url());
							        var data = {}; // data
						            data['price'] = $('#sum_ord').text();
						            data['id'] = getParameterByName("orderid", $.url());

								    if (parseFloat($('#typeWork3').text()) == 1) {
								             data['variant'] = "Writing from scratch";
								         }
								         else {
								             data['variant'] = "Editing";
								         }
								    data['category'] = $('#assigmenttype3').text();
								    data['name'] = $('#title3').text();
								    data['brand'] = $('#paperformat3').text();
								    data['coupon'] = $('#coupon3').text();

						            SendYandMetrik(targ,data);
							    });

								var id_ord=getParameterByName("orderid", $.url());
								var prc="0.0";
								$('.ord_id').text(id_ord);
								var data = {}; // data
					            data['id'] = getParameterByName("orderid", $.url());
					            data['getpriceorder'] = 1;

						        $.ajax({
						            url: "/utils",
						            type: "POST",
						            data: JSON.stringify(data),
						            contentType: "application/json",
						            dataType: 'json',
						            success: function(data){
						                prc=data.result;
						                //console.log(data);
						                //console.log("2prc= "+prc);
						                $("#paypalbutton").removeAttr("href");
										$('#paypalbutton').attr('href','/paypal/redirect?orderid='+id_ord);
										$('#sum_ord').text(prc);

										$('#typeWork3').text(data.variant);
										$('#assigmenttype3').text(data.category);
										$('#title3').text(data.name_topic);
										$('#paperformat3').text(data.brand);
										$('#coupon3').text(data.coupon);

										$('#load_content').hide();
						            },
						            complete: function(err) {
						            	$('#load_content').hide();
						            },
						            error: function(err) {
						            	$('#load_content').hide();
						                //Example.show("Oops something wrong... Please contact with us by email!");
						            }
						        });

						        	//console.log("3prc= "+prc);
									$("#edit_order").removeAttr("href");
									$('#edit_order').attr('href','/orderinfo?id='+id_ord+'&edit=1');
								});
							}

		        },
		        complete: function(err) {
		        	$('#load_content').hide();
		        },
		        error: function(err) {
		        	$('#load_content').hide();
		            //Example.show("Oops something wrong... Please contact with us by email!");
		        }
		    });
		}

});

} ) ( jQuery );
	
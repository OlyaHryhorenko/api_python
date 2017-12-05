
$(function(){
    $("[data-dismiss]").on("click", function(){
        $(this).closest("." + $(this).attr("data-dismiss")).hide();
        return false;
    });
});

$(document).ready(function() {
        /**
     * This tiny script just helps us demonstrate
     * what the various example callbacks are doing
     */
     $('#load_content').hide();
     $('#load_content_page').hide();

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

    $('.help_info').tooltip({
                            animation: true,
                            placement: 'bottom',
                            trigger: 'hover',
                            container: 'body'}).on('shown.bs.tooltip', function (e) {
                                var trg = e.target
                                if('ontouchstart' in window)
                                {
                                    setTimeout(function() {
                                        $(trg).tooltip('hide');
                                    }, 3000);
                                }
                            });


    $('#loadingfile').change(
        function(e){
            //console.log(e.currentTarget.files);
            var MaxFileSize=100*1024*1024;
            var errFile=1;
            var numFiles = e.currentTarget.files.length;
            $('#output').empty();
            $('#output').removeClass('MargTop');
                for (i=0;i<numFiles;i++){
                    fileSize = 1000.0*parseInt(e.currentTarget.files[i].size, 10)/1024;
                    filesize = Math.round(fileSize)/1000.0;
                    if (MaxFileSize < e.currentTarget.files[i].size){
                        errFile=0;
                    }
                    //($('<li />').addClass('li_dot1').html('<i>'+e.currentTarget.files[i].name+'</i>').prepend($('<span />').addClass('glyphicon glyphicon-remove-circle removeaddfile').attr("value",i))).appendTo($('#output'));
                    ($('<li />').addClass('li_dot').html('<i>'+e.currentTarget.files[i].name+'</i>')).appendTo($('#output'));
                    $('<span />').addClass('filesize').html(' (' + filesize + 'kb)').appendTo($('#output li:last'));
                    if (i == 0){
                        $('#tooltiploadfile').removeClass('hide');
                        $('#output').addClass('MargTop');
                    }
                }
            if (errFile == 0){
                ExampleDanger.show("Maximum file size is 100MB");
                $('#loadingfile').val("");
                $('#output').empty();
                $('#output').removeClass('MargTop');
            }
        });

    $(document).on('click','.showclassicloader',function(){
        $('.form_LoadFile').removeClass('hide');
        $('.dropzone_LoadFile').addClass('hide');
        $(this).addClass('returnWPLoader');
        //$(this).removeClass('showclassicloader');
        $(this).text("drag-and-drop uploader");
    });

    $(document).on('click','.returnWPLoader',function(){
        $('.form_LoadFile').addClass('hide');
        $('.dropzone_LoadFile').removeClass('hide');
        //$(this).addClass('showclassicloader');
        $(this).removeClass('returnWPLoader');
        $(this).text("browser uploader");
    });

    $(document).on('click','.removeaddfile',function(){
        var id_image=$(this).attr("value")
        var file_input_index=0;
        //console.log("id_image="+id_image);
        //console.log($('#loadingfile')[0].files[id_image]);
        /*$('#loadingfile').each(function() {
            console.log($(this).files[file_input_index]);
            if ("id_"+file_input_index == id_image){
                console.log("-----"+$(this));
            }
            file_input_index++;
        });*/
    });

    $(document).on('click','#sendMessageFromOrder',function(){
        var bodymessage = $("#bodymessage").val();
        var subject = $("#subject").val();
        var orderid = $("input#order__id").val();
        var formData = "bodymessage="+ bodymessage + "&subject=" + subject + "&orderid=" + orderid;
        var result = "";
        //console.log(formData);
        $('#load_content_page').show();
        $.ajax(
        {
          url : "/sendmessages",
          type: "POST",
          data : formData,
          success: function(data, textStatus, jqXHR)
          {
            result = data;
            if (result == "3"){
              $("#bodymessage").val("");
              $("#subject").val("");
              ExampleSuccess.show("Your message has been successfully sent.");
            } else if(result == "0"){
              Example.show("Your message will be delivered to the writer as soon as the order is paid.");
            } else if(result == "1"){
              ExampleWarning.show("An error occurred while sending your message. Please contact us via email or live chat for resolution.");
            }
            $('#load_content_page').hide();
          },
          complete: function(xhr) {
            //status.html(xhr.responseText);
            $('#load_content_page').hide();
          },
          error: function(err) {
            $('#load_content_page').hide();
            ExampleDanger.show("Oops, something wrong... Please contact us via email or live chat for resolution.");
          }
        });

    });

    $(document).on('click','.removefilecustomer',function(){
        var id_doc=$(this).attr("value")
        $(this).parents('tr').remove();
        //console.log(id_doc);
        var data = {}; // data
            data['path'] = id_doc;
            data['remfile'] = 1;
        $('#load_content').show();
        $.ajax({
             url: "/utils",
             type: "POST",
             data: JSON.stringify(data),
             contentType: "application/json",
             dataType: 'json',
             success: function(data){
                 $('#load_content').hide();
                 if (data.result == 'good') {
                    ExampleSuccess.show("The file has been removed!");
                 }
                 else
                 {
                     ExampleWarning.show("The file has not been removed. Please contact us via email or live chat for resolution.");
                 }
             },
             error: function(err) {
                 $('#load_content').hide();
                 ExampleDanger.show("Oops, something wrong... Please contact us via email or live chat for resolution.");
             }
        });
    });

    var percent = $('.percent');
    var status = $('#status');

    $('#formLoadFile').ajaxForm({
        url: "/upload",
        type: "POST",
        dataType: "json",
        beforeSend: function(jqXHR, settings) {
            //console.log(settings);
            var percentVal = 0;
            //percent.html(percentVal+'% Complete');
            //status.css('width', percentVal+'%').attr('aria-valuenow', percentVal);
            Example.show("The files are being uploaded at the moment.");
            $('#load_content_page').show();
        },
        uploadProgress: function(event, position, total, percentComplete) {
            //percent.html(percentComplete+'% Complete');
            //status.css('width', percentComplete+'%').attr('aria-valuenow', percentComplete);
        },
        success: function(data){
            //Example.show("The files are uploaded!");

            if (data.cfiles || data.wfiles) {
                $('#output').empty().removeClass('MargTop');
                $('#load_files').empty();
            }
            //console.log(data);
            if (data.cfiles) {
                for (var i = 0; i < (data.cfiles).length; i++) {
                    $('<tr />').appendTo($('#load_files'));
                    $('<td />').text(moment(data.cfiles[i].date).format("YYYY-MM-DD HH:mm:ss")).appendTo($('#load_files tr:last'));
                    $('<td />').text(data.cfiles[i].name).appendTo($('#load_files tr:last'));
                    //$('<td />').append($('<a />').attr("href","/download_customer?file="+data.cfiles[i].path+"&name="+data.cfiles[i].name).attr("type","button").addClass( "btn btn-primary" ).text("Download")).appendTo($('#load_files tr:last'));
                    $('<td />').append($('<a />').attr("href", "/download_customer?file=" + data.cfiles[i].path + "&name=" + data.cfiles[i].name).attr("type", "button").addClass("btn btn-primary").text("Download")).append('<a href="#" type="button" class="btn btn-danger removefilecustomer" value="' + data.cfiles[i].path + '" style="margin-left: 5px;"><span class="glyphicon glyphicon-trash"></span></a>').appendTo($('#load_files tr:last'));
                }
            }
            if (data.wfiles) {
                for (var i = 0; i < (data.wfiles).length; i++) {
                    $('<tr />').appendTo($('#load_files'));
                    $('<td />').text(moment(data.wfiles[i].date).format("YYYY-MM-DD HH:mm:ss")).appendTo($('#load_files tr:last'));
                    $('<td />').text(data.wfiles[i].name).appendTo($('#load_files tr:last'));
                    $('<td />').append($('<a />').attr("href", "/download?file=" + data.wfiles[i].path + "&name=" + data.wfiles[i].name).attr("type", "button").addClass("btn btn-primary").text("Download")).appendTo($('#load_files tr:last'));
                }
            }

            $('#load_content_page').hide();
            $('.details__form').addClass('hide');
            $("html, body").animate({ scrollTop: $("#load_files").height() }, 1000);
            $('#formLoadFile').val('');
            //var percentVal = 0;
            //percent.html(percentVal+'% Complete');
            //status.css('width', percentVal+'%').attr('aria-valuenow', percentVal);

            //location.reload();
        },
        complete: function(xhr) {
            //status.html(xhr.responseText);
            $('#load_content_page').hide();
        },
        error: function(err) {
            $('#load_content_page').hide();
            ExampleDanger.show("Oops, something wrong... Please contact us via email or live chat for resolution.");
        }
    });

    $('#bt_remove_order').click(function() {
        var box = bootbox.confirm("Do you really want to delete this order <span id='ord_id'></span> permanently?<br>This action cannot be undone.", function(result) {
        if (result){
                    $('#load_content').show();
                    var data = {}; // data
                    data['rem_ord'] = 1;
                    data['id'] = $('#orderid').val();
                    $.ajax({
                             url: "/utils",
                             type: "POST",
                             data: JSON.stringify(data),
                             contentType: "application/json",
                             dataType: 'json',
                             success: function(data){
                                 $('#load_content').hide();
                                 if (data.result == 'good') {
                                    ExampleSuccess.show("The order has been removed!");
                                    window.location.href = '/dashboard';
                                 }
                                 else
                                 {
                                     ExampleWarning.show("Sorry, for some reason were unable to remove your order. Please contact us via email or live chat for resolution.");
                                 }
                             },
                             error: function(err) {
                                 $('#load_content').hide();
                                 ExampleDanger.show("Oops, something wrong... Please contact us via email or live chat for resolution.");
                             }
                            }); 
                 }
        }); 
        box.on("shown.bs.modal", function() {
            box.attr("id", "remorderdialog");
            $('#ord_id').html('<b>'+$('#orderid').val()+'</b>');
        });
    });

    if (getParameterByName("edit", $.url())) {
        $('#bt_edit_order').click();
    }

    $(document).on('click','.paypalbutton',function(){
       var targ=$('#orderid').val();
       var data = {}; // data
       data['price'] = parseFloat($('#price').val().replace(/[^0-9\.]+/g, ""));
       data['id'] = $('#orderid').val();
       if ($('#typeWork').val() == 1) {
                data['variant'] = "Writing from scratch";
            }
            else {
                data['variant'] = "Editing";
            }
       data['category'] = $('#assigmenttype').val();
       data['name'] = $('#title').val();
       data['brand'] = $('#paperformat').val();
       data['coupon'] = $('#cupon').val();
       SendYandMetrik(targ,data);
    });

    
});
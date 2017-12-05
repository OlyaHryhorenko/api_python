// floatrx :: add animate class for logo
$(document).ready(function() {
    $('.logo').addClass('animate');
});

$(function () {
    $("[data-dismiss]").on("click", function () {
        $(this).closest("." + $(this).attr("data-dismiss")).hide();
        return false;
    });
});

//(document).ready(function() {
var Example = (function () {
    "use strict";

    var elem,
        hideHandler,
        that = {};

    that.init = function (options) {
        elem = $(options.selector);
    };

    that.show = function (text) {
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
//});

//ExampleSuccess
var ExampleSuccess = (function () {
    "use strict";

    var elem,
        hideHandler,
        that = {};

    that.init = function (options) {
        elem = $(options.selector);
    };

    that.show = function (text) {
        clearTimeout(hideHandler);

        elem.find("span").html(text);
        elem.delay(200).fadeIn().delay(4000).fadeOut();
    };

    return that;
}());

$(function () {
    ExampleSuccess.init({
        "selector": ".bb-alert-success"
    });
});
//---------

//ExampleWarning
var ExampleWarning = (function () {
    "use strict";

    var elem,
        hideHandler,
        that = {};

    that.init = function (options) {
        elem = $(options.selector);
    };

    that.show = function (text) {
        clearTimeout(hideHandler);

        elem.find("span").html(text);
        elem.delay(200).fadeIn().delay(4000).fadeOut();
    };

    return that;
}());

$(function () {
    ExampleWarning.init({
        "selector": ".bb-alert-warning"
    });
});
//---------

//ExampleDanger
var ExampleDanger = (function () {
    "use strict";

    var elem,
        hideHandler,
        that = {};

    that.init = function (options) {
        elem = $(options.selector);
    };

    that.show = function (text) {
        clearTimeout(hideHandler);

        elem.find("span").html(text);
        elem.delay(200).fadeIn().delay(4000).fadeOut();
    };

    return that;
}());

$(function () {
    ExampleDanger.init({
        "selector": ".bb-alert-danger"
    });
});
//---------


function sendMessageFromOrder() {
    //console.log("!!!");
    var bodymessage = $("#bodymessage").val();
    var subject = $("#subject").val();
    var orderid = $("#order__id").val();
    //console.log("bodymessage="+ bodymessage + "&subject=" + subject + "&orderid=" + orderid);
    var formData = "bodymessage=" + bodymessage + "&subject=" + subject + "&orderid=" + orderid;
    var result = "";
    $.ajax(
        {
            url: "https://api.bryteq.com/sendmessages",
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                result = data;
                if (result == "0") {
                    $("#bodymessage").val("");
                    $("#subject").val("");
                    ExampleSuccess.show("Thank you for contacting us! We will get in touch with you shortly...");
                    //Shom_Modal_Message.show("Your message has been sent successfully.");
                } else if (result == "3") {
                    Example.show("Your message will be delivered to the writer as soon as the order is paid.");
                    //Shom_Modal_Message.show("Your message will be delivered to the writer as soon as the order is paid.");
                } else if (result == "1") {
                    ExampleDanger.show("Error when trying to send the message");
                    //Shom_Modal_Message.show("Error when trying to send the message.");
                }
            }
        });
}

function sendMessageFromContacts(id_form) {
    var id_frm = 1;
    if (id_form === undefined) {
        id_frm = 0;
    }
    var name = $('#name').val();
    var email = $('#email').val();
    var phone = $('#phone').val();
    var message = $('#message').val();
    if (id_frm == 0) {
        if (name.length > 0 && email.length > 0 && phone.length >= 8 && message.length > 0) {
            if (!isValidEmailAddress(email)) {
                ExampleWarning.show("Please, enter a valid Email!");
                return false;
            }
            if (!validate_phone(phone)) {
                ExampleWarning.show("Please, enter a valid Phone!");
                return false;
            }
            var formData = "name=" + name + "&email=" + email + "&message=" + message + "&id_frm=" + id_frm + "&phone=" + phone;
            var result = "";
            $.ajax(
                {
                    url: "/contactus",
                    type: "POST",
                    data: formData,
                    success: function (data, textStatus, jqXHR) {
                        result = data;
                        if (result == "0") {
                            $('#name').val("");
                            $('#email').val("");
                            $('#phone').val("");
                            $('#message').val("");
                            ExampleSuccess.show("Thank you for contacting us! We will get in touch with you shortly.");
                        } else if (result == "1") {
                            ExampleWarning.show("You are sending too many requests. Please try again in a couple of minutes.");
                        }
                    }
                });
        } else {
            ExampleDanger.show("Please check all fields.");
        }
    }
    if (id_frm == 1) {
        if (name.length > 0)
            if (isValidEmailAddress(email)) {
                var reCaptchaResponse = $("#g-recaptcha-response").val();
                //console.log(reCaptchaResponse);
                if (reCaptchaResponse) {
                    var formData = "name=" + name + "&email=" + email + "&id_frm=" + id_frm;
                    var result = "";
                    $.ajax(
                        {
                            url: "/contactus",
                            type: "POST",
                            data: formData,
                            success: function (data, textStatus, jqXHR) {
                                result = data;
                                if (result == "0") {
                                    bootbox.alert("Dear <b>" + name + "</b>.<br>Thank you for your interest towards our company.<br>Our recruiting department will contact you shortly.<br>Kind regards!");
                                    $('#name').val("");
                                    $('#email').val("");
                                    $('#recaptcha_reload').click();
                                } else if (result == "1") {
                                    ExampleWarning.show("You are sending too many requests. Please try again in a couple of minutes.");
                                }
                            }
                        });
                }
                else {
                    ExampleWarning.show("Please, check reCaptcha!");
                }
            }
            else {
                ExampleWarning.show("Please, enter a valid Email!");
            }
        else {
            ExampleWarning.show("Please, enter a valid First name!");
        }
    }
}

function showMsg(id) {
    $(".msg" + id).each(function () {
        $(this).show();
        $("a." + id).attr("onclick", "hideMsg(" + id + ")")
        $("a." + id).html("Close")
        $("#" + id).attr("class", "")
    });
}

function hideMsg(id) {
    $(".msg" + id).each(function () {
        $(this).hide();
        $("a." + id).attr("onclick", "showMsg(" + id + ")")
        $("a." + id).html("Open")
    });
}

function removeFile(e) {
    if (!e) {
        e = window.event;
    }
    $(e).parent().parent().remove();
}

function removeEmptyFile() {
    if ($('input:file').eq(-1).val() == '') {
        $('input:file').eq(-1).parent().remove();
    }
}


var acceptFormat = [".txt", ".zip", ".doc", ".docx", ".xls", ".xlsx", ".rtf", ".jpeg", ".png", ".gif", ".ppt", ".pptx", ".csv", ".pdf", ".jpg", ".odt"],
    acceptFormatsStr = acceptFormat.join(',');

$('#pre').on("click", function() {
    $('#upload_file').trigger('click');
});

var upload_file = [],
    tmp_file_list = $('#tmp-file-list').html();

$('#upload_file').on('change', function(e) {
    console.clear('');
    var c = true;
    for(var i = 0; i < e.target.files.length; i++) {
        var format = e.target.files[i]['name'].split('.');

        format = format[format.length-1];

        if(format) {
            if(acceptFormat.indexOf('.'+ format) != -1) {
                for(var key = 0; upload_file.length > key; key++) {
                  if(!upload_file[key]) {
                    upload_file.splice(key, 1);
                  }else{
                    if( upload_file[key]['name'] == e.target.files[i]['name'] ) {
                        c = false;
                        break;
                    }  
                  }
                }
            }
        }

        if(!upload_file.length && acceptFormat.indexOf('.'+ format) != -1 || c && acceptFormat.indexOf('.'+ format) != -1) {
            upload_file.push(e.target.files[i]);
        }
    }
    var message = '', keys = {};
    for (var up = 0; up < upload_file.length; up++) {
        keys.id = up;
        keys.file_name = upload_file[up]['name'];
        message += tmp_file_list.replace(/\/\:[^\:\/]*\:\//g, function(e, d) {
            e = e.replace(/[\:\/]/g, '');
            return keys[e];
        });
    }

    $('#list-files').html(message);
}).attr('accept', acceptFormatsStr);

$('#list-files').on('click', '.close-file', function() {
    upload_file[$(this).data('id')] = 0;
    $(this).parents('li').slideUp(100);
    setTimeout(function() {
        $(this).parents('li').remove();
    });
});

function onValidate(e) {
    removeEmptyFile();
}
//--------- Check Email ------------------
function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
};
//---------- End Check Email -------------
//--------- Reset Password ------------------
function forgotpassword() {
    var resetmail = $("input#resetpassword").val();
    var formData = "mail=" + resetmail;
    var result = "";
    if (isValidEmailAddress(resetmail)) {
        $.ajax(
            {
                url: "https://api.bryteq.com/forgotpassword",
                type: "POST",
                data: formData,
                success: function (data, textStatus, jqXHR) {
                    result = data;
                    if (result == "0") {
                        Example.show("Check your email for a new password. Don't forget to check the spam/junk folder or unlock address support@writemypaper4me.org.");
                    } else {
                        ExampleWarning.show("Invalid email address.");
                    }
                }
            });
    }
    else {
        ExampleWarning.show("Invalid email address.");
    }
}
//--------- End Reset Password --------------
//------------------ Discount -----------------------
function checkdiscount(disccode, tprice) {
    var discountcode = disccode;
    var formData = "discountcode=" + discountcode;
    var result = "";
    $.ajax(
        {
            url: "https://api.bryteq.com/checkdiscount",
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                result = data;
                if (result == "0") {
                    ExampleWarning.show("Incorrect discount codе.");
                } else {
                    var total = tprice;
                    var totaldisc = (total - (total * (result / 100))).toFixed(2)
                    $('input[name=xdiscountcode]').val(discountcode);
                    return totaldisc;
                }
            }
        });
}

function getdiscount() {
    var getdiscountcode = $("input#getdiscountcode").val();
    var formData = "mail=" + getdiscountcode;
    var result = "";
    if (isValidEmailAddress(getdiscountcode)) {
        $.ajax(
            {
                url: "https://api.bryteq.com/getdiscount",
                type: "POST",
                data: formData,
                success: function (data, textStatus, jqXHR) {
                    result = data;
                    if (result == "0") {
                        ExampleWarning.show("Check your email for a discount code! Don't forget to check the Spam folder.");
                    } else {

                    }
                }
            });
    }
    else {
        ExampleDanger.show("Please enter a valid Email.");
    }
}
//------------------ End Discount -------------------
//------------------ Contacts And Testimonials -----------------------
function asendcontactform() {
    var name = $("input#name").val();
    var email = $("input#email").val();
    var message = $('textarea#message').val();
    var formData = "name=" + name + "&email=" + email + "&message=" + message;
    var result = "";
    $.ajax(
        {
            url: "https://api.bryteq.com/contactus",
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                result = data;
                if (result == "0") {
                    ExampleSuccess.show("Thank you! Your message has been successfully sent.");
                } else if (result == "1") {
                    ExampleWarning.show("You are sending too many requests. Please try again in a couple of minutes.");
                }
            }
        });
}
function atestimonials() {
    var name = $("input#name").val();
    var email = $("input#email").val();
    var rating = $("input#rating").val();
    var message = $('textarea#message').val();
    var formData = "name=" + name + "&email=" + email + "&rating=" + rating + "&message=" + message;
    var result = "";
    $.ajax(
        {
            url: "https://api.bryteq.com/atestimonials",
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                result = data;
                if (result == "0") {
                    ExampleSuccess.show("We have already received your feedback. Thank you!");
                } else if (result == "1") {
                    ExampleWarning.show("You are sending too many requests. Please try again in a couple of minutes.");
                }
            }
        });
}
//------------------ End Contacts And Testimonials -------------------

//------------------ SHOW/BLOCK progress ---------------------------
function ShowProgress(){
    $('.ordermodal').addClass('disabled');
    $('i.glyphicon.glyphicon-refresh.glyphicon-spin').removeClass('hide');
}
function HideProgress(){
    $('i.glyphicon.glyphicon-refresh.glyphicon-spin').addClass('hide');
    $('.ordermodal').removeClass('disabled');
}
//------------------ END SHOW/BLOCK progress -----------------------

//------------------ LOGIN -----------------------
function alogin() {
    if (validate_topic()) {
        if (validate_decription()) {
            ShowProgress();
            var totalPrice = $("[data-total-price]");
            var curprice = totalPrice.data('total-price');

            if (curprice == '0.00') {
                ExampleWarning.show("You are about to place an urgent Ph.D! order. Before you can proceed, Please discuss your paper details with our Customer Support.");
                $zopim.livechat.window.show();
                HideProgress();
                return false;
            }
            var email = $("input#lemail").val();
            var password = $("input#lpassword").val();
            var site_id = localStorage.getItem('site_id');
            var formData = "email=" + email + "&password=" + password + "&site_id=" + site_id;
            var result = "";
            $.ajax(
                {
                    url: "https://api.bryteq.com/api/login",
                    type: "POST",
                    data: formData,
                    xhrFields: {
                        withCredentials: true
                    },
                    crossDomain: true,
                    success: function (data, textStatus, jqXHR) {
                        result = data;
                        var obj = JSON.parse(result);
                        localStorage.setItem('user_id', obj.id);
        
                        $('#user_id').val(obj.id);
                        console.log(result);
                        if (obj) {
                            console.log(obj);
                            $("#subform").submit();
                        } else {
                            HideProgress();
                            if (result == "1") {
                                ExampleWarning.show("Sorry, unrecognized <b>Email</b> or <b>Password</b>.");
                            }
                        }
                    },
                    error: function () {
                        HideProgress();
                    }
                });
        } else {
            ExampleWarning.show("Please fill in the <b>Paper details</b> field.");
        }
    } else {
        ExampleWarning.show("Please fill in the <b>Title</b> field or type in “Writer’s choice” so that our writer would choose an appropriate <b>Title</b> for your paper.");
    }
}

function alogin2() {


    var email = $("input#remail").val();
    var password = $("input#rpassword").val();
    var site_id  = $("input#site_id").val();
    var formData = "email=" + email + "&password=" + password + "&site_id=" + site_id;
    var result = "";
    console.log(formData);
    // $.ajax(
    //     {
    //         url: "https://api.bryteq.com/api/login",
    //         type: "POST",
    //         data: formData,
    //         xhrFields: {
    //             withCredentials: true
    //         },
    //         crossDomain: true,
    //         success: function (data, textStatus, jqXHR) {
    //             result = data;
    //             var obj = JSON.parse(result);
    //             localStorage.setItem('user_id', obj.id);
    //             $('#user_id').val(obj.id);
    //             console.log(result);
    //             if (obj) {
    //             console.log('0');
    //            // $(location).attr('href', '/dashboard');
    //             } else if (result == "1") {
    //                 console.log('ss')
    //             }
    //         }
    //     });
}
//------------------ LOGIN END -----------------------
function aforgot() {
    var email = $("input#lemail").val();
    var formData = "email=" + email;
    var result = "";
    $.ajax(
        {
            url: "https://api.bryteq.com/forgot",
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                result = data;
                if (result == "0") {
                    ExampleSuccess.show("Your password has been successfully updated. Check your email.");
                } else if (result == "1") {
                    ExampleDanger.show("Error when trying to update your password.");
                }
            }
        });
}

function aregistration(fast_reg) {
    if ($('a.btn.acceptfororder').hasClass('notAccept')) {
        ExampleWarning.show("Please, accept the Terms of Use and Privacy and Cookies Policy.");
        return false;
    }
    if (validate_topic()) {
        if (validate_decription()) {

            var totalPrice = $("[data-total-price]");
            var curprice = totalPrice.data('total-price');

            if (curprice == '0.00') {
                ExampleWarning.show("You are about to place an urgent Ph.D! order. Before you can proceed, Please discuss your paper details with our Customer Support.");
                $zopim.livechat.window.show();
                return false;
            }

            var fr = 1;
            if (fast_reg === undefined) {
                fr = 0;
            }

            var firstname = $("input#fname").val();
            var lastname = $("input#lname").val();
            var email = $("input#email").val();
            var phone_old = $("input#phone").val();
            var area = $("input#phone_area").val();
            var numb = $("input#phone_numb").val();
            var phone = $("#phone_numb").val();
            var password = $("input#password").val();
            var cpassword = $("input#cpassword").val();

            var site_id = $('input#site_id').val();
            var formData = "fr=" + fr + "&fname=" + firstname + "&lname=" + lastname + "&email=" + email + "&phone=" + phone + "&password=" + password + "&cpassword=" + cpassword + "&site_id=" +site_id;
            var result = "";
            console.log(site_id);
            var xformData = "email=" + email;
            var xresult = "";
            if (isValidEmailAddress(email)) {
                ShowProgress();
                console.log(formData)
                $.ajax(
                    {
                        url: "https://api.bryteq.com/checkmail",
                        type: "POST",
                        data: xformData,
                        success: function (data, textStatus, jqXHR) {
                            xresult = data;
                            if (xresult == "0") {
                                if ((password == cpassword && password != '') || ( (fr == 1) && (area != '') && (numb != '') )) {
                                    $('.preload-order').css('display', 'inline-block');
                                    $.ajax(
                                        {
                                            url: "https://api.bryteq.com/aregistration",
                                            type: "POST",
                                            data: formData,
                                            success: function (data, textStatus, jqXHR) {
                                                result = data;
                                                var obj = JSON.parse(result);
                                                localStorage.setItem('user_id', obj.id);
                                                $('#user_id').val(obj.id);
                                                console.log(result);
                                                $("#subform").submit();
                                                if (obj) {
                                                    if (fr == 1) {
                                                        var sign__up_tex = $('.sign-up__title').html();
                                                        $('.sign-up__title').html(sign__up_tex + " <br>The password will be automatically sent to your email: <strong>" + email + "</strong>");
                                                    }
                                                    
                                                   

                                                } else {
                                                    HideProgress();
                                                    if (result == "1") {
                                                        ExampleDanger.show("Error! All fields are mandatory.");
                                                    }
                                                }
                                            },
                                            error: function () {
                                                HideProgress();
                                            }
                                        });
                                } else {
                                    HideProgress();
                                    if (fr == 1) {
                                        ExampleWarning.show("Error! Please enter your phone number.");
                                    }
                                    else {
                                        ExampleWarning.show("Error! Password mismatch.");
                                    }
                                }
                            } else {
                                ExampleWarning.show("This E-mail is already registered. Maybe you are already a member.  <a href=/forgot.html><strong>Click here to Restore Password</strong></a>");
                                HideProgress();
                            }
                        },
                        error: function () {
                            HideProgress();
                        }
                    });
            } else {
                ExampleDanger.show("Invalid email address");
            }
        } else {
            ExampleWarning.show("Please fill in the <b>Paper details</b> field.");
        }
    } else {
        ExampleWarning.show("Please fill in the <b>Title</b> field or type in “Writer’s choice” so that our writer would choose an appropriate <b>Title</b> for your paper.");
    }
}

function asendmessage() {
    var bodymessage = $("#bodymessage").val();
    var sendto = $("#sendto").find('option:selected').text();
    var orderid = $("input#orderid").val();
    var formData = "bodymessage=" + bodymessage + "&sendto=" + sendto + "&orderid=" + orderid;
    var result = "";
    $.ajax(
        {
            url: "/sendmessages",
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                result = data;
                if (result == "0") {
                    ExampleSuccess.show("Your profile has been successfully updated!");
                } else if (result == "1") {
                    ExampleDanger.show("An error occured while updating your profile.");
                    ;
                }
            }
        });
}

function messageModalForm(e) {
    if (validateMessageModalForm(e)) {
        $('.message input[name="date"]').val(getDateTime());
        $.ajax({
            url: '/messages_outbox',
            type: 'POST',
            data: new FormData(e),
            processData: false,
            contentType: false
        }).done(function () {
            bootbox.alert("0");
        }).fail(function () {
            bootbox.alert("1");
        });
    }
    return false;
}

//-----------------------
(function ($) {
    var fn = function (data, options) {
        if (options.callback) {
            options.callback(data);
        }
        else if (options.contentType === 'json' && ((typeof data === 'string' && !data.indexOf('{') && (data = json_decode$(data))) || typeof data === 'object')) {
            call$(data)
        }

        if (options.complete)options.complete(data);
    }

    $.fn.sf$ = function (options) {
        options = $.extend({
            contentType: 'json',
            beforeSend: null,
            afterSend: null,
            xhr: null,
            error: function (a, b, c) {
                console.log(c)
            },
            complete: null,
            callback: null,
            timeout: 0,
            iframe: 0
        }, options || {});

        return this.each(typeof FormData !== 'undefined' ? function () {
            var form = $(this);
            if (typeof tinymce !== 'undefined') {
                form.find('textarea.tinymce').each(function () {
                    tinymce.get(this.id).save()
                });
            }
            var formData = new FormData(form[0]), param = {
                url: form[0].action,
                type: 'POST',
                beforeSend: options.beforeSend,
                error: options.error,
                success: function (data, status, xhr) {
                    fn(data, options)
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                timeout: options.timeout
            };
            if (options.xhr)param.xhr = options.xhr;
            $.ajax(param);
            if (options.afterSend)options.afterSend();
        } : function () {
            options.iframe = 1;
            var name = 'sf-' + Math.random(), form = $(this), div = $('<div />').appendTo('body').hide().html('<iframe src="javascript:false" name="' + name + '"></iframe>');
            form.attr('target', name);
            var iframe = div.children('iframe'), container = form.parent(), requestDone = false, timer;
            var request_fn = function (data) {
                if (requestDone)fn(data, options); else if (options.error)options.error(null, null, 'timeout');
                div.remove();
            }
            iframe.one('load', function () {
                requestDone = true;
                clearTimeout(timer);
                try {
                    var doc = (this.contentWindow && this.contentWindow.document) || this.contentDocument || this.document;
                    if (doc && doc.location.href != 'about:blank') {
                        var f = $('body', doc), data = f.html();
                        request_fn(data);
                    }
                }
                catch (e) {
                    if (options.error)options.error(null, null, e);
                }
            });
            if (options.beforeSend)options.beforeSend();
            form[0].submit();
            if (options.timeout)timer = setTimeout(function () {
                request_fn()
            }, options.timeout);
            if (options.afterSend)options.afterSend();
        })
    }
})
(jQuery);
//-----------------------

function aprofileupdate(el) {
    el = (el == undefined) ? 0 : el;
    var name = $("#name").val();
    var phone = $("#phone_numb").val();
    var email = $('#email_customer').val();
    var newsletters = $('#newsletters').val();
    var formData = "name=" + name + "&phone=" + phone + "&email=" + email + "&newsletters=" + newsletters;
    var result = "";
    if (name == "") {
        ExampleWarning.show("The name field is epmty.");
        return false;
    }
    if (email == "") {
        ExampleWarning.show("The email field is epmty.");
        return false;
    }
    if (!isValidEmailAddress(email)) {
        ExampleWarning.show("Please, enter a valid Email!");
        return false;
    }
    if(el) {
        el.addClass('hold');
    }

    $.ajax(
        {
            url: "/updateprofile",
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                result = data;
                if(el) {
                    el.removeClass('hold');
                }

                if (result == "0") {
                    //bootbox.alert("Your profile has been successfully updated!");
                    ExampleSuccess.show("Your profile has been successfully updated!");
                    return true;
                } else if (result == "1") {
                    //bootbox.alert("Error update your profile.");
                    ExampleDanger.show("An error occured while updating your profile.");
                    return false;
                }
            }
        });
    return true;
}

function apasswordupdate(el) {
    el = (el == undefined) ? 0 : el;
    var oldpassword = $("#oldpassword").val();
    var newpassword = $("#newpassword").val();
    var cnewpassword = $("#cnewpassword").val();
    if (oldpassword == "") {
        ExampleWarning.show("The password field is epmty.");
        return false;
    }
    if (newpassword == "") {
        ExampleWarning.show("The new password field is epmty.");
        return false;
    }
    if (newpassword == cnewpassword) {
        if(el) {
            el.addClass('hold');
        }
        var formData = "password=" + oldpassword + "&newpass=" + newpassword;
        var result = "";
        $.ajax(
            {
                url: "/updatepassword",
                type: "POST",
                data: formData,
                success: function (data, textStatus, jqXHR) {
                    result = data;
                    if(el) {
                        el.removeClass('hold');
                    }
                    if (result == "0") {
                        //bootbox.alert("Your password was updated successfully!");
                        ExampleSuccess.show("Your password has been successfully updated!");
                        $("#oldpassword").val("");
                        $("#newpassword").val("");
                        $("#cnewpassword").val("");
                    } else if (result == "1") {
                        //bootbox.alert("Error update your password");
                        ExampleDanger.show("The old password is different from the one you entered.");
                    }
                }
            });
    } else {
        //bootbox.alert("New password and confirm password fields do not match.");
        ExampleWarning.show("New password and confirm password fields do not match.");
    }
}

$("#login_check_button").click(function (e) {
    if (validate_topic()) {
        if (validate_decription()) {
            return true;
        }
        else {
            ExampleWarning.show("Please fill in the <b>Paper details</b> field.");
            return false;
        }
    }
    else {
        ExampleWarning.show("Please fill in the <b>Title</b> field or type in “Writer’s choice” so that our writer would choose an appropriate <b>Title</b> for your paper.");
        return false;
    }
});

//------------------------------ pages -------
$('.btn-number').click(function (e) {
    e.preventDefault();

    fieldName = $(this).attr('data-field');
    type = $(this).attr('data-type');
    var input = $("input[name=pages]");
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if (type == 'minus') {

            if (currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            }
            if (parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            } else {
                $(this).removeAttr('disabled')
            }

        } else if (type == 'plus') {

            if (currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if (parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            } else {
                $(this).removeAttr('disabled')
            }
        }
    } else {
        input.val(0);
    }
});
$('.input-number').focusin(function () {
    $(this).data('oldValue', $(this).val());
});
$('.input-number').change(function () {

    minValue = parseInt($(this).attr('min'));
    maxValue = parseInt($(this).attr('max'));
    valueCurrent = parseInt($(this).val());

    name = $(this).attr('name');
    if (valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field=pages]").removeAttr('disabled')
    } else {
        bootbox.alert('Sorry, the minimum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    if (valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field=pages]").removeAttr('disabled')
    } else {
        bootbox.alert('Sorry, the maximum value was reached');
        $(this).val($(this).data('oldValue'));
    }


});

$(".input-number").keydown(function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
        // Allow: Ctrl+A
        (e.keyCode == 65 && e.ctrlKey === true) ||
        // Allow: home, end, left, right
        (e.keyCode >= 35 && e.keyCode <= 39)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});

$("form[name='subform'] :input").change(function () {
    var counter = jQuery('input[name=pages]').val();
    tot = parseInt(counter);
    $("#words").html(tot * 300 + ' words');
});

// ----------------------- 
//------------------------------ sources -------
$('.btn-number').click(function (e) {
    e.preventDefault();

    fieldName = $(this).attr('data-field');
    type = $(this).attr('data-type');
    var input = $("input[name=sources]");
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if (type == 'sminus') {

            if (currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            }
            if (parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if (type == 'splus') {

            if (currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if (parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    }
});
$('.input-number').focusin(function () {
    $(this).data('oldValue', $(this).val());
});
$('.input-number').change(function () {

    minValue = parseInt($(this).attr('min'));
    maxValue = parseInt($(this).attr('max'));
    valueCurrent = parseInt($(this).val());

    name = $(this).attr('name');
    if (valueCurrent >= minValue) {
        $(".btn-number[data-type='sminus'][data-field=sources]").removeAttr('disabled')
    } else {
        bootbox.alert('Sorry, the minimum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    if (valueCurrent <= maxValue) {
        $(".btn-number[data-type='splus'][data-field=sources]").removeAttr('disabled')
    } else {
        bootbox.alert('Sorry, the maximum value was reached');
        $(this).val($(this).data('oldValue'));
    }


});

$(".input-number").keydown(function (e) {
    // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
        // Allow: Ctrl+A
        (e.keyCode == 65 && e.ctrlKey === true) ||
        // Allow: home, end, left, right
        (e.keyCode >= 35 && e.keyCode <= 39)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});
// ----------------------- 
$(document).ready(function () {
    $('#IAmNew').change(function () {
        $('#CheckOutForm').css('display', 'none');
        $('#regForm').css('display', 'block');

    });
    $('#CheckMeRad').change(function () {
        $('#regForm').css('display', 'none');
        $('#CheckOutForm').css('display', 'block');

    });

    $("form[name='subform'] :input").change(function () {

        //counter methods
        var academic = jQuery('input[name=academic_levels]:checked').val();
        var urgency = jQuery('input[name=urgency]:checked').val();
        var counter = jQuery('input[name=pages]').val();
        var High_School = [9.95, 10.95, 11.95, 12.95, 13.95, 15.95, 17.95, 19.95];
        var College = [11.95, 12.95, 13.95, 14.95, 15.95, 17.95, 19.95, 22.95];
        var University = [13.95, 14.95, 15.95, 16.95, 17.95, 19.95, 21.95, 24.95];
        var Masters = [16.95, 18.95, 20.95, 22.95, 24.95, 27.95, 30.95, 33.95];
        var PhD = [19.95, 21.95, 23.95, 25.95, 27.95, 30.95];
        tot = parseInt(counter);

        if (academic === "1") {
            if (urgency === "10") {
                $("#totalprice").html('$' + (tot * High_School[0]).toFixed(2));
                $('input[name=total]').val((tot * High_School[0]).toFixed(2));
            }
            ;
            if (urgency === "9") {
                $("#totalprice").html('$' + (tot * High_School[1]).toFixed(2));
                $('input[name=total]').val((tot * High_School[1]).toFixed(2));
            }
            ;
            if (urgency === "8") {
                $("#totalprice").html('$' + (tot * High_School[1]).toFixed(2));
                $('input[name=total]').val((tot * High_School[1]).toFixed(2));
            }
            ;
            if (urgency === "7") {
                $("#totalprice").html('$' + (tot * High_School[2]).toFixed(2));
                $('input[name=total]').val((tot * High_School[2]).toFixed(2));
            }
            ;
            if (urgency === "6") {
                $("#totalprice").html('$' + (tot * High_School[2]).toFixed(2));
                $('input[name=total]').val((tot * High_School[2]).toFixed(2));
            }
            ;
            if (urgency === "5") {
                $("#totalprice").html('$' + (tot * High_School[3]).toFixed(2));
                $('input[name=total]').val((tot * High_School[3]).toFixed(2));
            }
            ;
            if (urgency === "4") {
                $("#totalprice").html('$' + (tot * High_School[3]).toFixed(2));
                $('input[name=total]').val((tot * High_School[3]).toFixed(2));
            }
            ;
            if (urgency === "3") {
                $("#totalprice").html('$' + (tot * High_School[4]).toFixed(2));
                $('input[name=total]').val((tot * High_School[4]).toFixed(2));
            }
            ;
            if (urgency === "2") {
                $("#totalprice").html('$' + (tot * High_School[5]).toFixed(2));
                $('input[name=total]').val((tot * High_School[5]).toFixed(2));
            }
            ;
            if (urgency === "1") {
                $("#totalprice").html('$' + (tot * High_School[6]).toFixed(2));
                $('input[name=total]').val((tot * High_School[6]).toFixed(2));
            }
            ;
            if (urgency === "0") {
                $("#totalprice").html('$' + (tot * High_School[7]).toFixed(2));
                $('input[name=total]').val((tot * High_School[7]).toFixed(2));
            }
            ;
        }

        if (academic === "2") {
            if (urgency === "10") {
                $("#totalprice").html('$' + (tot * College[0]).toFixed(2));
                $('input[name=total]').val((tot * College[0]).toFixed(2));
            }
            ;
            if (urgency === "9") {
                $("#totalprice").html('$' + (tot * College[1]).toFixed(2));
                $('input[name=total]').val((tot * College[1]).toFixed(2));
            }
            ;
            if (urgency === "8") {
                $("#totalprice").html('$' + (tot * College[1]).toFixed(2));
                $('input[name=total]').val((tot * College[1]).toFixed(2));
            }
            ;
            if (urgency === "7") {
                $("#totalprice").html('$' + (tot * College[2]).toFixed(2));
                $('input[name=total]').val((tot * College[2]).toFixed(2));
            }
            ;
            if (urgency === "6") {
                $("#totalprice").html('$' + (tot * College[2]).toFixed(2));
                $('input[name=total]').val((tot * College[2]).toFixed(2));
            }
            ;
            if (urgency === "5") {
                $("#totalprice").html('$' + (tot * College[3]).toFixed(2));
                $('input[name=total]').val((tot * College[3]).toFixed(2));
            }
            ;
            if (urgency === "4") {
                $("#totalprice").html('$' + (tot * College[3]).toFixed(2));
                $('input[name=total]').val((tot * College[3]).toFixed(2));
            }
            ;
            if (urgency === "3") {
                $("#totalprice").html('$' + (tot * College[4]).toFixed(2));
                $('input[name=total]').val((tot * College[4]).toFixed(2));
            }
            ;
            if (urgency === "2") {
                $("#totalprice").html('$' + (tot * College[5]).toFixed(2));
                $('input[name=total]').val((tot * College[5]).toFixed(2));
            }
            ;
            if (urgency === "1") {
                $("#totalprice").html('$' + (tot * College[6]).toFixed(2));
                $('input[name=total]').val((tot * College[6]).toFixed(2));
            }
            ;
            if (urgency === "0") {
                $("#totalprice").html('$' + (tot * College[7]).toFixed(2));
                $('input[name=total]').val((tot * College[7]).toFixed(2));
            }
            ;
        }


        if (academic === "3") {
            if (urgency === "10") {
                $("#totalprice").html('$' + (tot * University[0]).toFixed(2));
                $('input[name=total]').val((tot * University[0]).toFixed(2));
            }
            ;
            if (urgency === "9") {
                $("#totalprice").html('$' + (tot * University[1]).toFixed(2));
                $('input[name=total]').val((tot * University[1]).toFixed(2));
            }
            ;
            if (urgency === "8") {
                $("#totalprice").html('$' + (tot * University[1]).toFixed(2));
                $('input[name=total]').val((tot * University[1]).toFixed(2));
            }
            ;
            if (urgency === "7") {
                $("#totalprice").html('$' + (tot * University[2]).toFixed(2));
                $('input[name=total]').val((tot * University[2]).toFixed(2));
            }
            ;
            if (urgency === "6") {
                $("#totalprice").html('$' + (tot * University[2]).toFixed(2));
                $('input[name=total]').val((tot * University[2]).toFixed(2));
            }
            ;
            if (urgency === "5") {
                $("#totalprice").html('$' + (tot * University[3]).toFixed(2));
                $('input[name=total]').val((tot * University[3]).toFixed(2));
            }
            ;
            if (urgency === "4") {
                $("#totalprice").html('$' + (tot * University[3]).toFixed(2));
                $('input[name=total]').val((tot * University[3]).toFixed(2));
            }
            ;
            if (urgency === "3") {
                $("#totalprice").html('$' + (tot * University[4]).toFixed(2));
                $('input[name=total]').val((tot * University[4]).toFixed(2));
            }
            ;
            if (urgency === "2") {
                $("#totalprice").html('$' + (tot * University[5]).toFixed(2));
                $('input[name=total]').val((tot * University[5]).toFixed(2));
            }
            ;
            if (urgency === "1") {
                $("#totalprice").html('$' + (tot * University[6]).toFixed(2));
                $('input[name=total]').val((tot * University[6]).toFixed(2));
            }
            ;
            if (urgency === "0") {
                $("#totalprice").html('$' + (tot * University[7]).toFixed(2));
                $('input[name=total]').val((tot * University[7]).toFixed(2));
            }
            ;
        }

        if (academic === "4") {
            if (urgency === "10") {
                $("#totalprice").html('$' + (tot * Masters[0]).toFixed(2));
                $('input[name=total]').val((tot * Masters[0]).toFixed(2));
            }
            ;
            if (urgency === "9") {
                $("#totalprice").html('$' + (tot * Masters[1]).toFixed(2));
                $('input[name=total]').val((tot * Masters[1]).toFixed(2));
            }
            ;
            if (urgency === "8") {
                $("#totalprice").html('$' + (tot * Masters[1]).toFixed(2));
                $('input[name=total]').val((tot * Masters[1]).toFixed(2));
            }
            ;
            if (urgency === "7") {
                $("#totalprice").html('$' + (tot * Masters[2]).toFixed(2));
                $('input[name=total]').val((tot * Masters[2]).toFixed(2));
            }
            ;
            if (urgency === "6") {
                $("#totalprice").html('$' + (tot * Masters[2]).toFixed(2));
                $('input[name=total]').val((tot * Masters[2]).toFixed(2));
            }
            ;
            if (urgency === "5") {
                $("#totalprice").html('$' + (tot * Masters[3]).toFixed(2));
                $('input[name=total]').val((tot * Masters[3]).toFixed(2));
            }
            ;
            if (urgency === "4") {
                $("#totalprice").html('$' + (tot * Masters[3]).toFixed(2));
                $('input[name=total]').val((tot * Masters[3]).toFixed(2));
            }
            ;
            if (urgency === "3") {
                $("#totalprice").html('$' + (tot * Masters[4]).toFixed(2));
                $('input[name=total]').val((tot * Masters[4]).toFixed(2));
            }
            ;
            if (urgency === "2") {
                $("#totalprice").html('$' + (tot * Masters[5]).toFixed(2));
                $('input[name=total]').val((tot * Masters[5]).toFixed(2));
            }
            ;
            if (urgency === "1") {
                $("#totalprice").html('$' + (tot * Masters[6]).toFixed(2));
                $('input[name=total]').val((tot * Masters[6]).toFixed(2));
            }
            ;
            if (urgency === "0") {
                $("#totalprice").html('$' + (tot * Masters[7]).toFixed(2));
                $('input[name=total]').val((tot * Masters[7]).toFixed(2));
            }
            ;

        }

        if (academic === "5") {
            if (urgency === "10") {
                $("#totalprice").html('$' + (tot * PhD[0]).toFixed(2));
                $('input[name=total]').val((tot * PhD[0]).toFixed(2));
            }
            ;
            if (urgency === "9") {
                $("#totalprice").html('$' + (tot * PhD[1]).toFixed(2));
                $('input[name=total]').val((tot * PhD[1]).toFixed(2));
            }
            ;
            if (urgency === "8") {
                $("#totalprice").html('$' + (tot * PhD[1]).toFixed(2));
                $('input[name=total]').val((tot * PhD[1]).toFixed(2));
            }
            ;
            if (urgency === "7") {
                $("#totalprice").html('$' + (tot * PhD[2]).toFixed(2));
                $('input[name=total]').val((tot * PhD[2]).toFixed(2));
            }
            ;
            if (urgency === "6") {
                $("#totalprice").html('$' + (tot * PhD[2]).toFixed(2));
                $('input[name=total]').val((tot * PhD[2]).toFixed(2));
            }
            ;
            if (urgency === "5") {
                $("#totalprice").html('$' + (tot * PhD[3]).toFixed(2));
                $('input[name=total]').val((tot * PhD[3]).toFixed(2));
            }
            ;
            if (urgency === "4") {
                $("#totalprice").html('$' + (tot * PhD[3]).toFixed(2));
                $('input[name=total]').val((tot * PhD[3]).toFixed(2));
            }
            ;
            if (urgency === "3") {
                $("#totalprice").html('$' + (tot * PhD[4]).toFixed(2));
                $('input[name=total]').val((tot * PhD[4]).toFixed(2));
            }
            ;
            if (urgency === "2") {
                $("#totalprice").html('$' + (tot * PhD[5]).toFixed(2));
                $('input[name=total]').val((tot * PhD[5]).toFixed(2));
            }
            ;
            if (urgency === "1") {
                $("#totalprice").html('Sorry, not available');
                $('input[name=total]').val(0);
            }
            ;
            if (urgency === "0") {
                $("#totalprice").html('Sorry, not available');
                $('input[name=total]').val(0);
            }
            ;
        }
    });
});

function validate_topic() {
    if ($('#topic').val().replace(/[_\W]+/g, "").replace(/\s/g, '').length === 0) {
        return false;
    } else {
        return true;
    }
}

function validate_decription() {
    if ($('#paperDetails').val().replace(/[_\W]+/g, "").replace(/\s/g, '').length === 0) {
        return false;
    } else {
        return true;
    }
}

function validate_phone(phoneNumber) {
    var phoneNumberPattern = /^\D*([2-9]\d{2})(\D*)([2-9]\d{2})(\D*)(\d{4})\D*$/;
    return phoneNumberPattern.test(phoneNumber);
}

function check_site(site)
{
    $.ajax({
        url: 'https://api.bryteq.com/api/site_identity',
        type: 'POST',
        async: false,
        data: JSON.stringify({site:site}),
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        contentType: 'application/json;charset=UTF-8',
        success: function(response){
            console.log(response);
            localStorage.setItem('site_id', response);
            $('#site_id').val(response);
        },
        error: function(error) {
            console.log("error");
            console.log(error);
        }
    });
}



urlParams = new URLSearchParams(window.location.search);
url = urlParams.get('site');
check_site(urlParams.get('site'));


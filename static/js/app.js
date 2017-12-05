"use strict";
//$(function () {
var calendarInput,
    calendarInputValue,
    calendarInputDate,
    useCurrent,
    countInput,
    inputValue,
    timeType,
    deadlineText,
    element,
    headerHeightBefore,
    totalPrice,
    chekout,
    calcData = {
        typeOfWork: 1,
        academicLevel: $("[name=academicLevel] option:selected").val(),
        deadline: null,
        pages: $('#pages').val(),
        spaced: 2
    },
    calendarInputMain;

if (!calcData.academicLevel) {
    calcData.academicLevel = $("[name=academicLevel]:checked").val();
}
if ($("[name=workType]:checked").val()) {
    calcData.typeOfWork = $("[name=workType]:checked").val();
}
if ($("select[name=spaced]").val()) {
    calcData.spaced = $("[name=spaced]:checked").val();
}

headerHeightBefore = $(".header__top").outerHeight(true);
onscroll(headerHeightBefore);

totalPrice = $("[data-total-price]");
chekout = $('.ordermodal');

$("[data-deadlineTimeWrapper]").hide();

//MAIN PAGE
calendarInputMain = $(".form-control-deadline");

//ORDER FORM
calendarInput = $(".calendar input[type=text]");
deadlineText = $("[data-deadline]");

calendarInputValue = calendarInput.val();

if (calendarInputValue) {
    calendarInputDate = moment(calendarInputValue);
    orderFormCalc(calendarInputDate, calcData, deadlineText, totalPrice);

    if (calendarInputValue === moment().format("YYYY-MM-DD")) {
        useCurrent = true;
    }
    else {
        useCurrent = false;
    }
}

calendarInput.datetimepicker({
    minDate: new Date(),
    maxDate: moment().add(365, 'days'),
    format: "YYYY-MM-DD",
    showTodayButton: false,
    useCurrent: false,
    disabledDates: [new Date()],
}).on('dp.change', function (e) {
    calendarInput.blur();
    orderFormCalc(e.date, calcData, deadlineText, totalPrice);
});

calendarInputMain.datetimepicker({
    minDate: moment().add(1, 'days'),
    maxDate: moment().add(365, 'days'),
    format: "YYYY-MM-DD",
    showTodayButton: false,
    useCurrent: false,
}).on("dp.change", function (e) {
    calendarInputMain.blur();
    RecalcDate(e.date);
}).on("dp.show", function () {
    //console.log("0 Start= "+moment(calendarInputMain.val()).format("DD MM YYYY HH:mm:ss"));
    $("[data-calendar-today]").click(function (event) {
        setTimeout(function () {
            //Hide calendar when TODAY button is clicked
            calendarInputMain.data("DateTimePicker").hide();
        }, 100);
    })
})

function RecalcDate(val_date) {
    var FinDate = moment(moment(val_date).format("YYYY-MM-DD"), "YYYY-MM-DD");
    var StarDate = moment();
    //var dateDiff = moment.duration(StarDate.diff(moment(StarDate.format("YYYY-MM-DD"),"YYYY-MM-DD")));
    var dateDiff = StarDate.diff(moment(StarDate.format("YYYY-MM-DD"), "YYYY-MM-DD"), 'seconds');
    FinDate = FinDate.add(dateDiff, 'seconds');
    if (val_date.format("YYYY-MM-DD") === moment().format("YYYY-MM-DD")) {

        var hours = $("[data-deadlineTimeSelect]").find(":selected").val();
        //var than = moment(moment(e.date).format("YYYY-MM-DD") + " " + hours);
        //var now = moment();

        FinDate = FinDate.add(hours, 'hours');

        $("[data-deadlineTimeWrapper]").show();

        setDeadLineTime(hours);
        deadlineText.html(hours + "h left");
    }
    else {
        var nowHours = parseInt(moment().hour()) + 1;
        $("[data-deadline]").html(moment(moment(val_date).format('YYYY-MM-DD') + " " + nowHours + ":00").fromNow());
        $("[data-deadlineTimeWrapper]").hide();

        //FinDate=FinDate.add(12, 'hours');
    }

    //calcData.deadline = e.date.toDate();
    //console.log("dateDiff = "+ dateDiff);
    //console.log("StarDate = "+ moment(StarDate).format("DD MM YYYY HH:mm:ss"));
    //console.log("StarDat2 = "+ moment(moment(StarDate.format("YYYY-MM-DD"),"YYYY-MM-DD")).format("DD MM YYYY HH:mm:ss"));
    //console.log("FinDate  = "+ moment(FinDate).format("DD MM YYYY HH:mm:ss"));
    //console.log("DAte2 after = "+ moment(e.date.toDate()).format("DD MM YYYY HH:mm:ss"));
    //calcData.deadline = moment(e.date);
    calcData.deadline = moment(FinDate);
    runCalc(calcData, totalPrice);
}

function RecalcOnlyDate(val_date) {
    var FinDate = moment(moment(val_date).format("YYYY-MM-DD"), "YYYY-MM-DD");
    var StarDate = moment();
    //var dateDiff = moment.duration(StarDate.diff(moment(StarDate.format("YYYY-MM-DD"),"YYYY-MM-DD")));
    var dateDiff = StarDate.diff(moment(StarDate.format("YYYY-MM-DD"), "YYYY-MM-DD"), 'seconds');
    FinDate = FinDate.add(dateDiff, 'seconds');
    if (val_date.format("YYYY-MM-DD") === moment().format("YYYY-MM-DD")) {

        var hours = $("[data-deadlineTimeSelect]").find(":selected").val();
        //var than = moment(moment(e.date).format("YYYY-MM-DD") + " " + hours);
        //var now = moment();

        FinDate = FinDate.add(hours, 'hours');

        $("[data-deadlineTimeWrapper]").show();

        setDeadLineTime(hours);
        deadlineText.html(hours + "h left");
    }
    else {
        var nowHours = parseInt(moment().hour()) + 1;
        //$("[data-deadline]").html(moment(moment(val_date).format('YYYY-MM-DD') + " " + nowHours + ":00").fromNow());
        //$("[data-deadlineTimeWrapper]").hide();

        //FinDate=FinDate.add(12, 'hours');
    }

    //calcData.deadline = e.date.toDate();
    //console.log("dateDiff = "+ dateDiff);
    //console.log("StarDate = "+ moment(StarDate).format("DD MM YYYY HH:mm:ss"));
    //console.log("StarDat2 = "+ moment(moment(StarDate.format("YYYY-MM-DD"),"YYYY-MM-DD")).format("DD MM YYYY HH:mm:ss"));
    //console.log("FinDate  = "+ moment(FinDate).format("DD MM YYYY HH:mm:ss"));
    //console.log("DAte2 after = "+ moment(e.date.toDate()).format("DD MM YYYY HH:mm:ss"));
    //calcData.deadline = moment(e.date);
    calcData.deadline = moment(FinDate);
    runCalc(calcData, totalPrice);
}

//Reset default value of bootstrap datetimepicker
calendarInputMain.val("");

$("[data-deadlineTimeSelect]").change(function () {
    var hours = $(this).find(":selected").val();
    var than;

    than = $(".form-control-deadline").val();

    if (!than) {
        deadlineText.html(hours);
    }
    else {
        setDeadLineTime(hours);
    }
});

//When date is selected in the radio buttons
$('input[name="deadlineTime"]').change(function () {
    inputValue = $(this).val();
    //Days or hours?
    timeType = inputValue.slice(-1);
    //Remove "d" or "h" from date string
    inputValue = inputValue.substr(0, inputValue.length - 1);

    deadlineText.html(
        moment()
            .add(
                inputValue,
                timeType === "d" ? "days" : "hours"
            )
            .calendar()
    );
});


//INDEX PAGE ORDER FORM
$("#pages").change(function () {
    countInput = $(this);
    inputValue = Math.round(countInput.val());

    if (inputValue > 100) {
        countInput.val(100);
        inputValue = Math.round(countInput.val());
    }

    if (isNaN(inputValue) || inputValue < 1) {
        countInput.val(1);
        inputValue = Math.round(countInput.val());
        setPagesCount(countInput.val());
    }
    else {
        setPagesCount(inputValue);
    }

    calcData.pages = countInput.val();
    runCalc(calcData, totalPrice);

    //setPagesCount(inputValue);
});

$("[data-input-action]").click(function (e) {
    element = $(this);

    countInput = element.siblings("[data-count-input]");
    inputValue = Math.round(countInput.val());

    if (element.data('input-action') === "minus") {
        if (inputValue > 1) {
            countInput.val(--inputValue);
        }
    }
    else if (element.data('input-action') === "plus") {
        countInput.val(++inputValue);
    }

    if ($(countInput).attr('id') === "sources") {

        if (isNaN(inputValue) || inputValue < 0) {
            countInput.val(0);
        }

        if (inputValue > 100) {
            countInput.val(100);
        }
    }

    if ($(countInput).attr('id') === "pages") {

        if (inputValue > 100) {
            countInput.val(100);
            inputValue = Math.round(countInput.val());
        }

        if (isNaN(inputValue) || inputValue < 1) {
            countInput.val(1);
            calcData.pages = countInput.val();
            runCalc(calcData, totalPrice);
            setPagesCount(countInput.val());
        }
        else {
            calcData.pages = inputValue;
            runCalc(calcData, totalPrice);
            setPagesCount(inputValue);
        }
        //calcData.pages = inputValue;
        //runCalc(calcData, totalPrice);
        //setPagesCount(inputValue);
    }

    e.preventDefault();
});

$("[name=spaced]").change(function (event) {
    inputValue = Math.round($("#pages").val());
    if (isNaN(inputValue) || inputValue < 1) {
        setPagesCount(1);
    }
    else {
        setPagesCount(inputValue);
    }
});

$("[name=sources]").change(function (event) {
    inputValue = Math.round($("#sources").val());

    if ($.isEmptyObject($("#sources").val())) {
        $("#sources").val(0);
    }

    if (isNaN(inputValue) || inputValue < 0) {
        $("#sources").val(0);
    }

    if (inputValue > 100) {
        $("#sources").val(100);
    }
});

var inputElement;

$("[data-showPassword]").change(function () {
    if (this.checked) {
        inputElement = $(this).parent().parent().find('.form-control[type=password]');
        inputElement
            .clone()
            .prop('type', 'text')
            .insertAfter(inputElement)
            .prev()
            .remove();
    }
    else {
        inputElement = $(this).parent().parent().find('.form-control[type=text]');
        inputElement
            .clone()
            .prop('type', 'password')
            .insertAfter(inputElement)
            .prev()
            .remove();
    }
});

/* $('.paypalbutton').on('click', function( e ) {
 Custombox.open({
 target: '#paypalmodal',
 effect: 'slit',
 overlayClose: false,
 escKey: false
 });
 });*/

$("[data-showLoginModal]").click(function (event) {
    Custombox.open({
        target: '#loginModal',
        effect: 'slit',
        speed: 350,
        overlaySpeed: 150
    });

    event.preventDefault();
});

$("[data-faq] .panel")
    .on('hide.bs.collapse', function () {
        $(this).attr("aria-expanded", "false");
    })
    .on('show.bs.collapse', function () {
        $(this).attr("aria-expanded", "true");
    });

//When payment system is changed
$("[name=paymentType]").change(function (event) {
    $('[data-payment-system]').html($('[name=paymentType]:checked').val());
});

$("[name=academicLevel]").change(function () {
    var value;

    value = $(this).find("option:selected").val();
    if (!value) {
        value = $(this).val();
    }

    calcData.academicLevel = value;
    runCalc(calcData, totalPrice);
});

$("[name=workType]").change(function () {
    calcData.typeOfWork = $(this).val();
    runCalc(calcData, totalPrice);
});

$("[name=spaced]").change(function () {
    calcData.spaced = $(this).val();
    runCalc(calcData, totalPrice);
});


$(window).load(function () {
    /*$('.carousel-reviews .item').carouselHeights();
}).scroll(function (event) {
    onscroll(headerHeightBefore);*/
});

var currentDiscount = true;
$('#appdicount').on('click', function (e) {
    e.preventDefault();
    if(!currentDiscount) {
        return false;
    }
    var el = $(this);
    var curprice = $('[data-total-price]').attr('data-total-price');
    var discountcode = $('#discount').val();
    var formData = "discountcode=" + discountcode;
    var result = "";
    $.ajax(
        {
            url: "/checkdiscount",
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                result = data;
                
                if(result == "0") {
                    ExampleWarning.show("Incorrect discount codе");
                } else {
                    el.attr('data-discount', data).text("You save: $" + (curprice * (result / 100)).toFixed(2)).parent('.switch-inline-input').addClass('discount-done');

                    var totaldisc = (curprice - (curprice * (result / 100))).toFixed(2)
                    
                    $('input[name=xdiscountcode]').val(discountcode);
                    totalPrice.html("Total price: <span class=\"total-price\">$" + totaldisc + "</span>");
                        
                    //chekout.html("<i class='glyphicon glyphicon-refresh glyphicon-spin hide'></i>" + totalPrice.html() + ", CHECK OUT NOW!");
                }
            }
        });
});
//});

function runCalc(calcData, totalPrice) {
    var academicLevel = $('#academLevel').val(),
        deadline = $('#deadlineDate').val(),
        pages = $('#pages').val(),
        spaced = $('select[name=spaced]').val(),
        typeOfWork = $('#workType').val(),
        totalPrice = $('#total-price');

    if (academicLevel >= 0 && pages > 0 && deadline) {
        if (deadline instanceof Date) {
            var deadlineDay = deadline.getDate();
            var deadlineMonth = deadline.getMonth() + 1;
            var deadlineYear = deadline.getFullYear();

            deadline = deadlineYear + "/" + deadlineMonth + "/" + deadlineDay;
        }

        var res = orderCalc(academicLevel, deadline, pages, typeOfWork, spaced).toFixed(2);

        var discount = $('#appdicount').attr('data-discount');
        if(discount) {
            $('#appdicount').text("You save: $" + (res * (discount / 100)).toFixed(2));
            res = (res - (res * (discount / 100))).toFixed(2);
        }
        totalPrice.html(res < 1 ? "Not Available" : "$" + res).attr('data-total-price', res);
        $('.date-contain p.time-date').html(moment(deadline).format('h:mm a dddd Do of MMMM YYYY'));
        chekout.html("<i class='glyphicon glyphicon-refresh glyphicon-spin hide'></i>" + totalPrice.html() + ", CHECK OUT NOW!");
    }
}


function setPagesCount(inputValue, pagesCount) {
    var wordsCount;

    wordsCount = 300;

    //Single spaced
    if ($("select[name=spaced]").val() == 1) {
        wordsCount = 600;
    }

    $("[data-pagesCount]").html(wordsCount * inputValue + " words");
}

function onscroll(headerHeightBefore) {
    if ($(window).scrollTop() > 60) {
        $(".header__top").css('height', 0);
    }
    else if ($(window).scrollTop() === 0) {
        $(".logo").css({
            'z-index': 10
        });
        $(".header__top").css('height', headerHeightBefore);
    }
    else {
        $(".header__top").css('height', headerHeightBefore);
        $(".logo").css({
            'z-index': 1
        });
    }
}

function setDeadLineTime(hours) {
    $("[data-deadlineTime]").html(hours + "h left");
}

function orderFormCalc(date, calcData, deadlineText, totalPrice) {
    var hours;

    var FinDate = moment(moment(date).format("YYYY-MM-DD"), "YYYY-MM-DD");
    var StarDate = moment();
    //var dateDiff = moment.duration(StarDate.diff(moment(StarDate.format("YYYY-MM-DD"),"YYYY-MM-DD")));
    var dateDiff = StarDate.diff(moment(StarDate.format("YYYY-MM-DD"), "YYYY-MM-DD"), 'seconds');
    FinDate = FinDate.add(dateDiff, 'seconds');

    if (date.format("YYYY-MM-DD") === moment().format("YYYY-MM-DD")) {
        hours = $("[data-deadlinetimeselect] option:selected").val();

        $(".select-wrapper").has("[data-deadlinetimeselect]+.bootstrap-select").addClass("visible");

        //date = moment().add(hours, 'h');
        FinDate = FinDate.add(hours, 'h');

        //deadlineText.html(date.calendar());
        //console.log(moment(date).format('LLLL'));
        deadlineText.html("Tomorrow, " + moment(FinDate).format('MMMM D, YYYY h:mm A'));
        $('input[name="xhoures"]').val(hours);

        //console.log("1 date.toDate() "+date.toDate());
        //calcData.deadline = date.toDate();
        calcData.deadline = moment(FinDate);
    }
    else {
        $(".select-wrapper").has("[data-deadlinetimeselect]+.bootstrap-select").removeClass("visible");

        date.set('hour', moment().hour());
        date.set('minutes', moment().minutes());

        //deadlineText.html(moment(date).calendar());
        deadlineText.html(moment(FinDate).format('h:mm A, dddd, Do') + ' of ' + moment(FinDate).format('MMMM, YYYY'));
        //console.log(moment(date).format('h:mm A, dddd, Do MMMM, YYYY'));
        $('input[name="xhoures"]').val(0);

        //console.log("2 date.toDate() "+date.toDate());
        //calcData.deadline = date.toDate();
        calcData.deadline = moment(FinDate);
    }

    //console.log("dateDiff = "+ dateDiff);
    //console.log("StarDate = "+ moment(StarDate).format("DD MM YYYY HH:mm:ss"));
    //console.log("StarDat2 = "+ moment(moment(StarDate.format("YYYY-MM-DD"),"YYYY-MM-DD")).format("DD MM YYYY HH:mm:ss"));
    //console.log("FinDate  = "+ moment(FinDate).format("DD MM YYYY HH:mm:ss"));

    runCalc(calcData, totalPrice);

}

$(document).ready(function () {
    //set initial state.
    $('#accept_chb').change(function () {
        if ($(this).is(":checked")) {
            //$('a.btn.ordermodal').prop('disabled', false);
            $('a.btn.acceptfororder').removeClass('notAccept');
        }
        else {
            //$('a.btn.ordermodal').prop('disabled', true);
            $('a.btn.acceptfororder').addClass('notAccept');
        }
    });
});
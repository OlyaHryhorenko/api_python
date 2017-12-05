//from expensive to cheap ->

//Prices for writing from scratch
var pricesScratch = {
    //FORMAT: day, 2 days, 3 days, 5 days, 7 days, 14 days, 21 days, 30 days
    //HIGH SCHOOL
    1: [23.00, 20.50, 18.50, 16.50, 15.00, 13.50, 12.50, 11.50],
    //COLLEGE
    2: [26.00, 23.00, 21.00, 19.00, 17.50, 16.00, 15.00, 14.00],
    //UNIVERSITY
    3: [29.00, 26.00, 23.50, 21.50, 20.00, 18.50, 17.50, 16.50],
    //Master
    4: [38.00, 34.00, 30.50, 27.50, 25.00, 23.00, 21.00, 19.00],
    //PH.D.
    5: [null, null, 36.00, 33.00, 30.00, 27.50, 25.00, 23.00],
};

//Prices for editing
var pricesEditing = {
    //FORMAT: day, 2 days, 3 days, 5 days, 7 days, 14 days, 21 days, 30 days
    //HIGH SCHOOL
    1: [11.00, 10.00, 9.00, 8.00, 7.00, 6.00, 5.00, 4.00],
    //COLLEGE
    2: [14.00, 12.00, 10.00, 9.00, 8.00, 7.00, 6.00, 5.00],
    //UNIVERSITY
    3: [16.00, 14.00, 12.00, 10.00, 9.00, 8.00, 7.00, 6.00],
    //MASTER’S
    4: [20.00, 17.00, 15.00, 13.00, 11.00, 10.00, 9.00, 8.00],
    //Phd
    5: [24.00, 21.00, 18.00, 16.00, 14.00, 12.00, 11.00, 10.00],
};

var urgencyData = [
    //60 seconds * 60 minutes * 24 = 86400 = day
    43200, //12 hours
    86400, //24 hours
    86400 * 2, //2 days
    86400 * 3, //3 days
    86400 * 5, //5 days
    86400 * 7, //7 days
    86400 * 9, //9 days
    86400 * 10, //10 days
];

/**
 *
 * @param level int
 * @param deadline string
 * @param pages int
 * @param typeOfWork string
 * @param spaced int
 * @returns float
 */
function orderCalc(level, deadline, pages, typeOfWork, spaced) { 
    var urgency, totalPrice, new_urgency, new_typeOfWork;
    
    urgency = getUrgency(deadline);

    //Type of work - Writing from scratch
    if (typeOfWork == 1) {
        totalPrice = pricesScratch[level][urgency] * pages;
    }
    else {
        //Type of work - Editing
        totalPrice = pricesEditing[level][urgency] * pages;
    }

    //If single spaced
    if (spaced == 1) {
        totalPrice *= 2;
    }

    new_urgency=urgency
    //console.log("urgency "+urgency);
    if (urgency == 4) new_urgency=5;
    if (urgency == 5) new_urgency=7;
    if (urgency == 6) new_urgency=9;
    if (urgency == 7) new_urgency=30;
    if (typeOfWork == 2) new_typeOfWork=1;
    if (typeOfWork == 1) new_typeOfWork=2;
    if (typeOfWork == 3) {new_typeOfWork=3; spaced=2;}
    //$.PrcWrk(level, new_urgency, pages, new_typeOfWork);
    //$.PrcSpace(spaced);
    //console.log("totalPrice= "+($.PrcWrk(level, new_urgency, pages, new_typeOfWork))*($.PrcSpace(spaced)));
    //totalPrice=($.PrcWrk(level, new_urgency, pages, new_typeOfWork))*($.PrcSpace(spaced));
    
    //console.log("new_urgency "+new_urgency);
    totalPrice=(PrcWrk(level, new_urgency, pages, new_typeOfWork))*(PrcSpace(spaced));
    return totalPrice;
}

/**
 * @param deadline int
 * @return int
 */
function getUrgency(deadline) {
    var time, urgency = 0, urgencyLength;

    urgencyLength = urgencyData.length - 1;
    console.log("deadline "+deadline);
    console.log("Date now "+(new Date));
    time = +new Date(deadline).getTime();
    console.log("time  "+moment(time).format("DD MM YYYY HH:mm:ss"));
    time2 = +new Date().getTime();
    console.log("time2 "+moment(time2).format("DD MM YYYY HH:mm:ss"));
    time = (time - (+new Date)) / 1000;
    console.log("new time "+time);
    if (time < 0) {
        time = 0; // or alarma =)
    }

    if (time > urgencyData[urgencyLength]) {
        urgency = urgencyLength;
    }
    else {
        $.each(urgencyData, function (key, value) {
            if (time < value) {
                urgency = parseInt(key);
                return false;
            }
        });
    }

    return urgency;
}
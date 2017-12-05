//$(function () {
//  $(document).ready(function() {
    $prc_data =[];

    function GetListPrise () {
        var data = {}; // data
        data['price_on_date'] = moment().format('YYYY-MM-DD');
        $.ajax({
            url: 'https://api.bryteq.com/utils',
            type: 'POST',
            async: false,
            data: JSON.stringify(data),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            contentType: 'application/json;charset=UTF-8',
            success: function(datarecived){
                $prc_data=datarecived;
            },
            error: function(error) {
                console.log("error");
                console.log(error);
            }
        });
    };

    GetListPrise();
 //});

//$(document).ready(function() {
    function PrcWrk (level, deadline, pages, typeOfWork){
        //console.log("pages = "+pages);
        //console.log($prc_data);
        if (!jQuery.isEmptyObject($prc_data)){
            for (var i=0; i<$prc_data.result.length; i++){
                //console.log($prc_data.result[i]);
                if (($prc_data.result[i].id_table == typeOfWork) && ($prc_data.result[i].format == level) && ($prc_data.result[i].urgenc == deadline)) 
                {
                    //console.log(pages*$prc_data.result[i].price);
                    //console.log("id_table="+typeOfWork+" format="+level+" urgenc="+deadline);
                    return pages*$prc_data.result[i].price;
                }
            }
        }
        return 0;
    };

    function PrcSpace (space){
        //console.log("PrcSpace");
        if (!jQuery.isEmptyObject($prc_data)){
            for (var i=0; i<$prc_data.result2.length; i++){
                if ($prc_data.result2[i].countspace == space) 
                {
                    return $prc_data.result2[i].kof;
                }
            }
        }
        return 1;
    };

    function GetDefPlaceholder (text_for_placeholder) {
        if (!jQuery.isEmptyObject(text_for_placeholder)){
            return text_for_placeholder[Math.floor(Math.random()*text_for_placeholder.length)];
        }
        return "";
    };

    $('.info_label').tooltip({
        animation: true,
        placement: 'bottom',
        container: 'body'}).on('shown.bs.tooltip', function (e) {
            var trg = e.target
            if('ontouchstart' in window)
            {
                setTimeout(function() {
                    $(trg).tooltip('hide');
                },1500);
            }
        });

    $('.info_label').on('tooltip', function() {
        console.log(1);
    });

    $('.info_label2').tooltip({
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

    $('.info_label3').tooltip({
        placement: 'top',
        animation: false,
        trigger: 'hover click',
        container: 'body'});

//});

//$(function() {
    function SetDefAcademLevel (id,def) {
        def = def|| 2;
        console.log("id="+id);
        //console.log("def="+def);
        if (id > 0)
        {
            $("select[name='academicLevel']").val(id);
        }
        else
        {
            $("select[name='academicLevel']").val(def);
        }

        //console.log($("[name=academicLevel]:checked").val());
    };

    function SetDefPaperFormat (id,def) {
        def = def|| 2;
        console.log("SetDefPaperFormat id="+id);
        //console.log("SetDefPaperFormat def="+def);
        $("select[name='paperFormat']").val(id);
        
    };

    function SetDefDedline (date_val,def) {
        def = def|| 8;
        var DateNow=Date();
        console.log("date_val="+date_val);
        //console.log("def="+def);
        if (date_val != "")
        {
            $("#deadlineDate").val(moment(date_val,"YYYY-MM-DD").format("YYYY-MM-DD")).change();
        }
        else
        {
            //console.log(moment().add(def,'days').format("YYYY-MM-DD"));
            $("#deadlineDate").val(moment().add(def,'days').format("YYYY-MM-DD")).change();
        }
    };

//});
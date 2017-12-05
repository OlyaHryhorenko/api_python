function SendYandMetrik (targ,data) {
        //console.log("target= "+targ);
        var data_metrik = {}; // data
        for(var i in data){
          data_metrik[i]= data[i];
          //console.log("key= "+i+" Value= "+data_metrik[i]);
        }
        //console.log(data_metrik);
        //yaCounter25694771.reachGoal(targ, JSON.stringify(data_metrik), goalCallback);
        //console.log(data_metrik);
        window.dataLayer = window.dataLayer || [];
        console.log(window.dataLayer.push({
                                  "ecommerce": {
                                                "purchase": {
                                                    "actionField": {
                                                        "id" : targ,
                                                    },
                                                    "products": [
                                                        data_metrik
                                                    ]
                                                }
                                            }
                              })
        );
        goalCallback ();
        console.log(targ);
        console.log(data_metrik);
    }


    function goalCallback () {
        console.log('запрос в Метрику успешно отправлен');
    }

  function getParameterByName(name, url) {
      if (!url) url = window.location.href;
      name = name.replace(/[\[\]]/g, "\\$&");
      var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
          results = regex.exec(url);
      if (!results) return null;
      if (!results[2]) return '';
      return decodeURIComponent(results[2].replace(/\+/g, " "));
  }
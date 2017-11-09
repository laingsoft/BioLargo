// Experiment Javascript
function makeMetadata(data){
    table = $("#metadata-table");
    row = $('<tr></tr>')
    $.each(data, function(key, obj){
        
        $('<td></td>',{text:key}).appendTo(row);
    })
    row.appendTo(table);
    row = $('<tr></tr>')
    $.each(data, function(key, obj){
        
        $('<td></td>',{text:obj}).appendTo(row);
    })
    row.appendTo(table);
    

}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteExperiment(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings){
            if(!this.crossDomain){
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });
    $. ajax({
        type: 'POST',
        url: "/app/experimentrm/"+id,
        dataType: 'json',
        success: function(data) {
            // console.log(data);
            if(data.result){
                window.location = '/app/';
            }
        }
    })

}

function makeTable(jsondata){
    table = jQuery("#experimental-data"), row = null, data = null;
    console.log(jsondata);
    //$.each(jsondata, function(key, obj){ $.each(jsondata, function(k, v){ console.log(v)})});
    makeHeaders(jsondata, table);
    $.each(jsondata, function(key, obj){
        row = $('<tr></tr>'); // Create a new row
        $.each(obj, function(k, v){
            $('<td></td>',{text:v}).appendTo(row);
        });
        row.appendTo(table);
    });
}

function makeHeaders(jsondata, table){
    console.log(jsondata);
    row = $('<tr></tr>');
    for (prop in jsondata[0]){
        //console.log(prop);
        $('<th></th>',{text:prop}).appendTo(row);
    }
    row.appendTo(table);


}

function makeChart(jsondata){
    var time = [];
    var removal = [];
    var test = [1,2,3,4,5,6,7,8,9,5,4,2,7,8];
    $.each(jsondata, function(key, obj){
        time.push(obj["Time [min]"]);
        removal.push(Math.log(obj["StockCFU [CFU/mL]"]) - Math.log(obj["RemainingCFU [CFU/mL]"]));
    });
    console.log(removal)
    var ctx = document.getElementById("removalChart");
    var removalChart = new Chart(ctx, {
        type: 'line',
        
        data: {
            labels:time,
            datasets:[
                {
                    label: "Stock / Remaining (log10)",
                    data:removal,
                }
            ]
        }
        
    });
}
$.ajax({
    url: "/app/experimentjs/"+id,
    dataType: 'json',
    success: function(data) {
       // console.log(data);
        makeTable(data);
        makeChart(data);
        makeMetadata(metadata)
    }
});



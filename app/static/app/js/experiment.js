// Experiment Javascript

function deleteExperiment(){
    alert('test');

}

function makeTable(jsondata){
    table = jQuery("#experimental-data"), row = null, data = null;
    //console.log(jsondata);
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
    }
});



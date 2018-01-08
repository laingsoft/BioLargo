var metadata = JSON.parse(metadata_field.val());

Object.keys(metadata).forEach(function(key){
   var label = document.createElement("span");
   label.innerHTML = key;

   var field = document.createElement("input");
   field.value = metadata[key];
   field.setAttribute("class", "form-control metadata_field");
   field.setAttribute("placeholder", key)

   $("#metadata_fields").append(label, field);
});

var container = document.getElementById("hot");


if (!headers){ headers = [''] };

var options = {data: data,
    colHeaders: headers,
    rowHeaders: true,
    contextMenu: true,
    preventOverflow: 'horizontal',
    manualRowMove: true,
};

var hot = new Handsontable(container, options);

$("#exp_form").submit(function(e){
    $("#exp_data").val(JSON.stringify(hot.getSourceData()));

    $(".metadata_field").each(function(i){
        metadata[Object.keys(metadata)[i]] = $(this).val()
    });

    metadata_field.val(JSON.stringify(metadata));
});

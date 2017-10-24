var CONTAINER = $('#experiments')
var fields;

$.get("/app/get_metadata_template", {}, function(result){
    fields = result.data.map(function(f){
        return {name: f, type: "text", title: f}
        });
        
    fields.push({type: "control", itemTemplate: null})
    
    CONTAINER.jsGrid({
    width: "100%",
    filtering : true,
    sorting: true,
    pageLoading: true,
    paging: true,
    autoload: true,
    noDataContent: "No experiments found",
    
    
    controller: {
        loadData:   function(filter){
                var data;
                
                request = $.get("/app/experiments_list", filter, function(response){
                        data = response;
                    });
                    
                return request.promise()
        }
    },

    fields: fields,
    rowClick: function(item){
        window.location.href = "/app/experiment/" + item.item.id.toString();
    }
    });

    });



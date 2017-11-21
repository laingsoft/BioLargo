var CONTAINER = $('#experiments')
var fields;


function format_filter(filter){
    keys = Object.keys(filter);
    metadata_filters = [];
    filter_new = {}
    
    //~ id is always the first item
    id = filter.id;
    keys.shift();
    filter_new['id'] = id;
    
    if (filter.hasOwnProperty('sortField')){
        keys.splice(-2,2)
        filter_new['sortOrder'] = filter.sortOrder;
        filter_new['sortField'] = filter.sortField;
    }
    
    
    //~ remove pageSize and pageIndex from the end.
    filter_new['pageSize'] = filter.pageSize;
    filter_new['pageIndex'] = filter.pageIndex;
    
    keys.splice(-2, 2);
    
    if (filter.hasOwnProperty('experiment_data_filters')){
        filter_new['experiment_data_filters'] = filters.experiment_data_filters;
        keys.pop();
    }

    for(var i = 0; i < keys.length; i++){
        if (filter[keys[i]] !== ''){
            metadata_filters.push(keys[i]+'='+filter[keys[i]]) };
    }
    filter_new['metadata_filters'] = metadata_filters
    
    return filter_new;
}

$.get("/app/get_metadata_template", {}, function(result){
    fields = result.data.map(function(f){
        return {name: f, type: "text", title: f}
        });
           
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
            console.log(filter)
            var data;
            filter = format_filter(filter)
            console.log(filter)
            
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




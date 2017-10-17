var CONTAINER = $('#experiments')


CONTAINER.jsGrid({
    width: "100%",
    filtering : true,
    sorting: true,
    pageLoading: true,
    paging: true,
    autoload: true,
    
    controller: {
        loadData:   function(filter){
                var data;
                
                request = $.get("/app/experiments_list", filter, function(response){
                        data = response;
                    });
                    
                return request.promise()
        }
    },

    fields: [
        {name: "id", type:"number", align: "", title: "ID"},
        {name: "num_chambers", type:"number", align: "", title: "Chambers"},
        {name: "reactor_diameter", type:"number", align: "", title: "Diameter"},
        {name: "reactor_length", type:"number", align: "", title: "Length"},
        {name: "removal_target", type:"text", align: "", title: "Target"},
        {name: "reactor_age", type:"number", align: "", title: "Age (ml)"},
        {name: "group__name", type:"text", align: "", title: "Group"},
        {name: "tags", type:"text", align: "", title: "Tags"},
    ],
    
    rowClick: function(item){
        window.location.href = "/app/experiment/" + item.item.id.toString();
    }
});

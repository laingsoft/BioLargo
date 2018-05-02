var tour = {
    id: "experiment-tour",
    steps:[
	{
	    title: "Meta-information",
	    content: "This section shows the meta-information of the file",
	    target: "metadatacard",
	    placement: "top",
	},
	{
	    title: "Comments",
	    content: "This section allows you to make comments on an experiment. Comments are usually used to track information that wouldn't normally be included in the raw data.",
	    target: "commentLink",
	    placement: "bottom",
	    onShow: function () {
		$("#commentLink").click();
	    }
	},
	{
	    title: "Comment Box",
	    content: "You can try writing a comment here.",
	    target: "newCommentInput",
	    placement: "left",
	},
	{
	    title: "Raw Data",
	    content: "Using this tab, you can see the raw data.",
	    target: "dataLink",
	    placement: "bottom",
	    onShow: function(){
		$("#dataLink").click();
	    }
	},
	{
	    title:"Settings",
	    content: "All of your experiment-specific settings will be here.",
	    target: "settingsLink",
	    placement:"bottom",
	    onShow: function(){
		$("#settingsLink").click();
	    }
	}
    ]
}
	

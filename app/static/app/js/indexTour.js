var tour = {
    id: "hello-pasteur",
    steps:[
	{
	    title:"At a Glance",
	    content:"These are your At-a-glance settings. They will tell you basic information about the lab",
	    target:"stats",
	    placement:"right"
	},
	{
	    title:"Navigation Bar",
	    content:"This is your navigation bar, It will let you move around the site",
	    target:"tour-sidebar",
	    placement:"right"
	},
	
	{
	    title:"Navigation Bar",
	    content:"This is your navigation bar",
	    target:"tour-user-stop",
	    placement:"left",
	    onShow: function() {
		$("#tour-dropdown").addClass("show");
		$("#tour-hidden-menu").addClass("show");
	    }
	    
	},
	{
	    title:"Management Panel",
	    content:"This is the management panel",
	    target:"tour-management-stop",
	    placement:"left"
	}
	
    ]
};

	    

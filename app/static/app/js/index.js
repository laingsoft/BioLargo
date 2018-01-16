/*
* Fills in the "Most Active Users Graph
* Sister function is located in consumers: getUploadsPerUser
*
*/

function showUserStats(data){
   // console.log(data);
    var exp_data = [{
        type: 'line',
        x: Object.keys(data),
        y: Object.values(data)

    }]

    var exp_layout = {
        title: "Number of Experiments uploaded",
        height: 200,
        margin: {
            l: 60,
            r: 60,
            b: 30,
            t: 30,

        },

        xaxis: {
            showgrid: false,
            fixedrange: true
        },
        yaxis: {
            showgrid: false,
            fixedrange: true
        },


    }

    Plotly.newPlot('num_exp', exp_data, exp_layout, { displayModeBar: false });

};

/*
* Fills in the "Number of experiments uploaded" graph
* Sister function is in consumers.py: getUserStats
*
*/

function showUserUploadGraph(data){
    console.log(data);
    var user_data = [{
        type: 'bar',
        x: Object.values(data),
        y: Object.keys(data),
        orientation: 'h',
    }];

    var user_layout = {
        title: "Most Active Users",
        height: 200,
        margin: {
            l: 60,
            r: 60,
            b: 30,
            t: 30,
            pad: 0

        },
        xaxis: {
            showgrid: false,
            fixedrange: true
        },
        yaxis: {
            showgrid: false,
            fixedrange: true
        },

    }

    Plotly.newPlot('active_users', user_data, user_layout, { displayModeBar: false });
}

// ACTIONS is the dispacher graph. Register the functions you want to use here.
var ACTIONS = {'userstats': showUserStats, "showUserUploadGraph":showUserUploadGraph};

/*
* Dispacher function. Uses the data sent from the server to tell the client what to do with
* the data.
*/
function socket_dispach(e){
    console.log("Recieved: "+e.data);
    recv = JSON.parse(e.data);
    ACTIONS[recv['action']](recv['data']);
};


$(document).ready(function() {
    // Do some basic setup stuff
    // Basically just everything that needs to be done on the page. Perhaps think
    // about using a loader so the page doesn't seem lethargic.
    socket = new WebSocket("ws://"+window.location.host+window.location.pathname);
    socket.onmessage = function(e){
        socket_dispach(e);
    }
    socket.onopen = function(){
	socket.send(JSON.stringify({'action':'getUploadsPerUser', 'data':0}));
        socket.send(JSON.stringify({'action':'getUserStats', 'data':0}));

	console.log("sent");
    }


$(".clickable").click(function(){
window.location.href="/app/experiment/" + $(this).data('id')
})

})


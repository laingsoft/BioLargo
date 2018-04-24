/*
 * Fills in the "Most Active Users Graph
 * Sister function is located in consumers: getUploadsPerUser
 *
 */

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

function showUserStats(data) {
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

function showUserUploadGraph(data) {
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
var ACTIONS = { 'get_daily_upload_stats': showUserStats, "get_top_uploaders": showUserUploadGraph };

/*
 * Dispacher function. Uses the data sent from the server to tell the client what to do with
 * the data.
 */
function socket_dispach(e) {
    recv = JSON.parse(e.data);
    ACTIONS[recv['action']](recv['data']);
};

function set_tutorial_val(val){
    var csrftoken = getCookie('csrftoken')
    $.ajax({
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        url: "/api/set_tutorial/",
        dataType: 'json',
        method: 'POST',
        data: {"val": val},
        success: function(data) {
	    console.log("tutorial status updated");

        }
    });
}


$(document).ready(function() {
    // Do some basic setup stuff
    // Basically just everything that needs to be done on the page. Perhaps think
    // about using a loader so the page doesn't seem lethargic.
    socket = new WebSocket("ws://" + window.location.host + window.location.pathname);
    socket.onmessage = function(event) {
        socket_dispach(event);
    }
    socket.onopen = function() {
        socket.send(JSON.stringify({ 'action': 'get_daily_upload_stats' }));
        socket.send(JSON.stringify({ 'action': 'get_top_uploaders' }));
    }


    $(".clickable").click(function() {
        window.location.href = "/app/experiment/" + $(this).data('id')
    })

    //Show the tutorial
    if (show_tutorial){
	hopscotch.startTour(tour);
    }
    

})



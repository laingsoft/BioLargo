function showUserStats(data){
    console.log(data);
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

var ACTIONS = {'userstats': showUserStats};

function socket_dispach(e){
    console.log("Recieved: "+e.data);
    recv = JSON.parse(e.data);
    ACTIONS[recv['action']](recv['data']);
};


$(document).ready(function() {
    socket = new WebSocket("ws://"+window.location.host+window.location.pathname);
    socket.onmessage = function(e){
        socket_dispach(e);
    }
    socket.onopen = function(){
        console.log("sent");
        socket.send(JSON.stringify({'action':'getUserStats', 'data':0}))
    }

    $("tr").click(function() {
        console.log("clicked") // Change when we figure out how we're accessing experiments.
    })

    var user_data = [{
        type: 'bar',
        x: [5, 7, 7, 8, 12],
        y: ['User E', 'User D', 'User C', 'User B', 'User A'],
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
    

    
})


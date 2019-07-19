// Daniel Castillo formatted by Donald Collett
// Leaflet Map in Electron ish

var app = {
    cleanData     : [],
    retGPS        : [],
    ws            : new WebSocket('ws://localhost:8000'),
    j             : 0,
    alllatlongs   : [],
    directions    : [],
    foundLatLons  : [],
    map           : L.map('mymap').setView([0, 0], 15),
    progressBar   : $("#bar")
};

///////////////////////////////////////////////////////////////////////////////
// Websocket part of the code
//////////////////////////////////////////////////////////////////////////////

app.ws.onopen = function(event)
{
        console.log('connected')
}

app.ws.onmessage = function(event) 
{ 
        console.log("WebSocket message received");
        mapping(event.data);//get and concatenate the data
}

app.ws.onclose = function(event)
{
        console.log('connection closed')
}

//////////////////////////////////////////////////////////////////////////////////

function req0()
{
        console.log("sent")
        app.ws.send("0")
        var progressBar = $("#bar");
        countNumbers(progressBar);
}

function req1()
{
        console.log("sent")
        app.ws.send("1")
        
}

function req2()
{
        console.log("sent")
        app.ws.send("2")

}

//////////////////////////////////////////////////////////////////////////////////

function countNumbers(progressBar){

        var i = 0;

        if(i < 100){

            i = i + 1;

            progressBar.css("width", i + "%");
        }
        console.log(app.j)
        countNumbers();
}

function countNumbers(){
        //console.log("In count numbers");
        var element = document.getElementById("myprogressBar");
        var width = 1;
        var identity = setInterval(scene, 100);
        function scene(){
                if (width >= 100){
                        clearInterval(identity);
                } else {
                        width++;
                        element.style.width = width + '%';
                        element.innerHTML = width * 1 + '%'; //adds number to progress bar
                }
        }

        // Wait for sometime before running this script again

        //setTimeout("countNumbers()", 1);

    }

///////////////////////////////////////////////////////////////////

function passData(){
        // Leaflet Map Setup
        
        //app.map = L.map('mymap').setView([app.retGPS[0], app.retGPS[1]], 15);
        // Putting all of it into the tables

        document.getElementById('gpsData')
                .appendChild(populateTable(null, 3, app.j, app.alllatlongs)); 

        document.getElementById('directionData')
                .appendChild(populateTable(null, 3, app.j, app.direcDat));  

       document.getElementById('mymap').appendChild(mapping());

}

function mapping(points){

        app.map.setView([app.retGPS[0], app.retGPS[1]], 15)        
        
        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', 
        {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 50,
                id: 'mapbox.streets',
                accessToken: 'pk.eyJ1IjoiZGFub3JvOTYiLCJhIjoiY2p4ZGh4Zjh1MGViZzNubWY4dTRnbndpYiJ9.RlCJaOdgY9VQusXRfICljw'
        }).addTo(app.map);

        var item = points[points.length - 1]

        var lat = parseFloat(item[0]);
        var lng = parseFloat(item[1]);

        L.marker([lat, lng], {color: 'red'}).addTo(app.map); // plotting thw lasdt point a different color

        // Actual plotting
        var array = [];

        for (var i = 0; i < points.length - 1; i++) {
                var item = points[i]

                var lat = parseFloat(item[0]);
                var lng = parseFloat(item[1]);

                L.marker([lat, lng], {color: 'blue'}).addTo(app.map);
        }

        return app.map
}

////////////////////////////////////////////////////////////////

// Function for adding elements to table dynamically

function populateTable(table, rows, cells, content) 
{
        var is_func = (typeof content === 'function');
        if (!table) table = document.createElement('table');
                for (var i = 0; i < rows; ++i) 
                {
                        var row = document.createElement('tr');
                        for (var j = 0; j < cells; ++j) 
                        {
                                row.appendChild(document.createElement('td'));
                                var text = !is_func ? (content + '') : content(table, i, j);
                                row.cells[j].appendChild(document.createTextNode(text));
                        }
                        table.appendChild(row);
                }
        return table;
}

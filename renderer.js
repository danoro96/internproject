// Daniel Castillo 
// Leaflet Map in Electron

var app = {
    cleanData     : [],
    retGPS        : [],
    ws            : new WebSocket('ws://localhost:8000'),
    j             : 0,
    alllatlongs   : [],
    directions    : [],
    foundLatLons  : [] };

///////////////////////////////////////////////////

app.ws.onopen = function(event){
console.log('connected')
}

app.ws.onmessage = function(event) { 

app.j++

console.log("WebSocket message received");
app.cleanData.push(event.data);//get and concatenate the data


if (app.cleanData.length > 1){ 
app.retGPS = getData(app.cleanData, app.j);      // Analize the data and plot

// Leaflet Map Setup
var map = L.map('map',{center: [app.retGPS[0], app.retGPS[1]], zoom:15});

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
maxZoom: 50,
id: 'mapbox.streets',
accessToken: 'pk.eyJ1IjoiZGFub3JvOTYiLCJhIjoiY2p4ZGh4Zjh1MGViZzNubWY4dTRnbndpYiJ9.RlCJaOdgY9VQusXRfICljw'
}).addTo(map);


for (var i = 0; i = j; i++){

latlngs = app.alllatlongs[i];
// loop to put all markers and polylines
// Here go the markers

markers(latlngs);

// Here go the polylines

polyline(latlngs);

// Putting all of it into the tables

document.getElementById('gpsData')
        .appendChild(populateTable(null, 3, app.j, app.alllatlongs)); 

document.getElementById('directionData')
        .appendChild(populateTable(null, 3, app.j, app.direcDat));

        }
    }
}

app.ws.onclose = function(event){

console.log('connection closed')
}

function req(){
console.log("sent")
app.ws.send("0")
// console.log("after")
}


//////////////////////////////////////////////////////////////////////////////////

function getData(cleanData, j){

var cleanData1 = cleanData[j-2].split(",");
var cleanData2 = cleanData[1].split(",");


var  gpsLat = parseFloat(cleanData1[0]); // at 0
var  gpsLong = parseFloat(cleanData1[1]); // at 1

var lat = parseFloat(cleanData2[0]); // at 0
var long = parseFloat(cleanData2[1]); // at 1


var angleTru1 = parseFloat(cleanData1[6]); // at 10
var angleTru2 = parseFloat(cleanData2[6]);  // at 10

var lineArray = [];
var angleArray = [];

// Put both the angle variables into an array for later use
angleArray.push(math.tan(math.unit(angleTru1, 'deg')));
angleArray.push(math.tan(math.unit(angleTru2, 'deg')));

// Start analysis for position of thrid GPS point

lineArray.push(angleArray[0]*(gpsLong-long) + (gpsLat-lat));

var a = [[angleArray[0], -1], [angleArray[1], -1]];
var b = [[lineArray[0]], [0]];
var coords = math.usolve(a, b);

var cor0 = coords[0];
var cor1 = coords[1];

var latNew = math.sum([lat, cor1]);
var longNew = math.sum([long, cor0]);

// Variable Setup for plot

var lat1  = lat;
var lon1  = long;
var lat2  = gpsLat;
var lon2  = gpsLong;
var latNu = latNew;
var lonNu = longNew;

// create a red polyline from an array of LatLng points
var latlngs = [lat1, lon1, latNu, lonNu, lat2, lon2];

app.alllatlongs.push.latlngs;

nu = [latNu, lonNu]

app.foundLatLons.push.nu;

console.log(latlngs);

return latlngs

}

////////////////////////////////////////////////////////////////

// Function for adding elements to table dynamically

function populateTable(table, rows, cells, content) {
var is_func = (typeof content === 'function');
if (!table) table = document.createElement('table');
for (var i = 0; i < rows; ++i) {
var row = document.createElement('tr');
for (var j = 0; j < cells; ++j) {
    row.appendChild(document.createElement('td'));
    var text = !is_func ? (content + '') : content(table, i, j);
    row.cells[j].appendChild(document.createTextNode(text));
}
table.appendChild(row);
}
return table;
}

////////////////////////////////////////////////////////////////


function markers(latlngs){

lat1  = latlngs[0];
lon1  = latlngs[1]; 
latNu = latlngs[2];  
lonNu = latlngs[3]; 
lat2  = latlngs[4];
lon2  = latlngs[5];

// Setting the markers 
L.marker([lat1, lon1]).addTo(map); // marker 1
L.marker([lat2, lon2]).addTo(map); // marker 2
L.marker([latNu, lonNu]).addTo(map); // marker 3

}

////////////////////////////////////////////////////////////////

function polyline(latlngs){

latlngs = [[latlngs[0], latlngs[1]], [latlngs[2], latlngs[3]], [latlngs[4], latlngs[5]]];

// Creating the line
L.polyline(latlngs, {color: 'red'}).addTo(map);

// Getting the map to shoe exactly the area where the points are
map.fitBounds(polyline.getBounds());

}
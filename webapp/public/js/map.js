var map = null;
var center = null;
var markers = new Array();

function drawMap(center_coords, center_name, places_coords, places_names, start) {
    if (GBrowserIsCompatible()) {
        map = new GMap2(document.getElementById("map_canvas"));
        map.setUIToDefault();
        var baseIcon = createBaseIcon();
        var latlngbounds = new GLatLngBounds();
        
        var centerlatlng = new GLatLng(center_coords[0], center_coords[1]);
        placeCenter(centerlatlng, center_name, baseIcon);
        latlngbounds.extend(centerlatlng);
        
        for (var i=0; i<places_coords.length; i++) {
            var latlng = new GLatLng(places_coords[i][0], places_coords[i][1]);
            latlngbounds.extend(latlng);
            
            var markerOptions = getMarkerOptions(start, i, baseIcon);
            var marker = createMarker(latlng, places_names[i], markerOptions);
            markers.push(marker);
            
            map.addOverlay(marker);
        }
        
        var zoomlevel = (places_coords.length == 0) ? 3 : map.getBoundsZoomLevel(latlngbounds);
        map.setCenter(centerlatlng, zoomlevel);
    }
}

function placeCenter(centerlatlng, center_name, baseIcon) {
    baseIcon.image = "/img/orangeblank.png";    
    var markerOptions = {icon: baseIcon};
    center = createMarker(centerlatlng, center_name, markerOptions);
    map.addOverlay(center);
}

function createBaseIcon() {
    var baseIcon = new GIcon(G_DEFAULT_ICON);
    baseIcon.shadow = null;
    baseIcon.iconSize = new GSize(24, 27);
    baseIcon.iconAnchor = new GPoint(9, 34);
    baseIcon.infoWindowAnchor = new GPoint(9, 2);
    return baseIcon
}

function getMarkerOptions(start, i, baseIcon) {
    var num = start + i + 1;
    var pnum = (num < 10) ? ('0' + num) : num;
    var pnum = (num > 100) ? ('blank') : pnum;
    baseIcon.image = "http://google-maps-icons.googlecode.com/files/red" + pnum + ".png";    
    return {icon: baseIcon}
}

function createMarker(latlng, info, options) {
    var marker = new GMarker(latlng, options);
    GEvent.addListener(marker, 'click', function() {
        var html = '<div style="padding:15px;">'+info+'</div>';
        marker.openInfoWindowHtml(html);
    });
    return marker;
}

function showInfoWindow(i) {
    if (i == -1) {
        GEvent.trigger(center, 'click');
    } else {
        GEvent.trigger(markers[i], 'click');
    }
}

function getLatLng(address) {
    var geocoder = new GClientGeocoder();
    return geocoder.getLatLng(address, function(point) {return point});
}
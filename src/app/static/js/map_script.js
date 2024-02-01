function fetchEventsAndInitMap() {
    var queryObject = (typeof query === 'string') ? JSON.parse(query) : query;

    var queryString = Object.keys(queryObject).map(key => {
        return encodeURIComponent(key) + '=' + encodeURIComponent(queryObject[key]);
    }).join('&');

    var url = '/get_events'
    if (queryString) {
        url += '?' + queryString;
    }

    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(events => {
        if (events.length === 0) {
            document.getElementById('map').innerHTML = '<h1 style="grid-column: span 3; text-align: center; font-size: 24px;">¡No se han encontrado eventos con los parámetros especificados!</h1>' +
            '<img src="/static/images/rsz_no_results_found.png" alt="No events found" style="grid-column: span 3; display: block; margin: auto; height: auto;">';
            return;
        }else{
            initMap(events);
        }
    })
    .catch(error => {
        console.error('Error fetching events:', error);
    });
}


function initMap(events) {
    let userLatitude = localStorage.getItem('userLatitude');
    let userLongitude = localStorage.getItem('userLongitude');
    let zoomLevel=15;
    let mapCenter;
    let blueIcon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';

    if (userLatitude && userLongitude) {
        // Use the stored location
        mapCenter = new google.maps.LatLng(parseFloat(userLatitude), parseFloat(userLongitude));
    } else {
        // Default location if no user location is found
        mapCenter = new google.maps.LatLng(-34.397, 150.644);
    }

    map = new google.maps.Map(document.getElementById("map"), {
        center: mapCenter,
        zoom: zoomLevel,
    });

     // Function to navigate to Flask route
    function navigateToFlaskRoute(eventTitle) {
        // Construct the URL for Flask route
        var flaskUrl = `/event_detail_page/${encodeURIComponent(eventTitle)}`;
        window.location.href = flaskUrl; // Navigate to the Flask route
    }

    // Create a marker at the current location
    let userMarker = new google.maps.Marker({
        position: mapCenter,
        map: map,
        title: "Tú estás aquí"
    });

    let infoWindow = new google.maps.InfoWindow();

    events.forEach(function(event) {
        var latitude = parseFloat(event.coordinates.latitude);
        var longitude = parseFloat(event.coordinates.longitude);
        var title = event.title;
        var price = event.price;

        var eventMarker = new google.maps.Marker({
            position: {lat: latitude, lng: longitude},
            map: map,
            icon: blueIcon,
            title: title
        });

        // Add mouseover listener for each marker
        eventMarker.addListener('mouseover', function() {
            infoWindow.setContent(`
            <div style="color: black; background-color: white; font-size: 14px; padding: 5px;">
                <strong>${title}</strong><br>Price: ${price}
            </div>
        `);
            console.log(`<div style="color: black"><strong>${title}</strong><br>Price: ${price}</div>`);
            infoWindow.open(map, eventMarker);
        });

        // Add mouseout listener to close the info window
        eventMarker.addListener('mouseout', function() {
            infoWindow.close();
        });

        eventMarker.addListener('click', function() {
            navigateToFlaskRoute(title);
        });

    });
}


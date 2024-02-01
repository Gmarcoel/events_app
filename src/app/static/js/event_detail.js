function initMap() {
    let userLatitude = localStorage.getItem('userLatitude');
    let userLongitude = localStorage.getItem('userLongitude');
    let mapElement = document.getElementById("map");
    let eventCoordinates = mapElement.getAttribute("data-event-coordinates");
    let eventTitle = mapElement.getAttribute("data-event-title");
    let blueIcon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';


    let mapCenter;
    let zoomLevel=10;

    if (userLatitude && userLongitude) {
        // Use the stored location
        mapCenter = new google.maps.LatLng(parseFloat(userLatitude), parseFloat(userLongitude));
    } else {
        // Default location if no user location is found
        mapCenter = new google.maps.LatLng(-34.397, 150.644);
    }

    // Create the map
    map = new google.maps.Map(document.getElementById("map"), {
        center: mapCenter,
        zoom: zoomLevel,
    });

    // Create a marker at the current location
    new google.maps.Marker({
        position: mapCenter,
        map: map,
        title: "Tú estás aquí"
    });

    // Create a marker at the event location
    if (eventCoordinates) {
        let eventCoordinatesString = eventCoordinates.replace(/'/g, '"');
        let coordinates;
        try {
            coordinates = JSON.parse(eventCoordinatesString);
        } catch (e) {
            console.error("Error parsing event coordinates: " + e);
        }

        eventLatitude = parseFloat(coordinates.latitude);
        eventLongitude = parseFloat(coordinates.longitude);

        let eventPosition = new google.maps.LatLng(eventLatitude, eventLongitude);
        new google.maps.Marker({
            position: eventPosition,
            map: map,
            title: eventTitle,
            icon: blueIcon
        });
    }

}

// Description splitting and toggling
document.addEventListener('DOMContentLoaded', function() {
    var fullText = document.getElementById('hidden-description').textContent;
    
    // Split the text into sentences using a regular expression
    var sentences = fullText.match(/[^.!?]+[.!?]+/g);
    if (!sentences) sentences = [fullText]; // Fallback if no sentence markers are found

    // Define a heuristic for the first paragraph (e.g., first 3 sentences or 200 characters)
    var firstParagraph = sentences.slice(0, 3).join(' ');
    if (firstParagraph.length > 200) {
        firstParagraph = firstParagraph.substring(0, 200);
    }

    var remainingText = fullText.substring(firstParagraph.length);

    var descriptionSpan = document.getElementById('description');
    descriptionSpan.textContent = firstParagraph;

    document.getElementById('toggle-button').addEventListener('click', function() {
        var buttonText = this.textContent;

        if(buttonText === "Mostrar más") {
            descriptionSpan.textContent += remainingText; // Append the remaining text
            this.textContent = "Mostrar menos";
        } else {
            descriptionSpan.textContent = firstParagraph; // Revert to only the first paragraph
            this.textContent = "Mostrar más";
        }
    });
});

function imageLoadedPromise(imgElement) {
    return new Promise(resolve => {
        if (imgElement.complete) {
            resolve();
        } else {
            imgElement.addEventListener('load', resolve);
        }
    });
}

window.addEventListener('DOMContentLoaded', function() {
    const imageElements = document.querySelectorAll('#carouselEventImages .carousel-image');
    const imageLoadPromises = Array.from(imageElements).map(imageLoadedPromise);

    Promise.all(imageLoadPromises).then(() => {
        // All images are loaded, now execute carousel logic
        const carousel = document.querySelector('#carouselEventImages .carousel-inner .carousel-item');
        let imageWidth = carousel.querySelector('.carousel-image').offsetWidth;
        let interval = 2000;

        setInterval(function() {
            let newScrollLeft = carousel.scrollLeft + imageWidth;

            if (newScrollLeft + (imageWidth * 2) >= carousel.scrollWidth) {
                carousel.scrollLeft = 0;
            } else {
                carousel.scrollLeft = newScrollLeft;
            }
        }, interval);
    });
});

  

window.onload = function() {
    initMap();
};
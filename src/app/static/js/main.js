//####################### POPUP #########################################

function showPopup() {
    document.getElementById('popup').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}

function hidePopup() {
    document.getElementById('popup').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

document.getElementById('btn-search-plan').addEventListener('click', showPopup);

document.getElementById('overlay').addEventListener('click', function(event) {
    // Check if the click occurred outside the popup content
    if (event.target === document.getElementById('overlay')) {
        hidePopup();
    }
});

// Prevent the popup from closing when its content is clicked
document.getElementById('popup').addEventListener('click', function(event) {
    event.stopPropagation();
});


// ############################# LOCATION #########################################
// Function to get user's location with high accuracy
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            sendPosition(position);
 
            localStorage.setItem('userLatitude', position.coords.latitude);
            localStorage.setItem('userLongitude', position.coords.longitude);
        }, 
        error => console.warn(`ERROR(${error.code}): ${error.message}`),
        {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        });
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}

function sendPosition(position) {
    fetch('/get_nearest_events', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        }),
    })
    .then(response => response.json())
    .then(nearestEvents => updateEvents(nearestEvents))
    .catch(error => console.error('Error:', error));
}

function eventTemplate(event) {
    let totalRating = event.comments.reduce((sum, comment) => sum + parseFloat(comment.rating), 0);
    let meanRating = event.comments.length > 0 ? totalRating / (2 * event.comments.length) : 0;
    meanRating = (meanRating >= 4 && meanRating < 5) ? 4 : Math.round(meanRating);

    // Generate stars for the rating
    const stars = Array.from({ length: 5 }, (_, i) => i < meanRating ? 
    '<i class="fas fa-star text-yellow-400"></i>' : 
    '<i class="fas fa-star text-gray-400"></i>').join('');

    return `
    <a href="/event_detail_page/${encodeURIComponent(event.title)}" class="no-underline">
        <div class="event-card bg-white text-gray-900 rounded-lg overflow-hidden">
            <img src="${event.portrait}" alt="${event.title}" class="w-full">
            <div class="p-4">
                <p class="font-semibold">${event.title}</p>
                <p class="text-xs">${event.date}</p>
                <div class="flex items-center mt-2">
                    ${stars}
                    <span class="text-xs ml-1">${event.rating}</span>
                </div>
                <p class="mt-3 text-lg font-bold">${event.price}</p>
            </div>
        </div>
    </a>`;
}

function updateEvents(nearestEvents) {
    const eventsContainer = document.querySelector('.nearest-events-container');
    eventsContainer.innerHTML = ''; // Clear existing content

    nearestEvents.forEach(event => {
        const eventElement = eventTemplate(event);
        eventsContainer.innerHTML += eventElement;
    });
}

window.onload = function() {
    getLocation();
};

function fetchLocationsAndMark() {
    fetch('/get_locations')
        .then(response => response.json())
        .then(data => {
            data.forEach(location => {
                new google.maps.Marker({
                    position: { lat: location.latitude, lng: location.longitude },
                    map: map,
                    title: location.title // Assuming each location has a 'name' property
                });
                console.log(location.title);
            });
        })
        .catch(error => console.error('Error:', error));
}

document.getElementById("btn-search-plan").addEventListener("click", fetchLocationsAndMark);


// ############################# CATEGORIES BUTTONS #########################################
document.getElementById('btn-cult').addEventListener('click', function() { redirectToCategory('Cultura'); });
document.getElementById('btn-gastro').addEventListener('click', function() { redirectToCategory('Gastronomia'); });
document.getElementById('btn-sport').addEventListener('click', function() { redirectToCategory('Deportes'); });
document.getElementById('btn-bienestar').addEventListener('click', function() { redirectToCategory('Bienestar'); });


function redirectToCategory(category) {
    window.location.href = `/list_page?category=${category}`;
}

// ############################# BANNER #######################################
// Images for the banner
var images = [
    'url("https://img.rtve.es/imagenes/vogue-madrid-miriam-sanchez-moda/1595251528463.jpg")',
    'url("https://sitofon.com/wp-content/uploads/2020/02/Azotea-grupo-madrid.jpg")',
    'url("https://www.hdwallpapers.in/download/black_and_white_photo_of_madrid_palace_spain_hd_abstract-HD.jpg")',
    'url("https://assets.arcadina.com/4684/1223/mg-4462-en-el-centro-de-la-gran-via-b-n-copia_2023071912235864b7d5dece4c0.sized.jpg")',
    'url("https://imgresizer.eurosport.com/unsafe/1200x0/filters:format(png)/origin-imgresizer.eurosport.com/2021/08/17/3202856-65612388-2560-1440.png")',
];

var currentIndex = 0;

setInterval(function() {
    if (currentIndex >= images.length) {
        currentIndex = 0;
    }
    document.querySelector('.banner-background').style.backgroundImage = images[currentIndex];
    currentIndex++;
}, 8000); 

const slider = document.getElementById('energic');
const card = document.getElementById('sliderCardEnergic');
const cardValue = document.getElementById('cardValueEnergic');

slider.oninput = function() {
    cardValue.innerHTML = this.value;
    const percent = (this.value - this.min) / (this.max - this.min);
    const thumbOffset = percent * (this.offsetWidth - 8); // Adjust 8 based on the actual thumb width
    card.style.left = thumbOffset + 'px';
    card.style.display = 'block';
    setTimeout(() => { card.style.display = 'none'; }, 2000); // Hide after 1 second
};

const slider2 = document.getElementById('exciting');
const card2 = document.getElementById('sliderCardExciting');
const cardValue2 = document.getElementById('cardValueExciting');

slider2.oninput = function() {
    cardValue2.innerHTML = this.value;
    const percent = (this.value - this.min) / (this.max - this.min);
    const thumbOffset = percent * (this.offsetWidth - 8); // Adjust 8 based on the actual thumb width
    card2.style.left = thumbOffset + 'px';
    card2.style.display = 'block';
    setTimeout(() => { card2.style.display = 'none'; }, 2000); // Hide after 1 second
};

const slider3 = document.getElementById('calm');
const card3 = document.getElementById('sliderCardCalm');
const cardValue3 = document.getElementById('cardValueCalm');

slider3.oninput = function() {
    cardValue3.innerHTML = this.value;
    const percent = (this.value - this.min) / (this.max - this.min);
    const thumbOffset = percent * (this.offsetWidth - 8); // Adjust 8 based on the actual thumb width
    card3.style.left = thumbOffset + 'px';
    card3.style.display = 'block';
    setTimeout(() => { card3.style.display = 'none'; }, 2000); // Hide after 1 second
};

const slider4 = document.getElementById('outdoors');
const card4 = document.getElementById('sliderCardOutdoors');
const cardValue4 = document.getElementById('cardValueOutdoors');

slider4.oninput = function() {
    cardValue4.innerHTML = this.value;
    const percent = (this.value - this.min) / (this.max - this.min);
    const thumbOffset = percent * (this.offsetWidth - 8); // Adjust 8 based on the actual thumb width
    card4.style.left = thumbOffset + 'px';
    card4.style.display = 'block';
    setTimeout(() => { card4.style.display = 'none'; }, 2000); // Hide after 1 second
};

const slider5 = document.getElementById('with_children');
const card5 = document.getElementById('sliderCardWithChildren');
const cardValue5 = document.getElementById('cardValueWithChildren');

slider5.oninput = function() {
    cardValue5.innerHTML = this.value;
    const percent = (this.value - this.min) / (this.max - this.min);
    const thumbOffset = percent * (this.offsetWidth - 8); // Adjust 8 based on the actual thumb width
    card5.style.left = thumbOffset + 'px';
    card5.style.display = 'block';
    setTimeout(() => { card5.style.display = 'none'; }, 2000); // Hide after 1 second
};

const slider6 = document.getElementById('funny');
const card6 = document.getElementById('sliderCardFunny');
const cardValue6 = document.getElementById('cardValueFunny');

slider6.oninput = function() {
    cardValue6.innerHTML = this.value;
    const percent = (this.value - this.min) / (this.max - this.min);
    const thumbOffset = percent * (this.offsetWidth - 8); // Adjust 8 based on the actual thumb width
    card6.style.left = thumbOffset + 'px';
    card6.style.display = 'block';
    setTimeout(() => { card6.style.display = 'none'; }, 2000); // Hide after 1 second
};

const slider7 = document.getElementById('close');
const card7 = document.getElementById('sliderCardClose');
const cardValue7 = document.getElementById('cardValueClose');

slider7.oninput = function() {
    cardValue7.innerHTML = this.value;
    const percent = (this.value - this.min) / (this.max - this.min);
    const thumbOffset = percent * (this.offsetWidth - 8); // Adjust 8 based on the actual thumb width
    card7.style.left = thumbOffset + 'px';
    card7.style.display = 'block';
    setTimeout(() => { card7.style.display = 'none'; }, 2000); // Hide after 1 second
};

const slider8 = document.getElementById('price');
const card8 = document.getElementById('sliderCardPrice');
const cardValue8 = document.getElementById('cardValuePrice');

slider8.oninput = function() {
    cardValue8.innerHTML = this.value;
    const percent = (this.value - this.min) / (this.max - this.min);
    const thumbOffset = percent * (this.offsetWidth - 8); // Adjust 8 based on the actual thumb width
    card8.style.left = thumbOffset + 'px';
    card8.style.display = 'block';
    setTimeout(() => { card8.style.display = 'none'; }, 2000); // Hide after 1 second
};
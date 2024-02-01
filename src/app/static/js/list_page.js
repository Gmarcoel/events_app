document.addEventListener('DOMContentLoaded', function() {
    fetchEventsData('/list_content');

    // Set up event listeners for buttons
    document.getElementById('btn-list').addEventListener('click', function() {
        fetchEventsData('/list_content');
    });

    document.getElementById('btn-map').addEventListener('click', function() {
        fetchEventsData('/map_content');
    });
});

function fetchEventsData(contentUrl) {
    console.log(query);

    var queryObject = (typeof query === 'string') ? JSON.parse(query) : query;

    var queryString = Object.keys(queryObject).map(key => {
        return encodeURIComponent(key) + '=' + encodeURIComponent(queryObject[key]);
    }).join('&');

    console.log(queryString);

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
    .then(data => {
        console.log(data);
        console.log(contentUrl);
        loadContent(contentUrl, data);
    })
    .catch(error => {
        console.error('Error fetching events data:', error);
    });
}


function loadContent(url, data) {
    console.log(data);
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
    })
    .then(html => {
        const container = document.getElementById('list-map-container');
        container.innerHTML = html;

        if (url == '/map_content') {
            if (container.classList.contains('grid')) {
                container.classList.remove('grid');
            }
            if (container.classList.contains('grid-cols-4')) {
                container.classList.remove('grid-cols-4');
            }
            if (container.classList.contains('gap-3')) {
                container.classList.remove('gap-3');
            }
            fetchEventsAndInitMap();
        }else if ((url == '/list_content') && (data.length > 0)) {
            if (!container.classList.contains('grid')) {
                container.classList.add('grid');
            }
            if (!container.classList.contains('grid-cols-4')) {
                container.classList.add('grid-cols-4');
            }
            if (!container.classList.contains('gap-3')) {
                container.classList.add('gap-3');
            }
        }else {
            if (container.classList.contains('grid')) {
                container.classList.remove('grid');
            }
            if (container.classList.contains('grid-cols-4')) {
                container.classList.remove('grid-cols-4');
            }
            if (container.classList.contains('gap-3')) {
                container.classList.remove('gap-3');
            }
        }
    })
    .catch(error => {
        console.error('Error loading content:', error);
    });
}

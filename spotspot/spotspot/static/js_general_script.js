const socket = io();
const searchButton = document.getElementById('search-button');
const spinnerBorder = document.getElementById('spinner-border');
const searchInput = document.getElementById('search-input');
const searchDropdown = document.getElementById('search-dropdown');
let selectedType = "track";

function changeUI(reqState) {
    if (reqState === "busy") {
        searchInput.disabled = true;
        searchButton.disabled = true;
        searchDropdown.disabled = true;
        spinnerBorder.style.display = 'inline-block';
    } else {
        spinnerBorder.style.display = 'none';
        searchInput.disabled = false;
        searchButton.disabled = false;
        searchDropdown.disabled = false;
    }
}

function updateSelection(option) {
    selectedType = option.toLowerCase();
    document.getElementById("search-button").innerText = `Search for ${option}`;
}

function initiateSearch() {
    changeUI("busy");
    const searchText = searchInput.value;
    socket.emit('search', { query: searchText, type: selectedType });
}

function populateTemplate(type, data) {
    let templateId;
    let element;

    if (type === 'track') {
        templateId = 'track-item-template';
    } else if (type === 'album') {
        templateId = 'album-item-template';
    } else if (type === 'artist') {
        templateId = 'artist-item-template';
    } else if (type === 'playlist') {
        templateId = 'playlist-item-template';
    }

    const template = document.getElementById(templateId);
    const clone = document.importNode(template.content, true);

    const downloadButton = clone.querySelector('.download');

    if (type === 'track') {
        clone.querySelector('.track-img').src = data.image || 'https://picsum.photos/300';
        clone.querySelector('.name').textContent = data.name;
        clone.querySelector('.artist').textContent = data.artist;
        clone.querySelector('.download').href = data.url;
        clone.querySelector('.download').setAttribute('data-url', data.url);
    } else if (type === 'album') {
        clone.querySelector('.album-img').src = data.image || 'https://picsum.photos/300';
        clone.querySelector('.name').textContent = data.name;
        clone.querySelector('.artist').textContent = data.artist;
        clone.querySelector('.download').href = data.url;
        clone.querySelector('.download').setAttribute('data-url', data.url);
    } else if (type === 'artist') {
        clone.querySelector('.artist-img').src = data.image || 'https://picsum.photos/300';
        clone.querySelector('.name').textContent = data.name;
        clone.querySelector('.followers').textContent = `${data.followers} Followers`;
        clone.querySelector('.download').href = data.url;
        clone.querySelector('.download').setAttribute('data-url', data.url);
    } else if (type === 'playlist') {
        clone.querySelector('.playlist-img').src = data.image || 'https://picsum.photos/300';
        clone.querySelector('.name').textContent = data.name;
        clone.querySelector('.owner').textContent = data.owner;
        clone.querySelector('.download').href = data.url;
        clone.querySelector('.download').setAttribute('data-url', data.url);
    }

    element = document.getElementById('results-section');
    element.appendChild(clone);

    downloadButton.addEventListener('click', function (event) {
        event.preventDefault();
        handleDownloadClick(event);
    });
}

function handleDownloadClick(event) {
    const button = event.target;

    button.disabled = true;
    button.classList.remove('btn-primary');
    button.classList.add('btn-secondary');
    button.classList.add('disabled');
    button.innerText = 'Added';

    const trackUrl = button.getAttribute('data-url');
    const card = button.closest('.card');

    if (!trackUrl) {
        alert('No URL found!');
        return;
    }

    const itemData = {
        type: card.querySelector('.type')?.textContent.trim().toLowerCase(),
        name: card.querySelector('.name')?.textContent.trim(),
        artist: card.querySelector('.artist')?.textContent.trim() || null,
        url: trackUrl
    };

    socket.emit('download_item', itemData);
}

searchInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        initiateSearch();
    }
});

searchButton.addEventListener('click', initiateSearch);

socket.on('search_results', function (data) {
    changeUI("ready");
    const resultsSection = document.getElementById('results-section');
    resultsSection.innerHTML = '';

    if (data && data.results) {
        for (let category in data.results) {
            let items = data.results[category];

            if (Array.isArray(items) && items.length > 0) {
                items.forEach(item => {
                    populateTemplate(item.type, item);
                });
            } else {
                const noResultsMessage = document.createElement('p');
                noResultsMessage.textContent = 'No results found';
                resultsSection.appendChild(noResultsMessage);
            }
        }
    }
});

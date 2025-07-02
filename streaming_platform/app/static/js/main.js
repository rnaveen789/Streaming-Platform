// Video Player Controls
document.addEventListener('DOMContentLoaded', function() {
    const videoPlayer = document.querySelector('video');
    if (videoPlayer) {
        // Add keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            switch(e.key) {
                case ' ':
                    e.preventDefault();
                    videoPlayer.paused ? videoPlayer.play() : videoPlayer.pause();
                    break;
                case 'ArrowLeft':
                    videoPlayer.currentTime -= 5;
                    break;
                case 'ArrowRight':
                    videoPlayer.currentTime += 5;
                    break;
                case 'ArrowUp':
                    videoPlayer.volume = Math.min(1, videoPlayer.volume + 0.1);
                    break;
                case 'ArrowDown':
                    videoPlayer.volume = Math.max(0, videoPlayer.volume - 0.1);
                    break;
            }
        });
    }
});

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// File Upload Preview
function previewFile(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('filePreview');
            if (preview) {
                preview.src = e.target.result;
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Search Autocomplete
let searchTimeout;
const searchInput = document.querySelector('input[name="q"]');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = this.value.trim();
            if (query.length >= 2) {
                fetch(`/api/search?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        // Update search suggestions
                        updateSearchSuggestions(data);
                    })
                    .catch(error => console.error('Error:', error));
            }
        }, 300);
    });
}

function updateSearchSuggestions(data) {
    const suggestionsContainer = document.getElementById('searchSuggestions');
    if (!suggestionsContainer) return;

    suggestionsContainer.innerHTML = '';
    data.forEach(item => {
        const div = document.createElement('div');
        div.className = 'suggestion-item';
        div.textContent = item.title;
        div.addEventListener('click', () => {
            searchInput.value = item.title;
            suggestionsContainer.innerHTML = '';
        });
        suggestionsContainer.appendChild(div);
    });
}

// Watch Duration Tracking
let watchDurationInterval;
function startWatchDurationTracking(videoId) {
    if (watchDurationInterval) {
        clearInterval(watchDurationInterval);
    }

    watchDurationInterval = setInterval(() => {
        const video = document.querySelector('video');
        if (video && !video.paused) {
            fetch(`/api/video/${videoId}/watch-duration`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    duration: Math.floor(video.currentTime)
                })
            });
        }
    }, 30);
}

// Initialize tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
}); 
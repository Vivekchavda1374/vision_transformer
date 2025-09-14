// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const previewImage = document.getElementById('previewImage');
const predictionsList = document.getElementById('predictionsList');
const modelInfo = document.getElementById('modelInfo');

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkServerHealth();
});

function setupEventListeners() {
    // File input change
    imageInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Click to upload
    uploadArea.addEventListener('click', () => imageInput.click());
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
            processImage(file);
        } else {
            showError('Please select a valid image file.');
        }
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processImage(file);
    }
}

function processImage(file) {
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size too large. Please select an image under 10MB.');
        return;
    }
    
    // Show loading
    showLoading();
    
    // Create FormData and send to server
    const formData = new FormData();
    formData.append('image', file);
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred during prediction.');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error:', error);
        showError('Network error. Please try again.');
    });
}

function showLoading() {
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    // Scroll to loading section
    loadingSection.scrollIntoView({ behavior: 'smooth' });
}

function hideLoading() {
    loadingSection.style.display = 'none';
}

function displayResults(data) {
    // Display image
    previewImage.src = data.image;
    
    // Display predictions
    displayPredictions(data.predictions);
    
    // Display model info
    displayModelInfo(data.model_info);
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Add animation
    resultsSection.style.opacity = '0';
    resultsSection.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        resultsSection.style.transition = 'all 0.5s ease';
        resultsSection.style.opacity = '1';
        resultsSection.style.transform = 'translateY(0)';
    }, 100);
}

function displayPredictions(predictions) {
    predictionsList.innerHTML = '';
    
    predictions.forEach((prediction, index) => {
        const predictionItem = document.createElement('div');
        predictionItem.className = `prediction-item ${index === 0 ? 'top-prediction' : ''}`;
        
        predictionItem.innerHTML = `
            <div class="prediction-class">
                ${index === 0 ? '<i class="fas fa-crown"></i> ' : ''}
                ${prediction.class.replace(/_/g, ' ')}
            </div>
            <div class="prediction-confidence">
                ${prediction.percentage}
            </div>
        `;
        
        // Add animation delay
        predictionItem.style.opacity = '0';
        predictionItem.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            predictionItem.style.transition = 'all 0.3s ease';
            predictionItem.style.opacity = '1';
            predictionItem.style.transform = 'translateX(0)';
        }, index * 100);
        
        predictionsList.appendChild(predictionItem);
    });
}

function displayModelInfo(modelInfoData) {
    modelInfo.innerHTML = `
        <h4><i class="fas fa-info-circle"></i> Model Information</h4>
        <div class="model-detail">
            <strong>Model:</strong>
            <span>${modelInfoData.name}</span>
        </div>
        <div class="model-detail">
            <strong>Architecture:</strong>
            <span>${modelInfoData.architecture}</span>
        </div>
        <div class="model-detail">
            <strong>Input Size:</strong>
            <span>${modelInfoData.input_size}</span>
        </div>
        <div class="model-detail">
            <strong>Parameters:</strong>
            <span>${modelInfoData.parameters}</span>
        </div>
    `;
}

function showError(message) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add error styles
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ff4757;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(255, 71, 87, 0.3);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    // Add button styles
    const button = errorDiv.querySelector('button');
    button.style.cssText = `
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0.2rem;
        margin-left: 0.5rem;
    `;
    
    document.body.appendChild(errorDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 5000);
}

function checkServerHealth() {
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            console.log('Server health:', data);
            if (!data.model_loaded) {
                console.warn('Model not loaded properly');
            }
        })
        .catch(error => {
            console.error('Health check failed:', error);
        });
}

// Add CSS animation for error notification
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .error-notification button:hover {
        opacity: 0.7;
    }
`;
document.head.appendChild(style);

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + U to upload
    if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
        e.preventDefault();
        imageInput.click();
    }
    
    // Escape to close error notifications
    if (e.key === 'Escape') {
        const errorNotifications = document.querySelectorAll('.error-notification');
        errorNotifications.forEach(notification => notification.remove());
    }
});

// Add smooth scrolling for better UX
document.documentElement.style.scrollBehavior = 'smooth';
// Main JavaScript file for Emergency Routing System

// Utility function to show loading state
function showLoading(elementId, message = 'Loading...') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<p class="loading-text">${message}</p>`;
    }
}

// Utility function to show error message
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="alert alert-error">
                <strong>✗ Error:</strong> ${message}
            </div>
        `;
    }
}

// Utility function to show success message
function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="alert alert-success">
                <strong>✓ Success!</strong> ${message}
            </div>
        `;
    }
}

// Format date/time
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Form validation for ambulance form
function validateAmbulanceForm(formData) {
    if (!formData.patient_type) {
        alert('Please select Patient Type');
        return false;
    }
    
    if (!formData.emergency_type) {
        alert('Please select Emergency Type');
        return false;
    }
    
    return true;
}

// Auto-refresh functionality
let autoRefreshInterval = null;

function startAutoRefresh(callback, interval = 10000) {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    autoRefreshInterval = setInterval(callback, interval);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Notification sound (optional)
function playNotificationSound() {
    // Can be implemented if audio file is available
    console.log('Notification sound');
}

// Console logging for debugging
function logDebug(message, data = null) {
    if (typeof console !== 'undefined') {
        console.log(`[ERS Debug] ${message}`, data || '');
    }
}

// Initialize tooltips or other UI enhancements
document.addEventListener('DOMContentLoaded', function() {
    logDebug('Emergency Routing System initialized');
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

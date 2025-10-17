/**
 * Main JavaScript for eCourts Cause List Scraper
 * Handles real-time data fetching, form management, and UI interactions
 */

// Global variables
let currentState = {
    state: null,
    district: null,
    complex: null,
    court: null
};

let isProcessing = false;

// DOM elements
const elements = {
    form: null,
    stateSelect: null,
    districtSelect: null,
    complexSelect: null,
    courtSelect: null,
    dateInput: null,
    listTypeSelect: null,
    bulkModeCheck: null,
    submitBtn: null,
    loadingSection: null,
    loadingText: null,
    resultSection: null,
    resultContent: null,
    progressContainer: null,
    progressBar: null,
    progressText: null
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    setupEventListeners();
    loadStates();
    setDefaultDate();
});

/**
 * Initialize DOM elements
 */
function initializeElements() {
    elements.form = document.getElementById('scrapeForm');
    elements.stateSelect = document.getElementById('state');
    elements.districtSelect = document.getElementById('district');
    elements.complexSelect = document.getElementById('complex');
    elements.courtSelect = document.getElementById('court');
    elements.dateInput = document.getElementById('date');
    elements.listTypeSelect = document.getElementById('listType');
    elements.bulkModeCheck = document.getElementById('bulkMode');
    elements.submitBtn = document.getElementById('submitBtn');
    elements.loadingSection = document.getElementById('loadingSection');
    elements.loadingText = document.getElementById('loadingText');
    elements.resultSection = document.getElementById('resultSection');
    elements.resultContent = document.getElementById('resultContent');
    elements.progressContainer = document.getElementById('progressContainer');
    elements.progressBar = document.getElementById('progressBar');
    elements.progressText = document.getElementById('progressText');
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Form submission
    elements.form.addEventListener('submit', handleFormSubmit);
    
    // Cascading dropdowns
    elements.stateSelect.addEventListener('change', handleStateChange);
    elements.districtSelect.addEventListener('change', handleDistrictChange);
    elements.complexSelect.addEventListener('change', handleComplexChange);
    elements.courtSelect.addEventListener('change', handleCourtChange);
    
    // Bulk mode toggle
    elements.bulkModeCheck.addEventListener('change', handleBulkModeToggle);
    
    // Prevent form submission with Enter key during loading
    elements.form.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && isProcessing) {
            e.preventDefault();
        }
    });
}

/**
 * Set default date to today
 */
function setDefaultDate() {
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    elements.dateInput.value = formattedDate;
}

/**
 * Load states from API
 */
async function loadStates() {
    try {
        showSelectLoading(elements.stateSelect, 'Loading states...');
        
        const response = await fetchWithTimeout('/api/states', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            populateSelect(elements.stateSelect, result.data, 'Select State');
            console.log(`Loaded ${result.total} states`);
        } else {
            throw new Error(result.error || 'Failed to load states');
        }
        
    } catch (error) {
        console.error('Error loading states:', error);
        showSelectError(elements.stateSelect, 'Failed to load states');
        showToast('error', 'Failed to load states. Please refresh the page.');
    }
}

/**
 * Handle state selection change
 */
async function handleStateChange() {
    const stateCode = elements.stateSelect.value;
    
    // Reset dependent dropdowns
    resetSelect(elements.districtSelect, 'Select State first');
    resetSelect(elements.complexSelect, 'Select District first');
    resetSelect(elements.courtSelect, 'Select Court Complex first');
    
    currentState.state = stateCode;
    currentState.district = null;
    currentState.complex = null;
    currentState.court = null;
    
    if (!stateCode) return;
    
    try {
        showSelectLoading(elements.districtSelect, 'Loading districts...');
        
        const response = await fetchWithTimeout(`/api/districts/${stateCode}`);
        const result = await response.json();
        
        if (result.success) {
            populateSelect(elements.districtSelect, result.data, 'Select District');
            elements.districtSelect.disabled = false;
            console.log(`Loaded ${result.total} districts for state ${stateCode}`);
        } else {
            throw new Error(result.error || 'Failed to load districts');
        }
        
    } catch (error) {
        console.error('Error loading districts:', error);
        showSelectError(elements.districtSelect, 'Failed to load districts');
        showToast('error', 'Failed to load districts. Please try again.');
    }
}

/**
 * Handle district selection change
 */
async function handleDistrictChange() {
    const districtCode = elements.districtSelect.value;
    
    // Reset dependent dropdowns
    resetSelect(elements.complexSelect, 'Select District first');
    resetSelect(elements.courtSelect, 'Select Court Complex first');
    
    currentState.district = districtCode;
    currentState.complex = null;
    currentState.court = null;
    
    if (!districtCode || !currentState.state) return;
    
    try {
        showSelectLoading(elements.complexSelect, 'Loading court complexes...');
        
        const response = await fetchWithTimeout(`/api/complexes/${currentState.state}/${districtCode}`);
        const result = await response.json();
        
        if (result.success) {
            populateSelect(elements.complexSelect, result.data, 'Select Court Complex');
            elements.complexSelect.disabled = false;
            console.log(`Loaded ${result.total} court complexes`);
        } else {
            throw new Error(result.error || 'Failed to load court complexes');
        }
        
    } catch (error) {
        console.error('Error loading court complexes:', error);
        showSelectError(elements.complexSelect, 'Failed to load court complexes');
        showToast('error', 'Failed to load court complexes. Please try again.');
    }
}

/**
 * Handle complex selection change
 */
async function handleComplexChange() {
    const complexCode = elements.complexSelect.value;
    
    // Reset dependent dropdown
    resetSelect(elements.courtSelect, 'Select Court Complex first');
    
    currentState.complex = complexCode;
    currentState.court = null;
    
    if (!complexCode || !currentState.state || !currentState.district) return;
    
    try {
        showSelectLoading(elements.courtSelect, 'Loading courts...');
        
        const response = await fetchWithTimeout(`/api/courts/${currentState.state}/${currentState.district}/${complexCode}`);
        const result = await response.json();
        
        if (result.success) {
            populateSelect(elements.courtSelect, result.data, 'Select Court');
            elements.courtSelect.disabled = false;
            console.log(`Loaded ${result.total} courts`);
        } else {
            throw new Error(result.error || 'Failed to load courts');
        }
        
    } catch (error) {
        console.error('Error loading courts:', error);
        showSelectError(elements.courtSelect, 'Failed to load courts');
        showToast('error', 'Failed to load courts. Please try again.');
    }
}

/**
 * Handle court selection change
 */
function handleCourtChange() {
    currentState.court = elements.courtSelect.value;
}

/**
 * Handle bulk mode toggle
 */
function handleBulkModeToggle() {
    const isBulkMode = elements.bulkModeCheck.checked;
    
    if (isBulkMode) {
        // Disable court selection in bulk mode
        elements.courtSelect.disabled = true;
        elements.courtSelect.required = false;
        elements.submitBtn.innerHTML = '<i class="fas fa-layer-group me-2"></i>Generate Bulk PDF Report';
        
        showToast('info', 'Bulk mode enabled. Will scrape all courts in the selected complex.');
    } else {
        // Enable court selection
        elements.courtSelect.disabled = false;
        elements.courtSelect.required = true;
        elements.submitBtn.innerHTML = '<i class="fas fa-download me-2"></i>Generate Cause List PDF';
    }
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (isProcessing) return;
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    const formData = new FormData(elements.form);
    const data = Object.fromEntries(formData);
    
    // Add current state data
    data.state_code = currentState.state;
    data.district_code = currentState.district;
    data.complex_code = currentState.complex;
    data.court_code = currentState.court;
    
    const isBulkMode = elements.bulkModeCheck.checked;
    
    try {
        setProcessingState(true);
        hideResult();
        
        if (isBulkMode) {
            await performBulkScraping(data);
        } else {
            await performSingleScraping(data);
        }
        
    } catch (error) {
        console.error('Scraping error:', error);
        showError('Scraping failed: ' + error.message);
    } finally {
        setProcessingState(false);
    }
}

/**
 * Perform single court scraping
 */
async function performSingleScraping(data) {
    updateLoadingText('Connecting to eCourts server...');
    updateProgress(10);
    
    const response = await fetchWithTimeout('/api/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }, 300000); // 5 minute timeout
    
    updateProgress(50);
    updateLoadingText('Processing response...');
    
    const result = await response.json();
    
    updateProgress(100);
    
    if (result.success) {
        showSuccess(result);
    } else {
        throw new Error(result.error || 'Scraping failed');
    }
}

/**
 * Perform bulk court scraping
 */
async function performBulkScraping(data) {
    updateLoadingText('Starting bulk scraping...');
    updateProgress(10);
    
    const response = await fetchWithTimeout('/api/bulk-scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }, 600000); // 10 minute timeout
    
    updateProgress(50);
    updateLoadingText('Processing bulk results...');
    
    const result = await response.json();
    
    updateProgress(100);
    
    if (result.success) {
        showBulkSuccess(result);
    } else {
        throw new Error(result.error || 'Bulk scraping failed');
    }
}

/**
 * Validate form data
 */
function validateForm() {
    const isBulkMode = elements.bulkModeCheck.checked;
    
    // Check required fields
    if (!currentState.state) {
        showToast('error', 'Please select a state');
        elements.stateSelect.focus();
        return false;
    }
    
    if (!currentState.district) {
        showToast('error', 'Please select a district');
        elements.districtSelect.focus();
        return false;
    }
    
    if (!currentState.complex) {
        showToast('error', 'Please select a court complex');
        elements.complexSelect.focus();
        return false;
    }
    
    if (!isBulkMode && !currentState.court) {
        showToast('error', 'Please select a court');
        elements.courtSelect.focus();
        return false;
    }
    
    if (!elements.dateInput.value) {
        showToast('error', 'Please select a date');
        elements.dateInput.focus();
        return false;
    }
    
    // Validate date is not too far in the future
    const selectedDate = new Date(elements.dateInput.value);
    const today = new Date();
    const maxDate = new Date(today.getTime() + (30 * 24 * 60 * 60 * 1000)); // 30 days from now
    
    if (selectedDate > maxDate) {
        showToast('warning', 'Selected date is too far in the future. Please select a more recent date.');
        elements.dateInput.focus();
        return false;
    }
    
    return true;
}

/**
 * Set processing state
 */
function setProcessingState(processing) {
    isProcessing = processing;
    
    if (processing) {
        elements.submitBtn.disabled = true;
        elements.submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span

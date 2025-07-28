// PDF.js configuration
pdfjsLib.GlobalWorkerOptions.workerSrc = 'pdf.worker.min.js';

// Get PDF URL from query parameters
const urlParams = new URLSearchParams(window.location.search);
const pdfUrl = urlParams.get('pdf');

// State variables
let pdfDoc = null;
let pageNum = 1;
let pageRendering = false;
let pageNumPending = null;
let currentZoom = 100;
const zoomStep = 25;
let searchResults = [];
let currentSearchIndex = -1;

// Elements
const loadingEl = document.getElementById('loading');
const errorEl = document.getElementById('error');
const pdfViewerEl = document.getElementById('pdfViewer');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageInfoEl = document.getElementById('pageInfo');
const downloadBtn = document.getElementById('downloadBtn');
const zoomOutBtn = document.getElementById('zoomOut');
const zoomInBtn = document.getElementById('zoomIn');
const zoomFitBtn = document.getElementById('zoomFit');
const searchBtn = document.getElementById('searchBtn');
const searchContainer = document.getElementById('searchContainer');
const searchInput = document.getElementById('searchInput');

// Initialize the viewer
async function initViewer() {
    if (!pdfUrl) {
        showError('No PDF URL provided');
        return;
    }

    try {
        // Load the PDF document
        const loadingTask = pdfjsLib.getDocument(pdfUrl);
        pdfDoc = await loadingTask.promise;
        
        // Update page info
        updatePageInfo();
        
        // Render the first page
        renderPage(pageNum);
        
        // Set up controls
        setupControls();
        
        // Hide loading, show viewer
        loadingEl.style.display = 'none';
        pdfViewerEl.style.display = 'flex';
        
    } catch (error) {
        console.error('Error loading PDF:', error);
        showError('Failed to load PDF: ' + error.message);
    }
}

function setupControls() {
    // Navigation controls
    prevBtn.addEventListener('click', () => {
        if (pageNum <= 1) return;
        pageNum--;
        renderPage(pageNum);
    });

    nextBtn.addEventListener('click', () => {
        if (pageNum >= pdfDoc.numPages) return;
        pageNum++;
        renderPage(pageNum);
    });

    // Download button
    downloadBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.href = pdfUrl;
        link.download = 'arxiv-paper.pdf';
        link.click();
    });

    // Zoom controls
    zoomOutBtn.addEventListener('click', () => {
        currentZoom = Math.max(50, currentZoom - zoomStep);
        updateZoom();
    });

    zoomInBtn.addEventListener('click', () => {
        currentZoom = Math.min(300, currentZoom + zoomStep);
        updateZoom();
    });

    zoomFitBtn.addEventListener('click', () => {
        currentZoom = 100;
        updateZoom();
    });

    // Search controls
    searchBtn.addEventListener('click', () => {
        const isVisible = searchContainer.style.display === 'block';
        searchContainer.style.display = isVisible ? 'none' : 'block';
        if (!isVisible) {
            searchInput.focus();
        }
    });

    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

async function renderPage(num) {
    pageRendering = true;
    
    try {
        // Get page
        const page = await pdfDoc.getPage(num);
        
        // Create page container
        const pageContainer = document.createElement('div');
        pageContainer.className = 'page';
        pageContainer.id = `page-${num}`;
        
        // Clear previous content
        pdfViewerEl.innerHTML = '';
        pdfViewerEl.appendChild(pageContainer);
        
        // Calculate viewport
        const viewport = page.getViewport({ scale: 1 });
        const scale = currentZoom / 100;
        const scaledViewport = page.getViewport({ scale: scale });
        
        // Create canvas
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.height = scaledViewport.height;
        canvas.width = scaledViewport.width;
        
        // Create text layer
        const textLayerDiv = document.createElement('div');
        textLayerDiv.className = 'textLayer';
        textLayerDiv.style.width = scaledViewport.width + 'px';
        textLayerDiv.style.height = scaledViewport.height + 'px';
        
        pageContainer.appendChild(canvas);
        pageContainer.appendChild(textLayerDiv);
        
        // Render page
        const renderContext = {
            canvasContext: context,
            viewport: scaledViewport
        };
        
        await page.render(renderContext).promise;
        
        // Render text layer
        const textContent = await page.getTextContent();
        pdfjsLib.renderTextLayer({
            textContent: textContent,
            container: textLayerDiv,
            viewport: scaledViewport,
            textDivs: []
        });
        
        pageRendering = false;
        
        if (pageNumPending !== null) {
            renderPage(pageNumPending);
            pageNumPending = null;
        }
        
        updatePageInfo();
        updateNavigationButtons();
        
    } catch (error) {
        console.error('Error rendering page:', error);
        pageRendering = false;
    }
}

function updateZoom() {
    const pageContainer = document.querySelector('.page');
    if (pageContainer) {
        pageContainer.style.transform = `scale(${currentZoom / 100})`;
    }
}

function updatePageInfo() {
    if (pdfDoc) {
        pageInfoEl.textContent = `Page ${pageNum} of ${pdfDoc.numPages}`;
    }
}

function updateNavigationButtons() {
    prevBtn.disabled = pageNum <= 1;
    nextBtn.disabled = pageNum >= pdfDoc.numPages;
}

async function performSearch() {
    const searchTerm = searchInput.value.trim();
    if (!searchTerm || !pdfDoc) return;
    
    searchResults = [];
    currentSearchIndex = -1;
    
    try {
        // Search through all pages
        for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
            const page = await pdfDoc.getPage(pageNum);
            const textContent = await page.getTextContent();
            
            const text = textContent.items.map(item => item.str).join(' ');
            const regex = new RegExp(searchTerm, 'gi');
            let match;
            
            while ((match = regex.exec(text)) !== null) {
                searchResults.push({
                    page: pageNum,
                    index: match.index,
                    text: match[0]
                });
            }
        }
        
        if (searchResults.length > 0) {
            // Navigate to first result
            currentSearchIndex = 0;
            const firstResult = searchResults[0];
            pageNum = firstResult.page;
            renderPage(pageNum);
            highlightSearchResult(firstResult);
        } else {
            alert('No results found for: ' + searchTerm);
        }
        
    } catch (error) {
        console.error('Search error:', error);
        alert('Error performing search');
    }
}

function highlightSearchResult(result) {
    // This is a simplified highlight - in a full implementation,
    // you'd need to map the text position to canvas coordinates
    console.log('Found result on page', result.page, 'at position', result.index);
}

function showError(message) {
    loadingEl.style.display = 'none';
    errorEl.style.display = 'block';
    errorEl.querySelector('p').textContent = message;
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initViewer);

// Handle keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Don't trigger shortcuts when typing in search input
    if (e.target === searchInput) return;
    
    switch(e.key) {
        case 'ArrowLeft':
            if (!prevBtn.disabled) prevBtn.click();
            break;
        case 'ArrowRight':
            if (!nextBtn.disabled) nextBtn.click();
            break;
        case '-':
            zoomOutBtn.click();
            break;
        case '=':
        case '+':
            zoomInBtn.click();
            break;
        case '0':
            zoomFitBtn.click();
            break;
        case 'f':
        case 'F':
            if (e.ctrlKey || e.metaKey) {
                e.preventDefault();
                searchBtn.click();
            }
            break;
    }
});
// Content script for arXiv PDF Viewer extension
(function() {
  'use strict';

  // Function to extract arXiv ID from URL
  function getArxivId() {
    const url = window.location.href;
    const match = url.match(/arxiv\.org\/abs\/(.+)/);
    return match ? match[1] : null;
  }

  // Function to create the floating button
  function createFloatingButton() {
    const button = document.createElement('div');
    button.id = 'arxiv-pdf-viewer-btn';
    button.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
      </svg>
      <span>View PDF</span>
    `;
    button.title = 'Open PDF in new tab';
    
    // Add click event listener
    button.addEventListener('click', function() {
      const arxivId = getArxivId();
      if (arxivId) {
        const pdfUrl = `https://arxiv.org/pdf/${arxivId}`;
        const viewerUrl = chrome.runtime.getURL('index.html') + `?pdf=${encodeURIComponent(pdfUrl)}`;
        window.open(viewerUrl, '_blank');
      }
    });

    return button;
  }

  // Function to initialize the extension
  function init() {
    // Check if we're on an arXiv abstract page
    if (window.location.href.includes('arxiv.org/abs/')) {
      // Create and add the floating button
      const button = createFloatingButton();
      document.body.appendChild(button);
      
      // Add entrance animation
      setTimeout(() => {
        button.classList.add('visible');
      }, 100);
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Also initialize for dynamic page changes (SPA navigation)
  let lastUrl = location.href;
  new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
      lastUrl = url;
      // Remove existing button if it exists
      const existingButton = document.getElementById('arxiv-pdf-viewer-btn');
      if (existingButton) {
        existingButton.remove();
      }
      // Re-initialize
      setTimeout(init, 500);
    }
  }).observe(document, { subtree: true, childList: true });

})(); 
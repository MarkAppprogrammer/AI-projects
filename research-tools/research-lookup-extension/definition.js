import { parseMarkdown } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {

    // Load the definition data
    chrome.storage.local.get(['currentDefinition'], (result) => {
        if (result.currentDefinition) {
            document.getElementById('term').textContent = result.currentDefinition.term;
            document.getElementById('definition').innerHTML = parseMarkdown(result.currentDefinition.definition);
        }
    });

    // Add event listener for the back button
    document.querySelector('.back-button').addEventListener('click', (e) => {
        e.preventDefault();
        window.close();
    });
}); 
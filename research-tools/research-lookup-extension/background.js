import { runLLM } from './llm.js';

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "lookupResearchTerm",
    title: "Lookup research term",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "lookupResearchTerm") {
    const selectedText = info.selectionText;
    
    // Validate that we have a valid tab
    if (!tab || tab.id === undefined || tab.id === -1) {
        console.error('No valid tab found');
        return;
    }
      

    const prompt = `Define the following term or phrase: "${selectedText}"`; // TODO: switch up the prompt to be formal yet simple to understand
    //console.log(prompt);

    try {
      // Call Hugging Face API (replace with your API endpoint & token)

      const definition = await runLLM(prompt);

      // Inject content script to show popup with the result
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: showPopup,
        args: [selectedText, definition]
      });
    } catch (error) {
      console.error('Error:', error);
      // Show error in the tab
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: showPopup,
        args: ["Error: Could not fetch definition. Please try again."]
      });
    }
  }
});

function showPopup(selectedText, definition) {
  const popup = document.createElement('div');
  popup.style.position = 'fixed';
  popup.style.bottom = '20px';
  popup.style.right = '20px';
  popup.style.padding = '16px';
  popup.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
  popup.style.borderRadius = '8px';
  popup.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
  popup.style.zIndex = '9999';
  popup.style.maxWidth = '320px';
  popup.style.fontSize = '15px';
  popup.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
  popup.style.color = '#ffffff';
  popup.style.lineHeight = '1.4';
  popup.style.backdropFilter = 'blur(10px)';
  popup.style.webkitBackdropFilter = 'blur(10px)';
  popup.style.transition = 'opacity 0.2s ease-in-out, transform 0.2s ease-in-out';
  popup.style.opacity = '0';
  popup.style.cursor = 'pointer';
  popup.style.transform = 'translateY(10px)';

  // Create header for selected text
  const header = document.createElement('h3');
  header.style.margin = '0 0 8px 0';
  header.style.fontSize = '16px';
  header.style.fontWeight = '600';
  header.style.color = '#ffffff';
  header.style.position = 'relative';
  header.textContent = selectedText;

  // Add underline element for header
  const headerUnderline = document.createElement('div');
  headerUnderline.style.position = 'absolute';
  headerUnderline.style.bottom = '-2px';
  headerUnderline.style.left = '0';
  headerUnderline.style.width = '0';
  headerUnderline.style.height = '1px';
  headerUnderline.style.backgroundColor = '#ffffff';
  headerUnderline.style.transition = 'width 0.3s ease-in-out';
  header.appendChild(headerUnderline);

  // Create definition text
  const definitionText = document.createElement('div');
  definitionText.style.fontSize = '14px';
  definitionText.style.color = 'rgba(255, 255, 255, 0.9)';
  
  // Truncate text to first paragraph and add ellipsis
  const firstParagraph = definition.split('\n')[0];
  const truncatedText = firstParagraph.length > 200 ? 
    firstParagraph.substring(0, 200) + '...' : 
    firstParagraph;
  definitionText.textContent = truncatedText;

  // Add hover effects
  popup.addEventListener('mouseenter', () => {
    headerUnderline.style.width = '100%';
    popup.style.transform = 'translateY(0)';
  });

  popup.addEventListener('mouseleave', () => {
    headerUnderline.style.width = '0';
    popup.style.transform = 'translateY(10px)';
  });

  // Add click handler
  popup.addEventListener('click', () => {
    chrome.storage.local.set({ 
      currentDefinition: {
        term: selectedText,
        definition: definition
      }
    }, () => {
      // Verify storage was successful
      chrome.storage.local.get(['currentDefinition'], (result) => {
        if (result.currentDefinition) {
          console.log('Successfully stored definition:', result.currentDefinition);
        } else {
          console.error('Failed to store definition');
        }
      });
    });
    chrome.runtime.sendMessage({ action: 'openTab' });
  });

  // Add elements to popup
  popup.appendChild(header);
  popup.appendChild(definitionText);
  document.body.appendChild(popup);
  
  // Fade in
  requestAnimationFrame(() => {
    popup.style.opacity = '1';
  });

  // Auto-close with fade out
  setTimeout(() => {
    popup.style.opacity = '0';
    setTimeout(() => {
      popup.remove();
    }, 200);
  }, 10000);
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'openTab') {
      chrome.tabs.create({ url: chrome.runtime.getURL('definition.html') });
    }
  });
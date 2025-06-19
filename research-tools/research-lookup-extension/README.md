# Research Paper Lookup Chrome Extension

A Chrome extension that allows users to right-click on terms in research papers to get AI-generated definitions and explanations.

## Features

- Right-click context menu integration
- AI-powered definitions using Hugging Face models
- Clean, minimal popup interface
- Auto-dismissing definition popups

## Setup

1. Clone or download this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" in the top right
4. Click "Load unpacked" and select the `research-lookup-extension` folder

## Configuration

Before using the extension, you need to:

1. Replace `YOUR_MODEL_NAME` in `background.js` with your chosen Hugging Face model (e.g., `meta-llama/Llama-3-8b-chat-hf`)
2. Replace `YOUR_HUGGING_FACE_API_TOKEN` with your actual Hugging Face API token

## Usage

1. Navigate to any webpage containing research papers
2. Select a term or phrase
3. Right-click and choose "Lookup research term"
4. A popup will appear with the AI-generated definition
5. The popup will automatically dismiss after 10 seconds

## Development

The extension consists of:
- `manifest.json`: Extension configuration
- `background.js`: Context menu and API integration
- `popup.html/js`: Extension popup interface
- `icons/`: Extension icons

## Notes

- The extension requires an active internet connection
- API calls are made to Hugging Face's inference API
- Rate limits may apply based on your Hugging Face API plan 
# arXiv PDF Viewer Chrome Extension

A Chrome extension that adds a floating "View PDF" button to arXiv abstract pages, allowing you to open PDFs in a dedicated viewer with enhanced controls and HTML rendering.

## Features

- **Floating Button**: Appears in the bottom-right corner on arXiv abstract pages
- **Modern UI**: Clean, responsive design with smooth animations
- **PDF.js Integration**: Renders PDFs as HTML elements using Mozilla's PDF.js library
- **Text Selection**: Full text selection and copying capabilities
- **Search Functionality**: Search within PDF content with highlighting
- **Enhanced Navigation**: Smooth page navigation with proper controls
- **Zoom Controls**: Multiple zoom levels with smooth scaling
- **Keyboard Shortcuts**: Navigate and zoom using keyboard controls
- **Mobile Responsive**: Works on both desktop and mobile devices

## Installation

### Method 1: Load as Unpacked Extension (Recommended for Development)

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top-right corner
3. Click "Load unpacked" and select the `arxiv-pdf-viewer` folder
4. The extension should now appear in your extensions list

### Method 2: Install from Chrome Web Store (Future)

*This extension will be available on the Chrome Web Store once published.*

## Usage

1. Navigate to any arXiv abstract page (e.g., `https://arxiv.org/abs/2103.12345`)
2. Look for the floating "View PDF" button in the bottom-right corner
3. Click the button to open the PDF in a new tab with the enhanced viewer
4. Use the controls in the viewer:
   - **Navigation**: Use Previous/Next buttons or arrow keys
   - **Zoom Controls**: Use the +/- buttons or keyboard shortcuts
   - **Search**: Click the search button or press Ctrl+F to search within the PDF
   - **Download**: Click the download button to save the PDF
   - **Text Selection**: Click and drag to select text for copying

## Keyboard Shortcuts

- `Left Arrow`: Previous page
- `Right Arrow`: Next page
- `+` or `=`: Zoom in
- `-`: Zoom out
- `0`: Reset zoom to fit
- `Ctrl+F` or `Cmd+F`: Open search dialog

## Technical Features

### PDF.js Integration
- **HTML Rendering**: PDFs are rendered as HTML elements instead of iframe
- **Text Layer**: Full text extraction and selection capabilities
- **Canvas Rendering**: High-quality visual rendering
- **Responsive Design**: Adapts to different screen sizes

### Search Functionality
- **Full-Text Search**: Search across all pages of the PDF
- **Result Navigation**: Jump to search results automatically
- **Highlighting**: Visual highlighting of search terms (basic implementation)

### Performance Optimizations
- **Lazy Loading**: Pages are rendered on-demand
- **Efficient Rendering**: Uses PDF.js worker for background processing
- **Memory Management**: Proper cleanup of rendered content

## File Structure

```
arxiv-pdf-viewer/
├── manifest.json          # Extension configuration
├── content.js            # Content script for arXiv pages
├── content.css           # Styles for the floating button
├── index.html            # PDF viewer page with PDF.js integration
├── index.js              # PDF.js implementation and viewer logic
├── icons/
│   └── icon.png          # Extension icon
└── README.md             # This file
```

## How It Works

1. **Content Script**: `content.js` runs on arXiv abstract pages and injects a floating button
2. **Button Click**: When clicked, it extracts the arXiv ID and constructs the PDF URL
3. **PDF.js Viewer**: Opens `index.html` with PDF.js library integration
4. **HTML Rendering**: PDF.js renders the PDF as HTML elements with text layer
5. **Enhanced Features**: Provides search, zoom, navigation, and text selection

## Technical Details

- **Manifest Version**: 3 (latest Chrome extension standard)
- **PDF.js Version**: 3.11.174 (latest stable)
- **Permissions**: 
  - `activeTab`: To interact with arXiv pages
  - `scripting`: To inject content scripts
- **Host Permissions**: `https://arxiv.org/*`
- **Content Scripts**: Automatically injected on arXiv abstract pages
- **External Libraries**: PDF.js loaded from CDN for reliability

## Development

To modify the extension:

1. Edit the source files in the `arxiv-pdf-viewer` directory
2. Go to `chrome://extensions/`
3. Click the refresh icon on the arXiv PDF Viewer extension
4. Test your changes on arXiv pages

### PDF.js Customization
The viewer uses PDF.js for rendering. You can customize:
- **Rendering quality**: Adjust canvas resolution and scaling
- **Text layer**: Modify text selection behavior and styling
- **Search highlighting**: Implement more sophisticated result highlighting
- **Page caching**: Add page preloading for better performance

## Browser Compatibility

- Chrome 88+ (Manifest V3 support required)
- Edge 88+ (Chromium-based)
- Other Chromium-based browsers
- Requires JavaScript enabled for PDF.js functionality

## Troubleshooting

### Button Not Appearing
- Make sure you're on an arXiv abstract page (`arxiv.org/abs/...`)
- Check that the extension is enabled in `chrome://extensions/`
- Try refreshing the page

### PDF Not Loading
- Check your internet connection
- Verify the arXiv paper exists and has a PDF
- Check browser console for PDF.js errors
- Ensure JavaScript is enabled

### Search Not Working
- Make sure the PDF has extractable text (not just images)
- Check that the search term is not too short
- Verify PDF.js loaded correctly

### Extension Not Working
- Ensure you're using a compatible browser
- Check the browser console for any error messages
- Try reinstalling the extension
- Verify PDF.js CDN is accessible

## Performance Notes

- **Large PDFs**: Very large PDFs may take time to load initially
- **Memory Usage**: PDF.js keeps pages in memory for better performance
- **Network**: Requires internet connection for PDF.js library and PDF loading

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 
// Shared utility functions

export function parseMarkdown(text) {
    if (!text) return '';
    // Convert **bold** to <strong>bold</strong>
    let html = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    const lines = html.split(/\r?\n/);
    let result = '';
    let listStack = []; // Stack to keep track of nested lists

    function openList(level) {
        while (listStack.length < level) {
            result += '<ul>';
            listStack.push('ul');
        }
    }

    function closeList(level) {
        while (listStack.length > level) {
            result += '</ul>';
            listStack.pop();
        }
    }

    for (let line of lines) {
        // Match bullet points with optional leading spaces for nesting
        const bulletMatch = line.match(/^(\s*)\* (.+)/);
        if (bulletMatch) {
            const indent = bulletMatch[1] || '';
            // Each 2 spaces = 1 nesting level (adjust as needed)
            const level = Math.floor(indent.length / 2) + 1;
            openList(level);
            closeList(level);
            result += `<li>${bulletMatch[2]}</li>`;
        } else {
            closeList(0);
            if (line.trim() !== '') {
                result += `<p>${line}</p>`;
            }
        }
    }
    closeList(0);
    return result;
} 
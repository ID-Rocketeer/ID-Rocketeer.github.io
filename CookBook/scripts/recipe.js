window.addEventListener('DOMContentLoaded', (event) => {
    try {
        // Get the path parts
        const path = window.location.pathname;
        const decodedPath = decodeURIComponent(path);
        const pathParts = decodedPath.split('/');

        // The category is the parent directory (second to last item)
        // clean up empty strings if path ends/starts with slash
        const cleanParts = pathParts.filter(part => part.length > 0);

        if (cleanParts.length >= 2) {
            // recipes/Side Dishes/HardNotBoiledEggs.html -> Side Dishes is at index -2
            const category = cleanParts[cleanParts.length - 2];

            // Find the category label
            const labels = document.querySelectorAll('span.label');
            for (const label of labels) {
                if (label.textContent.trim() === 'Category:') {
                    // The category text is the next sibling text node
                    // We want to replace the text in the parent TD, specifically following the span
                    const parentTd = label.parentNode;

                    // Clear existing text nodes after the label
                    let nextNode = label.nextSibling;
                    while (nextNode) {
                        const toRemove = nextNode;
                        nextNode = nextNode.nextSibling;
                        parentTd.removeChild(toRemove);
                    }

                    // Add the new category text, preserving the space after the colon if desired, 
                    // though usually the design might imply "Category: Value"
                    parentTd.appendChild(document.createTextNode(category));
                    break;
                }
            }
        }
    } catch (e) {
        console.error("Error setting category:", e);
    }
});

// Search and sort functionality for hotels page
document.addEventListener('DOMContentLoaded', function() {
    // Only run on hotels page
    if (window.location.pathname === '/hotels/') {
        // Auto-submit on sort change
        const sortSelect = document.getElementById('sortSelect');
        
        if (sortSelect) {
            sortSelect.addEventListener('change', function() {
                document.getElementById('searchForm').submit();
            });
        }
    }
}); 
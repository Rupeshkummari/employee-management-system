// Main JavaScript for Employee Management System

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Sidebar Toggle Logic
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleBtn = document.getElementById('sidebarToggle');
    
    if(sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                // Mobile layout
                sidebar.classList.toggle('mobile-open');
            } else {
                // Desktop layout
                sidebar.classList.toggle('collapsed');
            }
        });
    }

    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('mobile-open')) {
            if (!sidebar.contains(event.target) && !sidebarToggleBtn.contains(event.target)) {
                sidebar.classList.remove('mobile-open');
            }
        }
    });

    // 2. Alert Auto-dismiss
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 300); // Wait for transition
        }, 5000); // 5 seconds display
    });

    // 3. Table Column Sorting
    const sortableHeaders = document.querySelectorAll('th[data-sortable="true"]');
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', () => sortTable(header));
    });

    function sortTable(header) {
        const table = header.closest('table');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const index = Array.from(header.parentElement.children).indexOf(header);
        const order = header.getAttribute('data-order') === 'asc' ? 'desc' : 'asc';
        
        // Reset all headers
        table.querySelectorAll('th').forEach(th => th.removeAttribute('data-order'));
        header.setAttribute('data-order', order);
        
        // Sorting logic
        rows.sort((a, b) => {
            const aText = a.children[index].textContent.trim();
            const bText = b.children[index].textContent.trim();
            
            if (!isNaN(aText) && !isNaN(bText)) {
                return order === 'asc' ? aText - bText : bText - aText;
            }
            return order === 'asc' ? aText.localeCompare(bText) : bText.localeCompare(aText);
        });

        rows.forEach(row => tbody.appendChild(row));
    }

    // 4. Input Search / Filter
    const searchInput = document.getElementById('tableSearch');
    if(searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase();
            const rows = document.querySelectorAll('.table tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
});

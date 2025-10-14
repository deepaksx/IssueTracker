// IT Issue Tracker JavaScript

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');

    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirm delete action
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');

    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
                return false;
            }
        });
    });
});

// Form validation enhancement
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Add loading state to submit buttons
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && form.checkValidity()) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';

                // Re-enable after 5 seconds as a fallback
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
    });
});

// Table sorting (basic client-side)
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('table.table');

    tables.forEach(function(table) {
        const headers = table.querySelectorAll('th');

        headers.forEach(function(header, index) {
            header.style.cursor = 'pointer';
            header.setAttribute('title', 'Click to sort');

            header.addEventListener('click', function() {
                sortTable(table, index);
            });
        });
    });
});

function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    // Determine sort direction
    const currentSort = table.dataset.sortColumn;
    const currentDir = table.dataset.sortDir || 'asc';
    const newDir = (currentSort == columnIndex && currentDir === 'asc') ? 'desc' : 'asc';

    // Sort rows
    rows.sort(function(a, b) {
        const aCell = a.cells[columnIndex].textContent.trim();
        const bCell = b.cells[columnIndex].textContent.trim();

        // Try to parse as numbers
        const aNum = parseFloat(aCell);
        const bNum = parseFloat(bCell);

        let comparison = 0;
        if (!isNaN(aNum) && !isNaN(bNum)) {
            comparison = aNum - bNum;
        } else {
            comparison = aCell.localeCompare(bCell);
        }

        return newDir === 'asc' ? comparison : -comparison;
    });

    // Re-append rows
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });

    // Update sort state
    table.dataset.sortColumn = columnIndex;
    table.dataset.sortDir = newDir;

    // Update header indicators
    const headers = table.querySelectorAll('th');
    headers.forEach(function(header, index) {
        header.classList.remove('sorted-asc', 'sorted-desc');
        if (index === columnIndex) {
            header.classList.add('sorted-' + newDir);
        }
    });
}

// Search highlight
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');

    if (searchInput && searchInput.value) {
        highlightSearchTerms(searchInput.value);
    }
});

function highlightSearchTerms(searchTerm) {
    if (!searchTerm) return;

    const tableBody = document.querySelector('table tbody');
    if (!tableBody) return;

    const regex = new RegExp('(' + searchTerm + ')', 'gi');

    tableBody.querySelectorAll('td').forEach(function(cell) {
        const text = cell.textContent;
        if (regex.test(text)) {
            cell.innerHTML = text.replace(regex, '<mark>$1</mark>');
        }
    });
}

// Keyboard shortcuts
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keydown', function(e) {
        // Alt+N: New Issue (if admin)
        if (e.altKey && e.key === 'n') {
            const addBtn = document.querySelector('a[href*="add_issue"]');
            if (addBtn) {
                e.preventDefault();
                window.location.href = addBtn.href;
            }
        }

        // Alt+D: Dashboard
        if (e.altKey && e.key === 'd') {
            const dashboardBtn = document.querySelector('a[href*="dashboard"]');
            if (dashboardBtn) {
                e.preventDefault();
                window.location.href = dashboardBtn.href;
            }
        }

        // Alt+A: Audit Log
        if (e.altKey && e.key === 'a') {
            const auditBtn = document.querySelector('a[href*="audit_log"]');
            if (auditBtn) {
                e.preventDefault();
                window.location.href = auditBtn.href;
            }
        }

        // ESC: Close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(function(modal) {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) bsModal.hide();
            });
        }
    });
});

// Print functionality
function printIssue() {
    window.print();
}

// Export functionality helper
function downloadCSV(data, filename) {
    const blob = new Blob([data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Add tooltips to all elements with title attribute
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

console.log('IT Issue Tracker JavaScript loaded successfully');

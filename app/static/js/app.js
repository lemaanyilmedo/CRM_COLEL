// JavaScript for Kolel CRM System

document.addEventListener('DOMContentLoaded', function () {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function () {
        var alerts = document.querySelectorAll('.alert.alert-dismissible');
        alerts.forEach(function (alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize sidebar functionality
    initializeSidebar();

    // Initialize table functionality
    initializeTables();

    // Initialize search functionality  
    initializeSearch();

    // Confirm delete actions
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('btn-delete') || e.target.closest('.btn-delete')) {
            if (!confirm('האם אתה בטוח שברצונך למחוק? פעולה זו לא ניתנת לביטול.')) {
                e.preventDefault();
                return false;
            }
        }
    });

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Number formatting
    function formatCurrency(amount) {
        return new Intl.NumberFormat('he-IL', {
            style: 'currency',
            currency: 'ILS',
            minimumFractionDigits: 0
        }).format(amount);
    }

    // Time validation
    function validateTimeInput(input) {
        var timeRegex = /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/;
        return timeRegex.test(input.value);
    }

    // Add time validation to time inputs
    var timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(function (input) {
        input.addEventListener('blur', function () {
            if (!validateTimeInput(this)) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });

    // Auto-calculate late minutes
    function calculateLateMinutes(entryTime, expectedTime) {
        if (!entryTime || !expectedTime) return 0;

        var entry = new Date('1970-01-01T' + entryTime + ':00');
        var expected = new Date('1970-01-01T' + expectedTime + ':00');

        if (entry > expected) {
            return Math.floor((entry - expected) / (1000 * 60));
        }
        return 0;
    }

    // Auto-calculate early exit minutes
    function calculateEarlyExitMinutes(exitTime, expectedTime) {
        if (!exitTime || !expectedTime) return 0;

        var exit = new Date('1970-01-01T' + exitTime + ':00');
        var expected = new Date('1970-01-01T' + expectedTime + ':00');

        if (exit < expected) {
            return Math.floor((expected - exit) / (1000 * 60));
        }
        return 0;
    }

    // Search functionality
    function initializeSearch() {
        var searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', function () {
                var searchTerm = this.value.toLowerCase();
                var rows = document.querySelectorAll('tbody tr');

                rows.forEach(function (row) {
                    var text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        }
    }

    // Initialize search
    initializeSearch();

    // Loading states for buttons
    function showLoading(button) {
        var originalText = button.innerHTML;
        button.innerHTML = '<span class="loading-spinner me-2"></span>טוען...';
        button.disabled = true;

        return function () {
            button.innerHTML = originalText;
            button.disabled = false;
        };
    }

    // AJAX form submission
    function submitFormAjax(form, callback) {
        var formData = new FormData(form);
        var submitBtn = form.querySelector('button[type="submit"]');
        var hideLoading = showLoading(submitBtn);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                if (callback) callback(data);
            })
            .catch(error => {
                hideLoading();
                console.error('Error:', error);
                showNotification('אירעה שגיאה בשליחת הטופס', 'error');
            });
    }

    // Notification system
    function showNotification(message, type = 'info') {
        var alertClass = type === 'error' ? 'alert-danger' :
            type === 'success' ? 'alert-success' : 'alert-info';

        var alertDiv = document.createElement('div');
        alertDiv.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
        alertDiv.style.top = '20px';
        alertDiv.style.right = '20px';
        alertDiv.style.zIndex = '9999';
        alertDiv.style.minWidth = '300px';

        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        // Auto remove after 5 seconds
        setTimeout(function () {
            if (alertDiv.parentNode) {
                var bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }
        }, 5000);
    }

    // Export to Excel functionality
    function exportTableToExcel(tableId, filename = 'export.xlsx') {
        var table = document.getElementById(tableId);
        if (!table) return;

        // Create workbook
        var wb = XLSX.utils.book_new();
        var ws = XLSX.utils.table_to_sheet(table);

        // Add worksheet to workbook
        XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

        // Save file
        XLSX.writeFile(wb, filename);
    }

    // Date utilities
    function formatHebrewDate(date) {
        var hebrewMonths = [
            'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני',
            'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'
        ];

        var day = date.getDate();
        var month = hebrewMonths[date.getMonth()];
        var year = date.getFullYear();

        return `${day} ב${month} ${year}`;
    }

    // Hebrew day names
    function getHebrewDay(dayIndex) {
        var hebrewDays = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת'];
        return hebrewDays[dayIndex];
    }

    // Expose utility functions globally
    window.KolelCRM = {
        formatCurrency: formatCurrency,
        calculateLateMinutes: calculateLateMinutes,
        calculateEarlyExitMinutes: calculateEarlyExitMinutes,
        showNotification: showNotification,
        exportTableToExcel: exportTableToExcel,
        formatHebrewDate: formatHebrewDate,
        getHebrewDay: getHebrewDay,
        showLoading: showLoading,
        submitFormAjax: submitFormAjax
    };
});

// Sidebar functionality
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileToggle = document.getElementById('mobileToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const mainContent = document.getElementById('mainContent');

    // Desktop sidebar toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');

            // Save state to localStorage
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    }

    // Mobile sidebar toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function () {
            sidebar.classList.add('show');
            sidebarOverlay.classList.add('show');
        });
    }

    // Close sidebar on overlay click (mobile)
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function () {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        });
    }

    // Restore sidebar state from localStorage
    const sidebarCollapsed = localStorage.getItem('sidebarCollapsed');
    if (sidebarCollapsed === 'true') {
        sidebar.classList.add('collapsed');
    }

    // Set active nav item based on current URL
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');

    navLinks.forEach(function (link) {
        const href = link.getAttribute('href');
        if (href && currentPath === href) {
            link.classList.add('active');

            // Expand parent submenu if needed
            const submenu = link.closest('.submenu');
            if (submenu) {
                submenu.classList.add('show');
                const toggle = submenu.previousElementSibling;
                if (toggle) {
                    toggle.setAttribute('aria-expanded', 'true');
                }
            }
        }
    });
}

// Table functionality
function initializeTables() {
    // Select all functionality
    const selectAllCheckboxes = document.querySelectorAll('.select-all-checkbox');
    selectAllCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const table = checkbox.closest('.table-container');
            const rowCheckboxes = table.querySelectorAll('.row-checkbox');
            const bulkActions = table.querySelector('.bulk-actions');

            rowCheckboxes.forEach(function (rowCheckbox) {
                rowCheckbox.checked = checkbox.checked;
                updateRowSelection(rowCheckbox);
            });

            updateBulkActions(table);
        });
    });

    // Individual row selection
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    rowCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            updateRowSelection(checkbox);
            updateBulkActions(checkbox.closest('.table-container'));
        });
    });

    // Row click to edit (except when clicking on checkbox or action buttons)
    const tableRows = document.querySelectorAll('.table tbody tr[data-edit-url]');
    tableRows.forEach(function (row) {
        row.addEventListener('click', function (e) {
            // Don't navigate if clicking on checkbox, button, or link
            if (e.target.type === 'checkbox' ||
                e.target.closest('.btn') ||
                e.target.closest('a') ||
                e.target.closest('.row-checkbox')) {
                return;
            }

            const editUrl = row.getAttribute('data-edit-url');
            if (editUrl) {
                window.location.href = editUrl;
            }
        });
    });

    // Table sorting
    const sortableHeaders = document.querySelectorAll('.table thead th.sortable');
    sortableHeaders.forEach(function (header) {
        header.addEventListener('click', function () {
            sortTable(header);
        });
    });

    // Bulk action buttons
    const bulkActionButtons = document.querySelectorAll('.bulk-action-btn');
    bulkActionButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const action = button.getAttribute('data-action');
            const table = button.closest('.table-container');
            const selectedRows = getSelectedRows(table);

            if (selectedRows.length === 0) {
                alert('אנא בחר לפחות שורה אחת');
                return;
            }

            handleBulkAction(action, selectedRows);
        });
    });
}

// Update row selection visual state
function updateRowSelection(checkbox) {
    const row = checkbox.closest('tr');
    if (checkbox.checked) {
        row.classList.add('selected');
    } else {
        row.classList.remove('selected');
    }
}

// Update bulk actions visibility
function updateBulkActions(table) {
    const selectedCount = table.querySelectorAll('.row-checkbox:checked').length;
    const bulkActions = table.querySelector('.bulk-actions');
    const bulkActionsText = table.querySelector('.bulk-actions-text');
    const selectAllCheckbox = table.querySelector('.select-all-checkbox');

    if (bulkActions) {
        if (selectedCount > 0) {
            bulkActions.classList.add('show');
            if (bulkActionsText) {
                bulkActionsText.textContent = `נבחרו ${selectedCount} פריטים`;
            }
        } else {
            bulkActions.classList.remove('show');
        }
    }

    // Update select all checkbox state
    if (selectAllCheckbox) {
        const totalCheckboxes = table.querySelectorAll('.row-checkbox').length;
        selectAllCheckbox.indeterminate = selectedCount > 0 && selectedCount < totalCheckboxes;
        selectAllCheckbox.checked = selectedCount === totalCheckboxes && totalCheckboxes > 0;
    }
}

// Get selected rows data
function getSelectedRows(table) {
    const selectedCheckboxes = table.querySelectorAll('.row-checkbox:checked');
    const selectedRows = [];

    selectedCheckboxes.forEach(function (checkbox) {
        const row = checkbox.closest('tr');
        const id = checkbox.value || row.getAttribute('data-id');
        if (id) {
            selectedRows.push({
                id: id,
                row: row,
                checkbox: checkbox
            });
        }
    });

    return selectedRows;
}

// Handle bulk actions
function handleBulkAction(action, selectedRows) {
    const ids = selectedRows.map(row => row.id);

    switch (action) {
        case 'delete':
            if (confirm(`האם אתה בטוח שברצונך למחוק ${selectedRows.length} פריטים?`)) {
                // Send delete request
                fetch(window.location.pathname + '/bulk-delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ ids: ids })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            selectedRows.forEach(row => row.row.remove());
                            showNotification('הפריטים נמחקו בהצלחה', 'success');
                        } else {
                            showNotification('שגיאה במחיקת הפריטים', 'error');
                        }
                    })
                    .catch(error => {
                        showNotification('שגיאה במחיקת הפריטים', 'error');
                    });
            }
            break;

        case 'export':
            // Export selected rows
            window.location.href = window.location.pathname + '/export?ids=' + ids.join(',');
            break;

        case 'activate':
        case 'deactivate':
            // Update status
            fetch(window.location.pathname + '/bulk-status', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    ids: ids,
                    status: action === 'activate' ? 'active' : 'inactive'
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        showNotification('שגיאה בעדכון הסטטוס', 'error');
                    }
                })
                .catch(error => {
                    showNotification('שגיאה בעדכון הסטטוס', 'error');
                });
            break;
    }
}

// Table sorting
function sortTable(header) {
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const isAscending = !header.classList.contains('sort-asc');

    // Remove sort classes from all headers
    table.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });

    // Add sort class to current header
    header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.children[columnIndex].textContent.trim();
        const bValue = b.children[columnIndex].textContent.trim();

        // Check if values are numbers
        const aNum = parseFloat(aValue.replace(/[^\d.-]/g, ''));
        const bNum = parseFloat(bValue.replace(/[^\d.-]/g, ''));

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        }

        // String comparison
        return isAscending ?
            aValue.localeCompare(bValue, 'he') :
            bValue.localeCompare(aValue, 'he');
    });

    // Append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

// Utility functions
function getCSRFToken() {
    const tokenMeta = document.querySelector('meta[name="csrf-token"]');
    return tokenMeta ? tokenMeta.getAttribute('content') : '';
}

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    // Ctrl+S to save (prevent default browser save)
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        var saveBtn = document.querySelector('button[type="submit"], .btn-save');
        if (saveBtn && !saveBtn.disabled) {
            saveBtn.click();
        }
    }

    // Ctrl+N for new entry
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        var newBtn = document.querySelector('.btn-new, [href*="add"]');
        if (newBtn) {
            newBtn.click();
        }
    }

    // ESC to close modals
    if (e.key === 'Escape') {
        var openModal = document.querySelector('.modal.show');
        if (openModal) {
            var modal = bootstrap.Modal.getInstance(openModal);
            if (modal) modal.hide();
        }
    }
});
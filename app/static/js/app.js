// JavaScript for Kolel CRM System

document.addEventListener('DOMContentLoaded', function() {
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
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirm delete actions
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-delete') || e.target.closest('.btn-delete')) {
            if (!confirm('האם אתה בטוח שברצונך למחוק? פעולה זו לא ניתנת לביטול.')) {
                e.preventDefault();
                return false;
            }
        }
    });

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
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
    timeInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
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
            searchInput.addEventListener('input', function() {
                var searchTerm = this.value.toLowerCase();
                var rows = document.querySelectorAll('tbody tr');
                
                rows.forEach(function(row) {
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
        
        return function() {
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
        setTimeout(function() {
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

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
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
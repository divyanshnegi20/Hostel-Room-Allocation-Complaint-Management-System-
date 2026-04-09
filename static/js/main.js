// HostelHub - Main JavaScript

// Sidebar toggle
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('show');
}

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add animation classes to elements as they appear
    const animateElements = document.querySelectorAll('.stat-card, .card, .table-container');
    animateElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.05}s`;
        el.classList.add('animate-fade-in');
    });
});

// Close sidebar on mobile when clicking a nav link
document.querySelectorAll('.sidebar .nav-item a').forEach(link => {
    link.addEventListener('click', function() {
        if (window.innerWidth < 768) {
            document.getElementById('sidebar').classList.remove('show');
        }
    });
});

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

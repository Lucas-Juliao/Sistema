document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    if (menuToggle && sidebar && overlay) {
        menuToggle.addEventListener('click', function() {
            menuToggle.classList.toggle('active');
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        });

        overlay.addEventListener('click', function() {
            menuToggle.classList.remove('active');
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    }

    // Highlight active nav link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

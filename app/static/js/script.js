document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;

    // Sidebar toggle
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Set active nav link
    navLinks.forEach(link => {
        if (link.getAttribute('data-path') === currentPath) {
            link.classList.add('active');
        }
    });
});

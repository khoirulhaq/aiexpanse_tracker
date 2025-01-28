        // Mobile Sidebar Toggle
        const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
        const sidebarContainer = document.getElementById('sidebarContainer');

        mobileSidebarToggle.addEventListener('click', () => {
            sidebarContainer.classList.toggle('-translate-x-full');
        });

        // Optional: Close sidebar when clicking outside on mobile
        document.addEventListener('click', (event) => {
            if (!sidebarContainer.contains(event.target) && 
                !mobileSidebarToggle.contains(event.target) && 
                window.innerWidth < 768) {
                sidebarContainer.classList.add('-translate-x-full');
            }
        });
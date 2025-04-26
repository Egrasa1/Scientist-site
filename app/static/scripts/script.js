document.addEventListener('DOMContentLoaded', function() {
    const userMenu = document.querySelector('.user-menu');
    const dropdown = document.querySelector('.dropdown-menu');
    const avatar = document.querySelector('.user-avatar');
    
    if (userMenu && dropdown && avatar) {
        avatar.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdown.classList.toggle('show');
        });
        
        document.addEventListener('click', function(e) {
            if (!userMenu.contains(e.target)) {
                dropdown.classList.remove('show');
            }
        });
        
        dropdown.addEventListener('mouseenter', function() {
            dropdown.classList.add('show');
        });
        
        userMenu.addEventListener('mouseleave', function() {
            setTimeout(() => {
                if (!dropdown.matches(':hover')) {
                    dropdown.classList.remove('show');
                }
            }, 300);
        });
    }
});
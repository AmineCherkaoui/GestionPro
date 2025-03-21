 document.querySelectorAll('.actions-button,.dashboard-create-button').forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                document.querySelectorAll('.dropdown-menu.active').forEach(menu => {
                    if (menu !== e.currentTarget.nextElementSibling) {
                        menu.classList.remove('active');
                    }
                });

                const dropdown = button.nextElementSibling;
                dropdown.classList.toggle('active');
            });
        });
document.addEventListener('click', () => {
            document.querySelectorAll('.dropdown-menu.active').forEach(menu => {
                menu.classList.remove('active');
            });
        });

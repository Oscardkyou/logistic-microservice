// Скрипт для обработки интерактивных элементов на странице

document.addEventListener('DOMContentLoaded', function() {
    // Автоматическое закрытие уведомлений через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
    
    // Подтверждение при удалении примечания
    const deleteNoteButtons = document.querySelectorAll('a[href^="/delete_note/"]');
    deleteNoteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Вы уверены, что хотите удалить это примечание?')) {
                event.preventDefault();
            }
        });
    });
    
    // Анимация при добавлении нового примечания
    const noteForm = document.querySelector('form[action="/add_note"]');
    if (noteForm) {
        noteForm.addEventListener('submit', function() {
            const notesContainer = document.getElementById('notes-container');
            if (notesContainer) {
                notesContainer.classList.add('highlight-animation');
                setTimeout(function() {
                    notesContainer.classList.remove('highlight-animation');
                }, 1000);
            }
        });
    }
});

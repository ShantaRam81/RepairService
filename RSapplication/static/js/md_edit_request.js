document.addEventListener('DOMContentLoaded', function() {
    var modalEditRequest = document.querySelector('.modal-EditRequest');
    var closeEditRequestBtn = document.querySelector('.close-EditRequest');

    function openEditRequestModal() {
        modalEditRequest.style.opacity = '1';
        modalEditRequest.style.display = 'block'; // Добавляем это свойство, чтобы модальное окно было видимым
    }

    function closeEditRequestModal() {
        modalEditRequest.style.opacity = '0';
        setTimeout(() => {
            modalEditRequest.style.display = 'none';
        }, 200);
    }

    // Находим все кнопки редактирования и назначаем им событие click
    var editRequestButtons = document.querySelectorAll('.EditRequest_button');
    editRequestButtons.forEach(function(button) {
        button.addEventListener('click', openEditRequestModal);
    });

    closeEditRequestBtn.addEventListener('click', closeEditRequestModal);
});

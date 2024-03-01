        var modalHistory = document.querySelector('.modal-history');
        var modalHistoryOpener = document.querySelector('.history_button');
        var closeHistoryBtn = document.querySelector('.close-history');

        function openHistoryModal() {
            modalHistory.style.opacity = '1';
            modalHistory.style.display = 'block'; // Добавляем это свойство, чтобы модальное окно было видимым
        }

        function closeHistoryModal() {
            modalHistory.style.opacity = '0';
            setTimeout(() => {
                modalHistory.style.display = 'none';
            }, 200);
        }

        modalHistoryOpener.addEventListener('click', openHistoryModal);
        closeHistoryBtn.addEventListener('click', closeHistoryModal);
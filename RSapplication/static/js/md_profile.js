var modalProfile = document.querySelector('.modal-profile');
        var modalProfileOpener = document.querySelector('.profile_button');
        var closeProfileBtn = document.querySelector('.close-profile');

        function openProfileModal() {
            modalProfile.style.opacity = '1';
            modalProfile.style.display = 'block'; // Добавляем это свойство, чтобы модальное окно было видимым
        }

        function closeProfileModal() {
            modalProfile.style.opacity = '0';
            setTimeout(() => {
                modalProfile.style.display = 'none';
            }, 200);
        }

        modalProfileOpener.addEventListener('click', openProfileModal);
        closeProfileBtn.addEventListener('click', closeProfileModal);
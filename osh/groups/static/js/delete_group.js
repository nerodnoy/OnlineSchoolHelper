document.addEventListener('DOMContentLoaded', function () {
  var deleteButton = document.getElementById('deleteButton');
  var modal = document.getElementById('myModal');
  var closeModal = document.getElementById('closeModal');
  var confirmDeleteButton = document.getElementById('confirmDelete');

  deleteButton.addEventListener('click', function () {
    modal.style.display = 'block';
  });

  closeModal.addEventListener('click', function () {
    modal.style.display = 'none';
  });

  confirmDeleteButton.addEventListener('click', function () {
    // Ваш код для удаления всех групп
    alert('Все группы удалены!');
    modal.style.display = 'none';
  });

  window.addEventListener('click', function (event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });
});
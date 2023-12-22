function showConfirmationModal() {
    document.getElementById('confirmationModal').classList.remove('hidden');
}

function hideConfirmationModal() {
    document.getElementById('confirmationModal').classList.add('hidden');
}

function showDeleteConfirmation(studentName, studentId) {
    document.getElementById('confirmationModal_' + studentId).classList.remove('hidden');
}

function hideDeleteConfirmation(studentId) {
    document.getElementById('confirmationModal_' + studentId).classList.add('hidden');
}
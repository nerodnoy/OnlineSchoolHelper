// copy_students.js
document.addEventListener('DOMContentLoaded', function () {
    var clipboard = new ClipboardJS('#copyButton', {
        text: function () {
            var copiedText = '';
            copiedText += 'Ссылка на группу: ' + decodeURIComponent('{{ group.link }}') + '\n\n';
            copiedText += 'Ждём на занятии:\n\n';

            var studentsList = document.getElementById('studentsList');
            for (var i = 0; i < studentsList.children.length; i++) {
                copiedText += studentsList.children[i].innerText + '\n';
            }

            return copiedText;
        }
    });

    clipboard.on('success', function (e) {
        alert('Текст скопирован в буфер обмена!');
        e.clearSelection();
    });

    clipboard.on('error', function (e) {
        alert('Не удалось скопировать текст. Используйте сочетание клавиш.');
    });
});
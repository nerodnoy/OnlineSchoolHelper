document.addEventListener('DOMContentLoaded', function () {
    var clipboard = new ClipboardJS('#copyButton2', {
        text: function () {
            return document.getElementById('TextToParents').innerText;
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
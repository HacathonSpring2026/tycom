/*
========================================
画面読み込み時の初期処理
========================================
*/
document.addEventListener("DOMContentLoaded", function () {
    setupMenuSelect(".select-category", "#selected-command", "#category-id", "category");
    setupMenuSelect(".select-mode", "#selected-mode", "#mode-id", "mode");
});

/*
========================================
選択UI共通処理
========================================
*/
function setupMenuSelect(selector, displaySelector, inputSelector, dataName) {
    const items = document.querySelectorAll(selector);

    if (items.length === 0) {
        return;
    }

    const display = document.querySelector(displaySelector);
    const input = document.querySelector(inputSelector);

    // 先頭をデフォルト選択
    setSelected(items, items[0], display, input, dataName);

    items.forEach(function (item) {
        item.addEventListener("click", function () {
            setSelected(items, item, display, input, dataName);
        });
    });
}

function setSelected(items, selectedItem, display, input, dataName) {
    items.forEach(function (item) {
        item.classList.remove("selected");
    });

    selectedItem.classList.add("selected");

    const value = selectedItem.dataset[dataName];
    const text = selectedItem.textContent.trim();
    // 上部表示
    display.textContent = "> " + text;
    // Post用
    input.value = value;
}
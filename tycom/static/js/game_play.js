/*
========================================
画面読み込み時の初期処理
========================================
*/
const params = new URLSearchParams(window.location.search);
const mode = params.get("mode");
console.log(mode);
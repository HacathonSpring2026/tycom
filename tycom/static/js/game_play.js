let time = 30;
let timer = null;

document.addEventListener("DOMContentLoaded", function () {
    // URLパラメータ取得
    const params = new URLSearchParams(window.location.search);
    const mode = params.get("mode");
    const categoryName = params.get("category_name");

    // モード・カテゴリー表示
    const selectedMode = document.getElementById("selected-mode");
    const selectedCommand = document.getElementById("category_name");

    if (selectedMode) {
        selectedMode.textContent = mode ? `> ${mode}` : ">";
    }

    if (selectedCommand) {
        selectedCommand.textContent = categoryName ? `> ${categoryName}` : ">";
    }

    // 問題データ取得
    const questionDataText =
        document.getElementById("question-data").textContent;

    const questionDataJson = JSON.parse(questionDataText);
    const questionData = JSON.parse(questionDataJson);

    // 要素取得
    const questionText = document.getElementById("question-text");
    const answerInput = document.getElementById("answer-input");
    const answerHint = document.getElementById("answer-hint");

    let questionIndex = 0;
    let currentQuestion = null;
    let currentAnswer = "";
    let hintTimer = null;

    // STEP1：結果画面用の回答履歴
    const playResults = [];

    /**
     * 問題文・回答文のプレースホルダ置換
     */
    function replaceTargetText(text, question) {
        let replacedText = text;

        if (question.directory_name) {
            replacedText = replacedText.replace(
                "{directory_name}",
                question.directory_name
            );
        }

        if (question.file_name) {
            replacedText = replacedText.replace(
                "{file_name}",
                question.file_name
            );
        }

        return replacedText;
    }

    /**
     * 問題表示
     */
    function showQuestion() {
        currentQuestion = questionData[questionIndex];

        const question = replaceTargetText(
            currentQuestion.question,
            currentQuestion
        );

        currentAnswer = replaceTargetText(
            currentQuestion.answer,
            currentQuestion
        );

        questionText.textContent = `> ${question}`;

        answerInput.value = "";
        answerInput.classList.remove(
            "input-correct",
            "input-wrong"
        );

        answerHint.textContent = "";
        answerHint.classList.remove("show");

        if (hintTimer) {
            clearTimeout(hintTimer);
        }

        // 2秒後にヒント表示
        hintTimer = setTimeout(() => {
            answerHint.textContent = currentAnswer;
            answerHint.classList.add("show");
        }, 2000);

        answerInput.focus();
    }

    /**
     * 回答結果保存
     */
    function saveResult(isCorrect, typedValue) {
        const result = {
            question_id: currentQuestion.question_id,
            command: currentAnswer,
            description: currentQuestion.description,
            typed_value: typedValue,
            is_correct: isCorrect,
            challenge_count: 1
        };

        playResults.push(result);

        console.log("回答結果", result);
        console.log("全結果", playResults);
    }

    /**
     * 次の問題へ進む
     */
    function moveNextQuestion() {
        if (time <= 1) {
            return;
        }

        questionIndex++;

        if (questionIndex >= questionData.length) {
            questionIndex = 0;
        }

        showQuestion();
    }

    /**
     * 入力判定
     */
    answerInput.addEventListener("input", () => {
        const typedValue = answerInput.value;

        // 入力済み部分を非表示にして残りを表示
        answerHint.innerHTML =
            `<span style="visibility:hidden">${typedValue}</span>` +
            currentAnswer.slice(typedValue.length);

        // 色リセット
        answerInput.classList.remove(
            "input-correct",
            "input-wrong"
        );

        // 正誤判定
        if (currentAnswer.startsWith(typedValue)) {
            answerInput.classList.add("input-correct");
        } else {
            answerInput.classList.add("input-wrong");
        }

        // 完全一致
        if (
            typedValue === currentAnswer &&
            time > 1
        ) {
            saveResult(true, typedValue);
            moveNextQuestion();
        }
    });

    /**
     * Enterで不正解確定
     */
    answerInput.addEventListener("keydown", (event) => {
        if (event.key !== "Enter") {
            return;
        }

        const typedValue = answerInput.value;

        if (typedValue === "") {
            return;
        }

        if (typedValue !== currentAnswer) {
            saveResult(false, typedValue);
            moveNextQuestion();
        }
    });

    /**
     * タイマー開始
     */
    function startTimer() {
        const timeElement =
            document.getElementById("time-count");

        timer = setInterval(() => {
            time--;

            timeElement.textContent = time;

            if (time <= 0) {
                clearInterval(timer);
                timeUp();
            }
        }, 1000);
    }

    /**
     * 時間切れ処理
     */
    async function timeUp() {
        console.log("時間切れ");
        console.table(playResults);

        const sendData = {
            results: playResults
        };

        try {
            await fetch("/game/time-end/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(sendData)
            });

            // 結果画面へ遷移
            window.location.href = "/game/result/";

        } catch (error) {
            console.error(error);
        }
    }

    // 初回問題表示
    showQuestion();

    // タイマー開始
    startTimer();
});

/**
 * CookieからCSRFトークン取得
 */
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (
                cookie.substring(0, name.length + 1) ===
                name + "="
            ) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}
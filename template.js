const results = {
    right: 0,
    wrong: 0
};
function checkAnswer(index) {
    const row = document.querySelector("#row-" + index);
    const input = document.querySelector("#write-" + index);
    const button = document.querySelector("#button-" + index);
    const answerInput = document.querySelector("#answer-" + index);
    const answer = answerInput.value.toLowerCase();
    const word = input.value.toLowerCase();
    let cssInput = "";
    if (word === answer) {
        results.right += 1;
        cssInput = "success";
    } else {
        results.wrong += 1;
        cssInput = "danger";
        answerInput.setAttribute("type", "text");
        answerInput.setAttribute("disabled", "disabled");
    }
    button.setAttribute("disabled", "disabled");
    input.setAttribute("disabled", "disabled");
    input.classList.add(cssInput);
    row.classList.add("alert-" + cssInput);
    
}
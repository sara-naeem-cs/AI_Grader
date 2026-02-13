/*Results render function here (use template that's in the html file)*/
function getCategoriesElement(breakdown) {
    let breakdownContainer = `
    <div class="col-md-8">
        <h5 class="mb-3">Breakdown</h5>`;

    for (const category in breakdown) {
        const categoryData = breakdown[category];
        const [scoreEarned, maxTotal] = categoryData.score.split("/");
        const scoreEarnedNum = Number(scoreEarned);
        const maxTotalNum = Number(maxTotal);
        const widthPercent = (scoreEarnedNum / maxTotalNum) * 100;

        const tempCategory = `
            <div class="mb-3">
                <div class="d-flex justify-content-between">
                    <span class="fw-semibold">${category}</span>
                    <span class="text-warning fw-bold">${scoreEarnedNum} / ${maxTotalNum}</span>
                </div>
                <div class="progress">
                    <div class="progress-bar bg-warning" style="width: ${widthPercent}%"></div>
                </div>
                <small class="text-muted">${categoryData.feedback}</small>
            </div>`;

        breakdownContainer += tempCategory;
    }

    breakdownContainer += `</div>`;
    return breakdownContainer;
}

function getSuggestedFixesElement(suggestedFixes) {
    let suggestedFixesContainer = `
        <hr class="my-4">
        <h5>Suggested Fixes</h5>
        <div class="alert alert-warning shadow-sm">
            <ul class="mb-0">`;

    if (!Array.isArray(suggestedFixes) || suggestedFixes.length === 0) {
        suggestedFixesContainer += `<li>No suggested fixes. Full marks achieved.</li>`;
    } else {
        for (const fix of suggestedFixes) {
            suggestedFixesContainer += `<li>${fix}</li>`;
        }
    }

    suggestedFixesContainer += `
            </ul>
        </div>`;

    return suggestedFixesContainer;
}


function renderResults(resultElement, result) {
    console.log(result)
    const [score, maxTotal] = result.total_score.split("/");
    const totalScore = Number(score);
    const maxTotalNum = Number(maxTotal);
    const categoriesElement = getCategoriesElement(result.breakdown);
    const suggestedFixesElement = getSuggestedFixesElement(result.suggested_fixes);

    resultElement.innerHTML = `
        <div class="card shadow-lg border-0">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-4 text-center mb-4 mb-md-0">
                        <div class="score-circle mx-auto">
                            <div class="score-inner">
                                <h2 class="mb-0">${totalScore}</h2>
                                <small class="text-muted">/ ${maxTotalNum}</small>
                            </div>
                        </div>
                        <h5 class="mt-3 fw-bold">Overall Score</h5>
                    </div>
                    ${categoriesElement}
                </div>
                ${suggestedFixesElement}
            </div>
        </div>`;

}

document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const resultElement = document.getElementById("result");

    resultElement.innerText = "Grading...";
    try {
        const response = await fetch("http://127.0.0.1:8000/submit", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Request failed (${response.status}): ${errorText}`);
        }

        const data = await response.json();

        let result;
        try {
            result = JSON.parse(data.response);
        } catch {
            result = data.response;
        }

        renderResults(resultElement, result);
    } catch (err) {
        resultElement.innerText = `Error: ${err.message}`;
        console.error(err);
    }
});

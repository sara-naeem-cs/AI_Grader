document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault(); 

    const formData = new FormData(this);

    document.getElementById("result").innerText = "Grading...";
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

        // If your LLM already returns JSON string, parse it
        let parsed;
        try {
            parsed = JSON.parse(data.response);
        } catch {
            parsed = data.response;
        }

        document.getElementById("result").innerText =
            JSON.stringify(parsed, null, 2);
    } catch (err) {
        document.getElementById("result").innerText = `Error: ${err.message}`;
        console.error(err);
    }
});

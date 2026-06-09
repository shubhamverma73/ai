async function sendQuestion() {

    const question =
        document.getElementById("question").value;

    const chatBox =
        document.getElementById("chat-box");

    chatBox.innerHTML +=
        `<p><b>You:</b> ${question}</p>`;

    const response = await fetch(
        "/chat",
        {
            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
                question
            })
        }
    );

    const data = await response.json();

    /*chatBox.innerHTML +=
        `<p><b>Bot:</b> ${data.answer}</p>`;*/
    let sourcesHtml = "";

    if(data.sources){
        sourcesHtml =
            "<br><b>Sources:</b><br>";

        data.sources.forEach(source => {
            sourcesHtml +=
                `${source.source} (Page ${source.page})<br>`;
        });
    }

    chatBox.innerHTML += `
    <p>
        <b>Bot:</b> ${data.answer}
        ${sourcesHtml}
    </p>
    `;

    document.getElementById("question").value = "";
}
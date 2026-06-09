async function sendQuestion() {

    const input =
        document.getElementById(
            "question"
        );

    const question =
        input.value;

    if (!question.trim()) return;

    input.value = "";

    const sendBtn =
        document.querySelector(
            "button"
        );

    sendBtn.disabled = true;

    const chatBox =
        document.getElementById(
            "chat-box"
        );

    chatBox.innerHTML +=
        `<p><b>You:</b> ${question}</p>`;

    const botMessage =
        document.createElement("p");

    botMessage.innerHTML =
        `
    <b>Bot:</b>
    <span class="loading">
        🔍 Searching documents...
    </span>
    `;

    const loadingMessages = [
        "🔍 Searching documents...",
        "📄 Reading PDF content...",
        "🧠 Analyzing context...",
        "✍️ Generating answer..."
    ];

    let loadingIndex = 0;

    const loadingInterval =
        setInterval(() => {

            loadingIndex =
                (loadingIndex + 1)
                % loadingMessages.length;

            botMessage.innerHTML =
                `
            <b>Bot:</b>
            <span class="loading">
                ${loadingMessages[
                loadingIndex
                ]}
            </span>
            `;
        }, 1500);

    chatBox.appendChild(
        botMessage
    );

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

    const reader =
        response.body.getReader();

    const decoder =
        new TextDecoder();

    let answer = "";

    while (true) {

        const {
            value,
            done
        } = await reader.read();

        if (done) break;

        const chunk =
            decoder.decode(value);

        clearInterval(
            loadingInterval
        );

        sendBtn.disabled = false;

        if (
            chunk.includes(
                "__END_STREAM__"
            )
        ) {
            break;
        }

        answer += chunk;

        botMessage.innerHTML =
            `<b>Bot:</b> ${answer}`;

        chatBox.scrollTop =
            chatBox.scrollHeight;
    }

    const sourceResponse =
        await fetch("/sources");

    const sources =
        await sourceResponse.json();

    let sourcesHtml =
        "<br><br><b>Sources:</b><br>";

    sources.forEach(source => {

        sourcesHtml +=
            `${source.source}
             (Page ${source.page})
             <br>`;
    });

    botMessage.innerHTML =
        `<b>Bot:</b>
         ${answer}
         ${sourcesHtml}`;

    chatBox.scrollTop =
        chatBox.scrollHeight;
}
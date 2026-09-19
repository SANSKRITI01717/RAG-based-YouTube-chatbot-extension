const API_URL = "https://youtube-rag-chatbot-v2rs.onrender.com";

let videoId = null;

async function getCurrentVideo() {
    const tabs = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    const url = tabs[0]?.url;

    if (!url) {
        return null;
    }

    const parsedUrl = new URL(url);

    if (parsedUrl.hostname !== "www.youtube.com") {
        return null;
    }

    return parsedUrl.searchParams.get("v");
}


async function initialize() {
    videoId = await getCurrentVideo();

    const videoInfo = document.getElementById("videoInfo");

    if (!videoId) {
        videoInfo.textContent = "Open a YouTube video first.";
        return;
    }

    videoInfo.textContent = `Video ID: ${videoId}`;
}


document.getElementById("processBtn").addEventListener(
    "click",
    async () => {

        if (!videoId) {
            return;
        }

        const status = document.getElementById("status");

        status.textContent = "Processing video...";

        try {
            const response = await fetch(
                `${API_URL}/process-video`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        video_id: videoId
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Request failed"
                );
            }

            status.textContent = data.message;

        } catch (error) {
            status.textContent =
                `Error: ${error.message}`;
        }
    }
);


document.getElementById("askBtn").addEventListener(
    "click",
    async () => {

        if (!videoId) {
            return;
        }

        const question =
            document.getElementById("question").value.trim();

        if (!question) {
            return;
        }

        const answer =
            document.getElementById("answer");

        answer.textContent = "Thinking...";

        try {
            const response = await fetch(
                `${API_URL}/ask`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        video_id: videoId,
                        question: question
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Request failed"
                );
            }

            answer.textContent = data.answer;

        } catch (error) {
            answer.textContent =
                `Error: ${error.message}`;
        }
    }
);


initialize();
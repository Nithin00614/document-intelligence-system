const API_BASE = "http://127.0.0.1:8002";

const uploadBtn = document.getElementById("uploadBtn");
const queryBtn = document.getElementById("queryBtn");

const uploadStatus = document.getElementById("uploadStatus");

const answer = document.getElementById("answer");
const confidence = document.getElementById("confidence");
const confidenceScore = document.getElementById("confidenceScore");
const processingTime = document.getElementById("processingTime");

const citations = document.getElementById("citations");


// ======================================================
// Upload PDFs
// ======================================================

uploadBtn.addEventListener("click", async () => {

    const files = document.getElementById("pdfFiles").files;

    if (files.length === 0) {

        alert("Please select at least one PDF.");

        return;
    }

    uploadBtn.disabled = true;

    uploadBtn.innerHTML = "⏳ Uploading...";

    uploadStatus.innerHTML = "";

    const formData = new FormData();

    for (const file of files) {

        formData.append("files", file);

    }

    try {

        const response = await fetch(

            `${API_BASE}/upload/`,

            {

                method: "POST",

                body: formData

            }

        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(

                data.detail ||

                "Upload failed."

            );

        }

        uploadStatus.style.background = "#ecfdf5";

        uploadStatus.style.borderLeft = "5px solid #22c55e";

        uploadStatus.style.color = "#166534";

        uploadStatus.innerHTML = `

        <h3>✅ Upload Successful</h3>

        <br>

        <strong>Documents Indexed:</strong>
        ${data.uploaded_files}

        <br>

        <strong>Chunks Generated:</strong>
        ${data.processed_chunks}

        `;

    }

    catch (error) {

        uploadStatus.style.background = "#fef2f2";

        uploadStatus.style.borderLeft = "5px solid #dc2626";

        uploadStatus.style.color = "#991b1b";

        uploadStatus.innerHTML = `

        <strong>❌ Upload Failed</strong>

        <br><br>

        ${error.message}

        `;

    }

    finally {

        uploadBtn.disabled = false;

        uploadBtn.innerHTML = "Upload Documents";

    }

});


// ======================================================
// Query
// ======================================================

queryBtn.addEventListener("click", async () => {

    const question =

        document.getElementById("question").value.trim();

    if (!question) {

        alert("Please enter a question.");

        return;

    }

    const mode =

        document.querySelector(

            'input[name="mode"]:checked'

        ).value;

    queryBtn.disabled = true;

    queryBtn.innerHTML = "⏳ Generating...";

    answer.innerHTML =

        "Generating answer...";

    confidence.innerHTML = "-";

    confidenceScore.innerHTML = "-";

    processingTime.innerHTML = "-";

    citations.innerHTML = "";

    try {

        const response = await fetch(

            `${API_BASE}/query/`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    question,

                    mode

                })

            }

        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(

                data.detail ||

                "Query failed."

            );

        }

        answer.innerText = data.answer;

        if (data.confidence === "High") {

            confidence.innerHTML = "🟢 High";

            confidence.className = "high";

        }

        else if (data.confidence === "Medium") {

            confidence.innerHTML = "🟡 Medium";

            confidence.className = "medium";

        }

        else {

            confidence.innerHTML = "🔴 Low";

            confidence.className = "low";

        }

        confidenceScore.innerHTML =

            Number(data.confidence_score).toFixed(3);

        processingTime.innerHTML =

            `${data.processing_time} sec`;

        citations.innerHTML = "";

        if (data.citations.length === 0) {

            citations.innerHTML =

                "<p>No citations available.</p>";

        }

        else {

            data.citations.forEach(

                citation => {

                    const card =

                        document.createElement("div");

                    card.className =

                        "citation-card";

                    card.innerHTML = `

                        <strong>

                        📄 ${citation.filename}

                        </strong>

                        <br><br>

                        📑 Page ${citation.page_number}

                        <br><br>

                        <div class="source-preview">

                        ${citation.source_preview}

                        </div>

                    `;

                    citations.appendChild(card);

                }

            );

        }

        document.querySelector("#answer").scrollIntoView({

            behavior: "smooth"

        });

    }

    catch (error) {

        answer.innerHTML =

            `❌ ${error.message}`;

    }

    finally {

        queryBtn.disabled = false;

        queryBtn.innerHTML =

            "Ask Question";

    }

});
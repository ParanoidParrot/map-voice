from fastapi.responses import HTMLResponse


def get_demo_html() -> HTMLResponse:
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MapVoice Demo</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
            :root {
                --bg: #111827;
                --bg-soft: #1F2937;
                --card: rgba(31, 41, 55, 0.82);
                --card-border: rgba(209, 213, 219, 0.18);
                --accent: #A7C957;
                --accent-light: #CDE990;
                --white: #F9FAFB;
                --text: #F9FAFB;
                --muted: #D1D5DB;
                --warning: #FBBF24;
                --danger: #FB7185;
                --shadow: rgba(167, 201, 87, 0.12);
            }

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;
                font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                color: var(--white);
                background:
                    radial-gradient(circle at top left, rgba(20, 184, 166, 0.28), transparent 34%),
                    radial-gradient(circle at 80% 20%, rgba(94, 234, 212, 0.12), transparent 30%),
                    linear-gradient(135deg, #031113 0%, var(--bg) 48%, #021012 100%);
            }

            .page {
                width: min(1080px, 100%);
                margin: 0 auto;
                padding: 36px 20px 48px;
            }

            .nav {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 58px;
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 10px;
                color: var(--white);
                font-weight: 800;
                letter-spacing: 0.08em;
                
            }

            .logo {
                width: 36px;
                height: 36px;
                border-radius: 12px;
                display: grid;
                place-items: center;
                color: #03201d;
                font-weight: 900;
                background: linear-gradient(135deg, var(--accent-light), var(--accent));
                box-shadow: 0 0 28px var(--shadow);
            }

            .pill {
                border: 1px solid var(--card-border);
                background: rgba(255,255,255,0.06);
                color: var(--muted);
                padding: 8px 12px;
                border-radius: 999px;
                font-size: 13px;
            }

            .hero {
                display: grid;
                grid-template-columns: 1.05fr 0.95fr;
                gap: 30px;
                align-items: start;
            }

            .eyebrow {
                color: var(--accent-light);
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                font-size: 13px;
                margin-bottom: 18px;
            }

            h1 {
                font-size: clamp(42px, 7vw, 82px);
                line-height: 0.94;
                letter-spacing: -0.06em;
                margin: 0;
            }

            .animated-word {
                display: inline-block;
                color: var(--accent-light);
                text-shadow: 0 0 24px rgba(94, 234, 212, 0.34);
                animation: shimmer 2.4s ease-in-out infinite;
            }

            @keyframes shimmer {
                0%, 100% {
                    opacity: 1;
                    transform: translateY(0);
                    filter: drop-shadow(0 0 0 rgba(94, 234, 212, 0));
                }
                50% {
                    opacity: 0.84;
                    transform: translateY(-2px);
                    filter: drop-shadow(0 0 12px rgba(94, 234, 212, 0.65));
                }
            }

            .subtitle {
                color: var(--muted);
                font-size: 19px;
                line-height: 1.65;
                margin: 24px 0 28px;
                max-width: 680px;
            }

            .hero-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                margin-bottom: 28px;
            }

            .button-link {
                text-decoration: none;
                color: #021916;
                background: var(--accent-light);
                font-weight: 800;
                border-radius: 999px;
                padding: 12px 18px;
                box-shadow: 0 12px 30px rgba(20, 184, 166, 0.25);
            }

            .button-link.secondary {
                color: var(--white);
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid var(--card-border);
                box-shadow: none;
            }

            .demo-card {
                background: linear-gradient(180deg, rgba(255,255,255,0.105), rgba(255,255,255,0.055));
                border: 1px solid var(--card-border);
                border-radius: 28px;
                padding: 22px;
                box-shadow: 0 24px 90px rgba(0,0,0,0.35);
                backdrop-filter: blur(18px);
            }

            .demo-card h2 {
                margin: 0 0 8px;
                font-size: 22px;
            }

            .demo-card p {
                color: var(--muted);
                margin-top: 0;
            }

            textarea {
                width: 100%;
                min-height: 124px;
                resize: vertical;
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,0.16);
                background: rgba(0, 0, 0, 0.24);
                color: var(--white);
                padding: 15px;
                font-size: 15px;
                outline: none;
                line-height: 1.5;
            }

            textarea:focus {
                border-color: var(--accent-light);
                box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.14);
            }

            button {
                border: none;
                cursor: pointer;
                border-radius: 999px;
                padding: 13px 16px;
                font-size: 15px;
                font-weight: 800;
                color: #041b18;
                background: linear-gradient(135deg, var(--accent-light), var(--accent));
                transition: transform 0.16s ease, box-shadow 0.16s ease, opacity 0.16s ease;
                box-shadow: 0 14px 34px rgba(20, 184, 166, 0.22);
            }

            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 16px 42px rgba(20, 184, 166, 0.28);
            }

            button:disabled {
                opacity: 0.65;
                cursor: wait;
                transform: none;
            }

            .sample-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 10px;
                margin: 16px 0;
            }

            .sample {
                color: var(--white);
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid var(--card-border);
                box-shadow: none;
                font-weight: 650;
                text-align: left;
                border-radius: 16px;
                padding: 11px 13px;
            }

            .sample.selected {
                color: #111827;
                background: var(--accent-light);
                border-color: var(--accent-light);
            }

            .language-note {
                margin: 4px 0 12px;
                color: var(--muted);
                font-size: 13px;
                line-height: 1.5;
            }

            .primary-action {
                width: 100%;
                margin-top: 4px;
            }

            .status {
                margin-top: 14px;
                color: var(--accent-light);
                font-weight: 700;
                min-height: 24px;
            }

            .status.error {
                color: var(--danger);
            }

            .output-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 16px;
                margin-top: 28px;
            }

            .output-card {
                background: var(--card);
                border: 1px solid var(--card-border);
                border-radius: 24px;
                padding: 18px;
                min-height: 170px;
            }

            .output-card h3 {
                margin: 0 0 12px;
                font-size: 15px;
                color: var(--accent-light);
                text-transform: uppercase;
                letter-spacing: 0.09em;
            }

            code {
                color: var(--white);
                white-space: pre-wrap;
                word-break: break-word;
                line-height: 1.55;
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                font-size: 14px;
            }

            audio {
                width: 100%;
                margin-top: 14px;
            }

            .features {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 16px;
                margin-top: 34px;
            }

            .feature {
                background: rgba(255,255,255,0.06);
                border: 1px solid var(--card-border);
                border-radius: 22px;
                padding: 18px;
            }

            .feature strong {
                display: block;
                color: var(--white);
                margin-bottom: 8px;
            }

            .feature span {
                color: var(--muted);
                font-size: 14px;
                line-height: 1.5;
            }

            .provider-note {
                margin-top: 18px;
                padding: 14px 16px;
                border: 1px solid var(--card-border);
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.055);
                color: var(--muted);
                font-size: 14px;
                line-height: 1.6;
                text-align: center;
            }

            .provider-note strong {
                color: var(--accent-light);
            }

            .footer {
                margin-top: 34px;
                color: rgba(255,255,255,0.56);
                font-size: 14px;
                text-align: center;
            }

            .typing {
                position: relative;
            }

            .typing::after {
                content: "";
                display: inline-block;
                width: 8px;
                height: 1.1em;
                margin-left: 3px;
                background: var(--accent-light);
                vertical-align: -2px;
                animation: blink 0.9s steps(2, start) infinite;
            }

            @keyframes blink {
                50% {
                    opacity: 0;
                }
            }

            @media (max-width: 880px) {
                .hero {
                    grid-template-columns: 1fr;
                }

                .output-grid,
                .features {
                    grid-template-columns: 1fr;
                }

                .sample-grid {
                    grid-template-columns: 1fr;
                }

                .nav {
                    margin-bottom: 36px;
                }
            }
        </style>
    </head>

    <body>
        <main class="page">
            <nav class="nav">
                <div class="brand">
                    <div class="logo">MV</div>
                    <span>MapVoice</span>
                </div>
                <div class="pill">Indian navigation pronunciation engine</div>
            </nav>

            <section class="hero">
                <div>
                    <div class="eyebrow">speech-aware routing text</div>
                    <h1>
                        Make Indian place names sound speech-friendly.
                    </h1>
                    <p class="subtitle">
                        MapVoice normalizes navigation-style instructions, expands road abbreviations,
                        applies Indian place-name pronunciation hints, and sends the speech-friendly text
                        to Sarvam AI Text-to-Speech for raw vs normalized audio comparison along with native 
                        language speech generation.
                    </p>

                    <div class="hero-actions">
                        <a class="button-link" href="https://github.com/ParanoidParrot/nav-pronunciation-engine" target="_blank">View Source</a>
                        <a class="button-link secondary" href="/docs" target="_blank">API docs</a>
                    </div>

                    <div class="features">
                        <div class="feature">
                            <strong>Suffix-aware</strong>
                            <span>Splits words like Hosakerehalli into pronunciation-friendly parts.</span>
                        </div>
                        <div class="feature">
                            <strong>Road aware</strong>
                            <span>Expands NH, road units, distances, and ordinals for speech.</span>
                        </div>
                        <div class="feature">
                            <strong>Sarvam TTS</strong>
                            <span>Speech synthesis is powered by Sarvam AI Text-to-Speech.</span>
                        </div>
                        <div class="feature">
                            <strong>Prototype app</strong>
                            <span>Backend + Android MVP for portfolio and Play testing.</span>
                        </div>
                    </div>
                </div>

                <div id="demo" class="demo-card">
                    <h2>Live pronunciation demo</h2>
                    <p>Enter a navigation instruction or pick a sample.</p>

                    <textarea id="instruction">Turn left onto NH 44 after 500m near MG Marg</textarea>

                    <div class="sample-grid">
                        <button class="sample" data-lang="hi-IN" onclick="setSample(this, 'Turn right after 100m near Sansad Marg', 'hi-IN', 'Hindi')">Hindi : Sansad Marg</button>
                        <button class="sample" data-lang="bn-IN" onclick="setSample(this, 'Continue to Rabindra Sarani', 'bn-IN', 'Bengali')">Bengali : Rabindra Sarani</button>
                        <button class="sample" data-lang="kn-IN" onclick="setSample(this, 'Turn left after 500m to Hosakerehalli', 'kn-IN', 'Kannada')">Kannada : Hosakerehalli</button>
                        <button class="sample" data-lang="mr-IN" onclick="setSample(this, 'Head towards Shivaji Peth', 'mr-IN', 'Marathi')">Marathi : Shivaji Peth</button>
                        <button class="sample" data-lang="te-IN" onclick="setSample(this, 'Continue towards Ameerpet Veedhi', 'te-IN', 'Telugu')">Telugu : Ameerpet Veedhi</button>
                        <button class="sample" data-lang="ta-IN" onclick="setSample(this, 'Take the next right near Anna Salai', 'ta-IN', 'Tamil')">Tamil : Anna Salai</button>
                    </div>

                    <div id="languageNote" class="language-note">
                        Select a language sample to also generate native-language navigation audio.
                    </div>

                    <button id="generateButton" class="primary-action" onclick="compareAudio()">
                        Normalize + Generate Audio
                    </button>

                    <div id="status" class="status"></div>
                </div>
            </section>

            <section class="output-grid">
                <div class="output-card">
                    <h3>Original</h3>
                    <code id="originalText">Waiting for input...</code>
                    <audio id="rawAudio" controls preload="none"></audio>
                </div>

                <div class="output-card">
                    <h3>Normalized</h3>
                    <code id="normalizedText">Waiting for output...</code>
                </div>

                <div class="output-card">
                    <h3>Speech Text</h3>
                    <code id="speechText">Waiting for pronunciation hints...</code>
                    <audio id="normalizedAudio" controls preload="none"></audio>
                </div>

                <div class="output-card">
                    <h3 id="nativeHeading">Native Language</h3>
                    <code id="translatedText">Select a language to generate native-language speech...</code>
                    <audio id="nativeAudio" controls preload="none"></audio>
                    <div id="nativeError" style="display:none; color:#FB7185; margin-top:10px;"></div>
                </div>
            </section>

            <div class="provider-note">
                Speech synthesis is powered by <strong>Sarvam AI Text-to-Speech</strong>. 
                MapVoice adds normalization, abbreviation expansion, suffix splitting, and pronunciation hints before generating speech.
            </div>

            <div class="footer">
                MapVoice · pronunciation-aware normalization for Indian navigation-style text
            </div>
        </main>

        <script>
            let selectedLanguageCode = null;
            let selectedLanguageName = null;

            function setSample(button, text, languageCode, languageName) {
                document.getElementById("instruction").value = text;
                selectedLanguageCode = languageCode;
                selectedLanguageName = languageName;

                document.querySelectorAll(".sample").forEach((sample) => {
                    sample.classList.remove("selected");
                });
                button.classList.add("selected");

                document.getElementById("languageNote").textContent =
                    languageName + " selected — native-language audio will be generated.";
                document.getElementById("nativeHeading").textContent =
                    languageName + " Audio";

                clearOutputs(false);
            }

            function clearOutputs(resetLanguage = true) {
                document.getElementById("originalText").textContent = "Waiting for input...";
                document.getElementById("normalizedText").textContent = "Waiting for output...";
                document.getElementById("speechText").textContent = "Waiting for pronunciation hints...";
                document.getElementById("translatedText").textContent = selectedLanguageCode
                    ? "Waiting for " + selectedLanguageName + " translation..."
                    : "Select a language to generate native-language speech...";
                document.getElementById("status").textContent = "";

                const rawAudio = document.getElementById("rawAudio");
                const normalizedAudio = document.getElementById("normalizedAudio");
                const nativeAudio = document.getElementById("nativeAudio");

                [rawAudio, normalizedAudio, nativeAudio].forEach((audio) => {
                    audio.removeAttribute("src");
                    audio.load();
                });

                if (resetLanguage) {
                    selectedLanguageCode = null;
                    selectedLanguageName = null;
                    document.querySelectorAll(".sample").forEach((sample) => {
                        sample.classList.remove("selected");
                    });
                    document.getElementById("languageNote").textContent =
                        "Select a language sample to also generate native-language navigation audio.";
                    document.getElementById("nativeHeading").textContent = "Native Language";
                }
            }

            function typeText(element, text, delay = 14) {
                element.textContent = "";
                element.classList.add("typing");

                let i = 0;
                const timer = setInterval(() => {
                    element.textContent += text.charAt(i);
                    i += 1;

                    if (i >= text.length) {
                        clearInterval(timer);
                        element.classList.remove("typing");
                    }
                }, delay);
            }

            async function compareAudio() {
                const instruction = document.getElementById("instruction").value;
                const generateButton = document.getElementById("generateButton");
                const status = document.getElementById("status");

                const originalText = document.getElementById("originalText");
                const normalizedText = document.getElementById("normalizedText");
                const speechText = document.getElementById("speechText");
                const translatedText = document.getElementById("translatedText");
                const rawAudio = document.getElementById("rawAudio");
                const normalizedAudio = document.getElementById("normalizedAudio");
                const nativeAudio = document.getElementById("nativeAudio");
                const nativeError = document.getElementById("nativeError");

                generateButton.disabled = true;
                status.classList.remove("error");
                status.textContent = selectedLanguageCode
                    ? "Generating English comparison + " + selectedLanguageName + " audio..."
                    : "Generating speech comparison...";

                originalText.textContent = "Loading...";
                normalizedText.textContent = "Loading...";
                speechText.textContent = "Loading...";
                translatedText.textContent = selectedLanguageCode
                    ? "Translating to " + selectedLanguageName + "..."
                    : "Select a language to generate native-language speech...";

                [rawAudio, normalizedAudio, nativeAudio].forEach((audio) => {
                    audio.removeAttribute("src");
                    audio.load();
                });

                try {
                    const requestBody = { instruction };
                    if (selectedLanguageCode) {
                        requestBody.target_language_code = selectedLanguageCode;
                    }

                    const response = await fetch("/demo/compare", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(requestBody)
                    });

                    if (!response.ok) {
                        const errorText = await response.text();
                        throw new Error("Backend error " + response.status + ": " + errorText);
                    }

                    const data = await response.json();

                    typeText(originalText, data.original_text || instruction);
                    typeText(normalizedText, data.normalized_text || "No normalized text returned.");
                    typeText(speechText, data.speech_text || data.normalized_text || "No speech text returned.");

                    rawAudio.src = data.raw_audio_url;
                    normalizedAudio.src = data.normalized_audio_url;
                    rawAudio.load();
                    normalizedAudio.load();

                    if (data.translated_text && data.native_audio_url) {

                        typeText(translatedText, data.translated_text);

                        nativeAudio.src = data.native_audio_url;
                        nativeAudio.load();
                        nativeAudio.style.display = "block";

                        document.getElementById("nativeHeading").textContent =
                            (data.target_language_name || selectedLanguageName || "Native")
                            + " Audio";

                        status.textContent =
                            "Ready. Compare raw, normalized, and native-language audio.";

                    } else {

                        // Clear any native audio from the previous request.
                        nativeAudio.pause();
                        nativeAudio.removeAttribute("src");
                        nativeAudio.load();
                        nativeAudio.style.display = "none";

                        // If translation succeeded but TTS failed, still show the translation.
                        if (data.translated_text) {
                            typeText(translatedText, data.translated_text);
                        } else {
                            translatedText.textContent =
                                "Select a language sample to generate native-language speech.";
                        }

                        status.textContent =
                            "Ready. Raw and normalized English audio are available.";
                    }


                    if (data.native_audio_error) {

                        nativeError.textContent = data.native_audio_error;
                        nativeError.style.display = "block";

                    } else {

                        nativeError.textContent = "";
                        nativeError.style.display = "none";
                    }
                } catch (err) {
                    status.classList.add("error");
                    status.textContent = "Error: " + err.message;

                    originalText.textContent = "Error";
                    normalizedText.textContent = "Error";
                    speechText.textContent = "Error";
                    translatedText.textContent = "Error";
                } finally {
                    generateButton.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
import html
import time

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Lumen",
    page_icon="◐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────── Design system ─────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap');

:root {
    --bg: #0b0a09;
    --surface: #131211;
    --surface-2: #1a1816;
    --line: rgba(255, 246, 230, 0.09);
    --line-strong: rgba(255, 246, 230, 0.18);
    --text: #ece7df;
    --muted: #8d877c;
    --faint: #5f5a52;
    --accent: #c9a86a;
    --accent-soft: rgba(201, 168, 106, 0.12);
    --good: #8fb996;
    --bad: #c8776b;
    --serif: 'Instrument Serif', Georgia, serif;
    --sans: 'Geist', 'Inter', system-ui, sans-serif;
    --mono: 'Geist Mono', ui-monospace, monospace;
}

html, body, .stApp, [class*="css"] {
    font-family: var(--sans) !important;
    color: var(--text);
    -webkit-font-smoothing: antialiased;
}
button, input, textarea { font-family: var(--sans) !important; }

/* Canvas: warm black, faint top glow, fine grain */
.stApp {
    background:
        radial-gradient(1100px 520px at 50% -18%, rgba(201,168,106,0.075), transparent 62%),
        var(--bg);
}
.stApp::before {
    content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: .5;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 .96  0 0 0 0 .9  0 0 0 .035 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}

#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none; }

.block-container {
    max-width: 820px;
    padding-top: 1.6rem;
    padding-bottom: 8rem;
}

/* ── Top bar ── */
.topbar {
    display: flex; justify-content: space-between; align-items: center;
    padding-bottom: 1.1rem; border-bottom: 1px solid var(--line);
}
.wordmark { font-family: var(--serif); font-size: 1.55rem; letter-spacing: -0.01em; }
.wordmark i { color: var(--accent); }
.status {
    font-family: var(--mono); font-size: 11px; letter-spacing: .08em;
    text-transform: uppercase; color: var(--muted);
    display: flex; align-items: center; gap: 9px;
}
.status .dot { width: 6px; height: 6px; border-radius: 50%; }
.status .dot.on { background: var(--good); box-shadow: 0 0 0 4px rgba(143,185,150,.14); }
.status .dot.off { background: var(--bad); box-shadow: 0 0 0 4px rgba(200,119,107,.14); }

/* ── Hero ── */
.hero { padding: 5.5rem 0 3rem; animation: rise .8s cubic-bezier(.2,.7,.2,1) both; }
.eyebrow {
    font-family: var(--mono); font-size: 11px; letter-spacing: .16em;
    text-transform: uppercase; color: var(--accent); margin-bottom: 1.6rem;
}
.hero h1 {
    font-family: var(--serif) !important; font-weight: 400 !important;
    font-size: clamp(3rem, 7.2vw, 5.4rem); line-height: .98; letter-spacing: -0.025em;
    margin: 0; padding: 0; color: var(--text);
}
.hero h1 i { color: var(--accent); }
.hero p {
    margin: 1.8rem 0 0; max-width: 470px; color: var(--muted);
    font-size: 1.02rem; line-height: 1.65; font-weight: 300;
}

.principles {
    display: grid; grid-template-columns: repeat(3, 1fr);
    border-top: 1px solid var(--line); margin: 1rem 0 3rem;
}
.principle { padding: 1.3rem 1.4rem 0 0; }
.principle + .principle { padding-left: 1.4rem; border-left: 1px solid var(--line); }
.principle .n { font-family: var(--mono); font-size: 11px; color: var(--faint); letter-spacing: .1em; }
.principle .t { font-size: .95rem; font-weight: 500; margin: .55rem 0 .3rem; }
.principle .d { font-size: .84rem; color: var(--muted); line-height: 1.55; font-weight: 300; }

.label {
    font-family: var(--mono); font-size: 11px; letter-spacing: .14em;
    text-transform: uppercase; color: var(--faint); margin: 0 0 .7rem;
}

/* Suggestion rows */
div[class*="st-key-sug_"] button {
    width: 100%; display: flex !important; justify-content: space-between !important;
    align-items: center; text-align: left;
    background: transparent !important; border: none !important; border-radius: 0 !important;
    border-top: 1px solid var(--line) !important;
    padding: 1.05rem .2rem !important; color: var(--text) !important;
    font-size: 1.02rem; font-weight: 400; transition: all .25s ease;
}
div[class*="st-key-sug_"]:last-of-type button { border-bottom: 1px solid var(--line) !important; }
div[class*="st-key-sug_"] button > div { flex: 1; text-align: left; }
div[class*="st-key-sug_"] button::after {
    content: "→"; color: var(--faint); transition: all .25s ease; font-family: var(--mono);
}
div[class*="st-key-sug_"] button:hover { padding-left: .8rem !important; color: var(--accent) !important; }
div[class*="st-key-sug_"] button:hover::after { color: var(--accent); transform: translateX(4px); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div:first-child { padding-top: .4rem; }
.side-brand { font-family: var(--serif); font-size: 1.9rem; margin: .4rem 0 .2rem; letter-spacing: -0.01em; }
.side-brand i { color: var(--accent); }
.side-tag { font-size: .8rem; color: var(--muted); font-weight: 300; margin-bottom: 1.8rem; }
.sec {
    font-family: var(--mono); font-size: 10.5px; letter-spacing: .14em;
    text-transform: uppercase; color: var(--faint);
    display: flex; gap: 10px; margin: 1.7rem 0 .8rem;
}
.sec b { color: var(--accent); font-weight: 500; }

.ledger { border: 1px solid var(--line); border-radius: 10px; background: var(--bg); }
.ledger .file {
    padding: 14px 16px; border-bottom: 1px solid var(--line);
    font-size: .9rem; font-weight: 500; line-height: 1.4; word-break: break-word;
}
.ledger .row {
    display: flex; justify-content: space-between; padding: 10px 16px;
    font-family: var(--mono); font-size: 11px; color: var(--muted);
    letter-spacing: .04em; text-transform: uppercase;
}
.ledger .row + .row { border-top: 1px solid var(--line); }
.ledger .row span:last-child { color: var(--text); }
.ledger.empty .file { color: var(--muted); font-weight: 300; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 9px; font-size: .86rem; font-weight: 500; padding: .62rem 1rem;
    background: transparent; color: var(--text);
    border: 1px solid var(--line-strong); transition: all .2s ease;
}
.stButton > button:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-soft); }
.stButton > button[kind="primary"] {
    background: var(--text); color: var(--bg); border: 1px solid var(--text);
}
.stButton > button[kind="primary"]:hover {
    background: var(--accent); border-color: var(--accent); color: var(--bg);
}

/* ── Uploader ── */
[data-testid="stFileUploaderDropzone"], [data-testid="stFileUploader"] section {
    background: var(--bg); border: 1px dashed var(--line-strong); border-radius: 10px;
    transition: border-color .2s ease;
}
[data-testid="stFileUploaderDropzone"]:hover, [data-testid="stFileUploader"] section:hover {
    border-color: var(--accent);
}
[data-testid="stFileUploader"] small, [data-testid="stFileUploader"] span { color: var(--muted); }
[data-testid="stFileUploader"] button { font-size: .78rem; padding: .35rem .8rem; }

/* ── Conversation ── */
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatarCustom"] { display: none !important; }

[data-testid="stChatMessage"] {
    background: transparent; border: none; border-radius: 0;
    border-top: 1px solid var(--line);
    padding: 1.9rem 0 1.5rem; margin: 0; gap: 0;
    animation: rise .5s cubic-bezier(.2,.7,.2,1) both;
}
.role {
    font-family: var(--mono); font-size: 10.5px; letter-spacing: .16em;
    text-transform: uppercase; color: var(--faint); margin-bottom: .75rem;
}
.role.ai { color: var(--accent); }

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p {
    font-family: var(--serif) !important; font-size: 1.75rem; line-height: 1.22;
    letter-spacing: -0.01em; color: var(--text);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) li {
    font-size: .98rem; line-height: 1.78; color: #d8d3ca; font-weight: 300;
}
[data-testid="stChatMessage"] strong { color: var(--text); font-weight: 500; }
[data-testid="stChatMessage"] h1, [data-testid="stChatMessage"] h2, [data-testid="stChatMessage"] h3 {
    font-family: var(--serif) !important; font-weight: 400; letter-spacing: -0.01em;
}
[data-testid="stChatMessage"] code {
    font-family: var(--mono) !important; font-size: .82em;
    background: var(--surface-2); border: 1px solid var(--line);
    padding: 2px 6px; border-radius: 5px; color: var(--accent);
}
[data-testid="stChatMessage"] pre { background: var(--surface) !important; border: 1px solid var(--line); border-radius: 10px; }
.meta {
    font-family: var(--mono); font-size: 10.5px; letter-spacing: .08em;
    color: var(--faint); margin-top: .9rem; text-transform: uppercase;
}

/* ── Composer ── */
[data-testid="stBottom"] > div { background: linear-gradient(to top, var(--bg) 60%, transparent); }
[data-testid="stChatInput"] {
    background: var(--surface); border: 1px solid var(--line-strong);
    border-radius: 14px; transition: all .25s ease;
    box-shadow: 0 24px 60px rgba(0,0,0,.55);
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent); box-shadow: 0 24px 60px rgba(0,0,0,.55), 0 0 0 4px var(--accent-soft);
}
[data-testid="stChatInput"] textarea { color: var(--text); font-size: .98rem; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--faint); }
[data-testid="stChatInput"] button { color: var(--accent); }

/* Compact header once chatting */
.docbar { padding: 1.6rem 0 1.2rem; }
.docbar .eyebrow { margin: 0 0 .5rem; }
.docbar .title { font-family: var(--serif); font-size: 2.1rem; letter-spacing: -0.015em; line-height: 1.1; }

[data-testid="stAlert"] { border-radius: 10px; border: 1px solid var(--line); background: var(--surface); }
[data-testid="stSpinner"] { color: var(--muted); }
hr { border-color: var(--line) !important; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: var(--line-strong); border-radius: 8px; }
::selection { background: var(--accent); color: var(--bg); }

@keyframes rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }

@media (max-width: 720px) {
    .principles { grid-template-columns: 1fr; }
    .principle + .principle { border-left: none; padding-left: 0; border-top: 1px solid var(--line); margin-top: 1.1rem; }
    .hero { padding-top: 3rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ───────────────────────── State ─────────────────────────
for key, default in {
    "messages": [],
    "active_document": None,
    "chunks": None,
    "pending": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def api_online() -> bool:
    try:
        requests.get(f"{API_URL}/docs", timeout=1.5)
        return True
    except requests.RequestException:
        return False


online = api_online()
doc_name = st.session_state.active_document
esc_doc = html.escape(doc_name) if doc_name else None

# ───────────────────────── Sidebar ─────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="side-brand">Lumen<i>.</i></div>'
        '<div class="side-tag">Private document intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec"><b>01</b> Source</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a PDF", type=["pdf"], label_visibility="collapsed"
    )

    if st.button("Index document", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.warning("Select a PDF first.")
        else:
            with st.spinner("Reading, chunking and indexing…"):
                try:
                    response = requests.post(
                        f"{API_URL}/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf",
                            )
                        },
                        timeout=600,
                    )
                    response.raise_for_status()
                    data = response.json()

                    st.session_state.active_document = data["filename"]
                    st.session_state.chunks = data.get("chunks")
                    st.session_state.messages = []
                    st.toast(data["message"])
                    st.rerun()
                except requests.RequestException as e:
                    st.error(f"Upload failed: {e}")

    st.markdown('<div class="sec"><b>02</b> Document</div>', unsafe_allow_html=True)
    n_q = sum(1 for m in st.session_state.messages if m["role"] == "user")
    chunks = st.session_state.chunks
    if doc_name:
        st.markdown(
            f"""
            <div class="ledger">
                <div class="file">{esc_doc}</div>
                <div class="row"><span>Chunks</span><span>{chunks if chunks is not None else "—"}</span></div>
                <div class="row"><span>Questions</span><span>{n_q:02d}</span></div>
                <div class="row"><span>Status</span><span>Indexed</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="ledger empty">
                <div class="file">No document loaded</div>
                <div class="row"><span>Questions</span><span>{n_q:02d}</span></div>
                <div class="row"><span>Index</span><span>Default</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sec"><b>03</b> Session</div>', unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ───────────────────────── Top bar ─────────────────────────
status_cls = "on" if online else "off"
status_txt = "Engine online" if online else "Engine offline"
st.markdown(
    f"""
    <div class="topbar">
        <div class="wordmark">Lumen<i>.</i></div>
        <div class="status"><span class="dot {status_cls}"></span>{status_txt}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ───────────────────────── Hero / doc header ─────────────────────────
SUGGESTIONS = [
    "Summarize this document in five key points",
    "What are the most important takeaways?",
    "List the key dates, names and figures",
]

if not st.session_state.messages:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Hybrid retrieval · Runs locally</div>
            <h1>Your documents,<br><i>answered.</i></h1>
            <p>Upload a PDF and ask in plain language. Every answer is drawn from
            your document, processed entirely on your own machine.</p>
        </div>
        <div class="principles">
            <div class="principle"><div class="n">01</div><div class="t">Private by design</div>
                <div class="d">Powered by Ollama on your hardware. Nothing is sent to the cloud.</div></div>
            <div class="principle"><div class="n">02</div><div class="t">Hybrid search</div>
                <div class="d">Semantic and keyword retrieval combined for precise context.</div></div>
            <div class="principle"><div class="n">03</div><div class="t">Grounded answers</div>
                <div class="d">Responses stay anchored to what your document actually says.</div></div>
        </div>
        <div class="label">Begin with</div>
        """,
        unsafe_allow_html=True,
    )
    for i, text in enumerate(SUGGESTIONS):
        if st.button(text, key=f"sug_{i}", use_container_width=True):
            st.session_state.pending = text
            st.rerun()
else:
    st.markdown(
        f"""
        <div class="docbar">
            <div class="eyebrow">Conversation</div>
            <div class="title">{esc_doc or "Default document"}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ───────────────────────── History ─────────────────────────
for message in st.session_state.messages:
    is_user = message["role"] == "user"
    with st.chat_message(message["role"]):
        st.markdown(
            f'<div class="role {"" if is_user else "ai"}">{"You" if is_user else "Lumen"}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(message["content"])
        if message.get("elapsed"):
            st.markdown(
                f'<div class="meta">Answered in {message["elapsed"]:.1f}s</div>',
                unsafe_allow_html=True,
            )

# ───────────────────────── Chat ─────────────────────────
question = st.chat_input("Ask anything about your document…")
if st.session_state.pending:
    question = st.session_state.pending
    st.session_state.pending = None

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown('<div class="role">You</div>', unsafe_allow_html=True)
        st.markdown(question)

    with st.chat_message("assistant"):
        st.markdown('<div class="role ai">Lumen</div>', unsafe_allow_html=True)
        with st.spinner("Consulting your document…"):
            start = time.time()
            try:
                response = requests.post(
                    f"{API_URL}/ask", json={"question": question}, timeout=300
                )
                response.raise_for_status()
                answer = response.json()["answer"]
                elapsed = time.time() - start

                st.markdown(answer)
                st.markdown(
                    f'<div class="meta">Answered in {elapsed:.1f}s</div>',
                    unsafe_allow_html=True,
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "elapsed": elapsed}
                )
            except requests.RequestException as e:
                error_message = f"Couldn't reach the API: {e}"
                st.error(error_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message}
                )
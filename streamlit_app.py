
import streamlit as st
from ollama import chat
from pypdf import PdfReader
from duckduckgo_search import DDGS
import speech_recognition as sr
import json
import os

def web_search(query):

    results = []

    with DDGS() as ddgs:

        for r in ddgs.text(
            query,
            max_results=5
        ):
            results.append(
                f"{r['title']}\n{r['body']}"
            )

    return "\n\n".join(results)

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="Chiranjeevi AI",
    layout="wide"
)

# ----------------------------
# CREATE FOLDERS
# ----------------------------

os.makedirs("data/chats", exist_ok=True)
os.makedirs("uploads", exist_ok=True)


# ----------------------------
# LOAD MEMORY
# ----------------------------

with open("memory.json", "r") as f:
    memory = json.load(f)

project_names = ", ".join(
    [project["name"] for project in memory["projects"]]
)

system_prompt = f"""
You are Chiranjeevi's personal AI assistant.

Name: {memory['name']}
Age: {memory['age']}
College: {memory['college']}
Branch: {memory['branch']}
Year: {memory['year']}
Location: {memory['location']}
Profession: {memory['profession']}

Skills:
{', '.join(memory['skills'])}

Interests:
{', '.join(memory['interests'])}

Currently Learning:
{', '.join(memory['current_learning'])}

Career Goals:
{', '.join(memory['career_goals'])}

Projects:
{project_names}

You are Chiranjeevi's AI assistant.

Use the information only as background knowledge.

Do not pretend to be Chiranjeevi.

Do not say "I study at SRM AP" or
"I am Chiranjeevi".

Instead say:
"Chiranjeevi studies at SRM AP."

Answer as an assistant helping Chiranjeevi.

Keep answers concise and practical.
"""

# ----------------------------
# SESSION
# ----------------------------
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3.2:3b"

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "1.json"

if "messages" not in st.session_state:
    st.session_state.messages = []
chat_path = f"data/chats/{st.session_state.current_chat}"
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "voice_prompt" not in st.session_state:
    st.session_state.voice_prompt = ""


if os.path.exists(chat_path):

    try:

        with open(chat_path, "r") as f:

            chat_data = json.load(f)

        if len(st.session_state.messages) == 0:

            st.session_state.messages = chat_data.get(
                "messages",
                []
            )

    except:
        pass
# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.title("Chiranjeevi AI")

    # New Chat

    if st.button("➕ New Chat"):

        chat_files = os.listdir("data/chats")

        new_id = len(chat_files) + 1

        with open(
            f"data/chats/{new_id}.json",
            "w"
        ) as f:

            json.dump(
                {
                    "title": "New Chat",
                    "messages": []
                },
                f,
                indent=4
            )

        st.session_state.current_chat = f"{new_id}.json"
        st.session_state.messages = []

        st.rerun()

    # AI Tools

    st.subheader("AI Tools")

    st.link_button(
        "ChatGPT",
        "https://chatgpt.com"
    )

    st.link_button(
        "Claude",
        "https://claude.ai"
    )

    st.link_button(
        "Gemini",
        "https://gemini.google.com"
    )
    st.divider()

    st.subheader("Model")

    st.session_state.selected_model = st.selectbox(
    "Choose Model",
    [
        "llama3.2:3b",
        "phi3",
        "qwen3:4b"
    ]
)
    st.divider()

    web_mode = st.checkbox(
    "🌐 Web Search"
)

    # Search Chats

    search_chat = st.text_input(
        "🔍 Search Chats",
        key="search_chat"
    )

    # Chats

    st.subheader("Chats")

    chat_files = sorted(
        os.listdir("data/chats")
    )
    chat_files = sorted(
        os.listdir("data/chats")
    )

    for chat_file in chat_files:

        try:

            with open(
                f"data/chats/{chat_file}",
                "r"
            ) as f:

                chat_data = json.load(f)

            title = chat_data.get(
                "title",
                "New Chat"
            )

            if search_chat:

                if search_chat.lower() not in title.lower():
                    continue

            if st.button(
                f"💬 {title}",
                key=chat_file,
                use_container_width=True
            ):

                st.session_state.current_chat = chat_file

                st.session_state.messages = chat_data.get(
                    "messages",
                    []
                )

                st.rerun()

        except:
            pass
# ----------------------------
# MAIN AREA
# ----------------------------
st.title("Chiranjeevi AI")

# Show previous messages

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# File Upload

uploaded_file = st.file_uploader(
    "",
    type=["pdf", "png", "jpg", "jpeg", "txt", "docx"],
    label_visibility="collapsed"
)
pdf_text = ""

if uploaded_file:

    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    st.markdown(
        f"""
        <div style="
        padding:10px;
        border-radius:10px;
        border:1px solid #555;
        width:300px;">
        📄 {uploaded_file.name}
        </div>
        """,
        unsafe_allow_html=True
    )

    if uploaded_file.name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pdf_text += text + "\n"
    if pdf_text:
        st.session_state.pdf_text = pdf_text
# Voice Input

if st.button("🎤 Speak"):

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        st.info("Listening...")

        audio = recognizer.listen(source)

    try:

        voice_text = recognizer.recognize_google(audio)

        st.session_state.voice_prompt = voice_text

        st.success(
            f"You said: {voice_text}"
        )

    except:

        st.error(
            "Could not understand audio"
        )

# Chat Input

prompt = st.chat_input(
    "Message to Chiranjeevi AI",
    key="main_chat"
)

if not prompt and st.session_state.voice_prompt:

    prompt = st.session_state.voice_prompt

    st.session_state.voice_prompt = ""



user_message = prompt if prompt else ""

if st.session_state.pdf_text and prompt:

    user_message = f"""
PDF Content:

{st.session_state.pdf_text[:10000]}

Question:
{prompt}
"""

#response = chat(...)
if prompt:

    if web_mode:

        search_results = web_search(prompt)

        user_message = f"""
Web Search Results:

{search_results}

User Question:
{prompt}
"""

    with st.chat_message("user"):
        st.markdown(prompt)

    response = chat(
        model=st.session_state.selected_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            }
        ] + st.session_state.messages + [
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    answer = response["message"]["content"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # ----------------------------
    # SAVE CHAT
    # ----------------------------

    chat_file = f"data/chats/{st.session_state.current_chat}"

    try:

        with open(chat_file, "r") as f:
            chat_data = json.load(f)

    except:

        chat_data = {
            "title": "New Chat",
            "messages": []
        }

    chat_data["messages"] = st.session_state.messages

    if chat_data["title"] == "New Chat":
        chat_data["title"] = prompt[:40]

    with open(chat_file, "w") as f:
        json.dump(chat_data, f, indent=4)

    with st.chat_message("assistant"):
        st.markdown(answer)
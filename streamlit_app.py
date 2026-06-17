import streamlit as st
from groq import Groq
from pypdf import PdfReader
from duckduckgo_search import DDGS
import speech_recognition as sr
import json
import os

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def web_search(query):

    try:

        results = []

        with DDGS() as ddgs:

            if any(word in query.lower() for word in
                   ["latest", "today", "news", "breaking"]):

                data = ddgs.news(
                    query,
                    max_results=10
                )

            else:

                data = ddgs.text(
                    query,
                    max_results=5
                )

            for r in data:

                results.append(
                    f"{r['title']}\n{r['body']}"
                )

        if not results:
            return "No search results found."

        return "\n\n".join(results)

    except Exception as e:

        return f"SEARCH ERROR: {str(e)}"

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="Chiranjeevi AI",
    layout="wide"
)
st.markdown("""
<style>

/* Sidebar */
section[data-testid="stSidebar"]{
    border-right:1px solid rgba(128,128,128,0.2);
}

/* Buttons */
.stButton > button{
    width:100%;
    border-radius:12px;
    height:48px;
    border:1px solid #ddd;
}



.stTextInput input{
    border-radius:12px;
}

.stSelectbox div[data-baseweb="select"]{
    border-radius:12px;
}

/* Hide footer */
footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

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

You are Chiranjeevi AI.

Use the profile information only when the user's question
is specifically about Chiranjeevi, his studies, projects,
skills, goals, memories, or personal information.

For normal conversations, behave like a general AI assistant.

Do not mention Chiranjeevi unless it is relevant to the question.

Keep answers concise, helpful, and practical.

If the user asks "Who are you?", "What are you?" or
"Tell me about yourself",

ALWAYS reply exactly:

" I'm  personal assistant of Chiranjeevi.
I can help with coding, studies, projects, AI, productivity, and general questions."

Do not say:
- "I'm an AI language model"
- "I don't have a personal identity"
- "I'm just an AI assistant"

If Web Search Results are provided,
use them as the primary source of information.
Prefer search results over old model knowledge.
When web search results are provided:

- Use only relevant search results.
- Ignore unrelated search results.
- Prefer recent information from search results.
- If results are unrelated, clearly say so."""
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
if "show_tools" not in st.session_state:
    st.session_state.show_tools = False
if "show_ai_tools" not in st.session_state:
    st.session_state.show_ai_tools = False
if "web_mode" not in st.session_state:
    st.session_state.web_mode = False
uploaded_file = None
# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.markdown("""
<h2 style="
margin-left:10px;
font-weight:700;
">
Chiranjeevi AI
</h2>
""", unsafe_allow_html=True)

 
    st.caption("Personal AI Assistant")
    # New Chat

    if st.button("+ New Chat"):

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


    # Tools

    if st.button("Add Files&More"):

        st.session_state.show_tools = not st.session_state.get(
            "show_tools",
            False
        )

    if st.session_state.get("show_tools"):

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file is not None:

            try:

                pdf = PdfReader(uploaded_file)

                text = ""

                for page in pdf.pages:
                    text += page.extract_text() or ""

                st.session_state.pdf_text = text

                st.success("PDF Loaded Successfully")

            except Exception as e:

                st.error(f"Error reading PDF: {e}")

    st.session_state.web_mode = st.checkbox(
            "Web Search"
        )

   # st.button(
   #     "Voice Input",
   #     key="voice_tool",
    #    disabled=True
    #)
       # if st.button(
       #     "Voice Input",
       #     key="voice_tool"
      #    try:
#                r = sr.Recognizer()

        ##            st.info("Listening...")

         #           audio = r.listen(
        #                source,
                #        timeout=5
 #                   )
#
               # text = r.recognize_google(st.audio)

              #  st.session_state.voice_prompt = text

               # st.success(
              ##      f"You said: {text}"
#                )

 #               st.rerun()

  #          except Exception as e:

   #             st.error(
    #                f"Voice Error: {e}"
     #           )
    #ai tools
    if st.button("AI Tools", key="ai_tools_btn"):
        st.session_state.show_ai_tools = \
        not st.session_state.get(
            "show_ai_tools",
            False
        )
        if st.session_state.get("show_ai_tools"):
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
    #models
    st.divider()

    st.caption("Model")

    st.session_state.selected_model = st.selectbox(
    "Choose Model",
    [
        "llama3.2:3b",
        "phi3",
        "qwen3:4b"
    ]
)
    

    # Search Chats
    search_chat = st.text_input(
    "Search Chats",
    key="search_chat"
)
        # Chats
    st.caption("Recent Chats")

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

            col1, col2 = st.columns([5, 1])

            with col1:

                if st.button(
                    title,
                    key=f"open_{chat_file}",
                    use_container_width=True
                ):

                    st.session_state.current_chat = chat_file

                    st.session_state.messages = chat_data.get(
                        "messages",
                        []
                    )

                    st.rerun()

            with col2:

                with st.popover("⋮"):

                                if st.button(
                                    "Delete",
                                    key=f"delete_{chat_file}"
                                ):

                                    os.remove(
                                        f"data/chats/{chat_file}"
                                    )
                                    st.rerun()
        except:
            pass    
# ----------------------------
# MAIN AREA
# ----------------------------
st.markdown("""
<div style="
text-align:center;
margin-top:60px;
">
<h1>Chiranjeevi AI</h1>
<p>How can I help you today?</p>
</div>
""", unsafe_allow_html=True)
# Show previous messages

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input

prompt = st.chat_input(
    "Ask me anything...",
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

    if st.session_state.get("web_mode", False):

        search_results = web_search(prompt+"ipl, cricket, news, latest, today, breaking,war, india, pakistan, australia, england, south africa, new zealand, sri lanka, west indies, bangladesh, afghanistan, odi, t20i, test match,world news, sports news, cricket news, latest news, breaking news, current affairs, trending news, top stories, headlines, updates, live scores, match results, sports updates, cricket updates, sports headlines, cricket headlines,latest information, recent news, news articles, news updates, news headlines, news stories, news reports, news coverage, news analysis, news commentary, news insights, news opinions, news perspectives, news reviews, news summaries, news digests, news briefs, news highlights, news recaps, news roundups, news overviews, news snapshots, news bulletins, news alerts, news notifications")
        st.write(search_results)

        user_message += f"""

Use the web search results below.
Carefully analyze whether the search results
are relevant to the user's question.

If the search results are irrelevant,
answer using your own knowledge.

Web Search Results:

{search_results}

User Question:
{prompt}
"""

    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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

    answer = response.choices[0].message.content

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

import json
import streamlit as st

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage

from newsupdate import get_city_news
from weatherTool import get_weather

load_dotenv()

# -------------------- Page Configuration --------------------

st.set_page_config(
    page_title="City Intelligence System",
    page_icon="🌍",
    layout="wide"
)

# -------------------- Styling --------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #818cf8;
        margin-bottom: 0;
    }

    .subtitle {
        color: #a1a1aa;
        margin-top: 5px;
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }

    div.stButton > button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- Tools and Model --------------------

tools = {
    "get_weather": get_weather,
    "get_city_news": get_city_news,
}

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

llm_tool = llm.bind_tools(list(tools.values()))

# -------------------- Session State --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_tools" not in st.session_state:
    st.session_state.pending_tools = []

if "tool_results" not in st.session_state:
    st.session_state.tool_results = []


# -------------------- Helper Functions --------------------

def get_response_text(content):
    """Extract readable text from a LangChain response."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict) and item.get("text"):
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)

        return "\n".join(parts)

    return str(content)


def advance_agent():
    """Run the model until it finishes or requests tool approval."""

    while True:
        result = llm_tool.invoke(st.session_state.messages)
        st.session_state.messages.append(result)

        if result.tool_calls:
            st.session_state.pending_tools = [
                {
                    "id": call["id"],
                    "name": call["name"],
                    "args": call["args"],
                    "status": "pending",
                }
                for call in result.tool_calls
            ]
            return

        answer = get_response_text(result.content)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
        })

        return


def resolve_tool(tool_id, approved):
    """Approve or deny a pending tool call."""

    pending = next(
        (
            item for item in st.session_state.pending_tools
            if item["id"] == tool_id
            and item["status"] == "pending"
        ),
        None,
    )

    if pending is None:
        return

    if approved:
        tool = tools.get(pending["name"])

        if tool is None:
            tool_result = {"error": "Unknown tool."}
        else:
            try:
                tool_result = tool.invoke(pending["args"])
            except Exception as exc:
                tool_result = {"error": str(exc)}

        pending["status"] = "approved"

    else:
        tool_result = "Tool call denied by the user."
        pending["status"] = "denied"

    if isinstance(tool_result, (dict, list)):
        tool_content = json.dumps(
            tool_result,
            ensure_ascii=False,
            default=str,
        )
    else:
        tool_content = str(tool_result)

    st.session_state.messages.append(
        ToolMessage(
            content=tool_content,
            tool_call_id=tool_id,
        )
    )

    st.session_state.tool_results.append({
        "name": pending["name"],
        "status": pending["status"],
        "content": tool_content,
    })

    # Continue only after all requested tool calls are resolved.
    if all(
        item["status"] != "pending"
        for item in st.session_state.pending_tools
    ):
        st.session_state.pending_tools = []
        advance_agent()


# -------------------- Sidebar --------------------

with st.sidebar:
    st.title("🌍 City Intelligence")
    st.caption("Your AI-powered city assistant")

    st.divider()

    st.markdown("### Available tools")
    st.markdown("- 🌦️ Current weather")
    st.markdown("- 📰 Latest city news")

    st.info(
        "The AI must receive your approval "
        "before executing a tool."
    )

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.pending_tools = []
        st.session_state.tool_results = []
        st.rerun()


# -------------------- Main Interface --------------------

st.markdown(
    '<p class="main-title">City Intelligence System</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="subtitle">'
    'Ask about city weather, local news, and more.'
    '</p>',
    unsafe_allow_html=True,
)

# Display conversation history
for index, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display tool execution results
if st.session_state.tool_results:
    with st.expander("🔧 Tool activity and results"):
        for item in st.session_state.tool_results:
            st.markdown(
                f'**{item["name"]} — {item["status"].title()}**'
            )

            try:
                parsed = json.loads(item["content"])

                if isinstance(parsed, dict):
                    if "news" in parsed:
                        st.markdown(
                            f'**City:** {parsed.get("city", "Unknown")}'
                        )

                        for article in parsed["news"]:
                            st.markdown(
                                f'### {article.get("title") or "Untitled"}'
                            )

                            if article.get("published_date"):
                                st.caption(article["published_date"])

                            if article.get("url"):
                                st.markdown(
                                    f'[Read article]({article["url"]})'
                                )

                            if article.get("content"):
                                st.write(article["content"])

                    elif "temperature_c" in parsed:
                        st.markdown(
                            f'### 🌦️ {parsed.get("city", "Weather")}'
                        )

                        col1, col2, col3 = st.columns(3)

                        col1.metric(
                            "Temperature",
                            f'{parsed["temperature_c"]} °C',
                        )
                        col2.metric(
                            "Feels like",
                            f'{parsed["feels_like_c"]} °C',
                        )
                        col3.metric(
                            "Humidity",
                            f'{parsed["humidity_percent"]}%',
                        )

                        st.write(
                            f'**Condition:** {parsed.get("condition", "N/A")}'
                        )
                        st.write(
                            f'**Wind speed:** '
                            f'{parsed.get("wind_speed_m_s", "N/A")} m/s'
                        )
                        st.write(
                            f'**Country:** {parsed.get("country", "N/A")}'
                        )

                    else:
                        st.json(parsed)

                elif isinstance(parsed, list):
                    st.json(parsed)

                else:
                    st.write(parsed)

            except (json.JSONDecodeError, TypeError):
                st.write(item["content"])

            st.divider()

# Human-in-the-loop approval interface
if st.session_state.pending_tools:
    st.divider()
    st.subheader("🔐 Tool approval required")
    st.write(
        "The assistant wants to execute the following tool(s). "
        "Review the arguments before approving."
    )

    for index, item in enumerate(st.session_state.pending_tools):
        if item["status"] != "pending":
            continue

        with st.container(border=True):
            st.markdown(f"**Tool:** `{item['name']}`")
            st.json(item["args"])

            col1, col2 = st.columns(2)

            with col1:
                st.button(
                    "✅ Approve",
                    key=f"approve_{item['id']}",
                    use_container_width=True,
                    on_click=resolve_tool,
                    args=(item["id"], True),
                )

            with col2:
                st.button(
                    "❌ Deny",
                    key=f"deny_{item['id']}",
                    use_container_width=True,
                    on_click=resolve_tool,
                    args=(item["id"], False),
                )

# Chat input
user_input = st.chat_input(
    "Ask about weather or news in a city...",
    disabled=bool(st.session_state.pending_tools),
)

if user_input:
    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
    })

    try:
        advance_agent()
    except Exception as exc:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"An error occurred: {exc}",
        })

    st.rerun()

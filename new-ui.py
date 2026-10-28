
import streamlit as st
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="centered"
)

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = ""

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# UI
st.title("📰 AI News Summarizer")
st.write("Search for the latest AI news and get a clear summary.")

query = st.text_input(
    "Enter your news topic",
    placeholder="e.g. Latest AI news of 2026"
)

max_results = st.slider(
    "Number of search results",
    min_value=1,
    max_value=10,
    value=5
)

if st.button("🔍 Search & Summarize", type="primary"):
    if not query.strip():
        st.warning("Please enter a news topic.")
    else:
        try:
            with st.spinner("Searching news and generating summary..."):

                # Search tool
                search_tool = TavilySearchResults(
                    max_results=max_results
                )

                news = search_tool.invoke(query)

                if not news:
                    st.warning("No news results found. Try another topic.")
                    st.stop()

                # Gemini model
                llm = ChatGoogleGenerativeAI(
                    model="gemini-3.5-flash-lite",
                    temperature=0.3
                )

                # Prompt template
                prompt = ChatPromptTemplate.from_template("""
You are a helpful AI news assistant.

Summarize the following search results into clear bullet points.
For each important story, include:
- A short headline
- The key information
- Why it matters
- The source URL, when available

Use only the information provided in the search results.
Do not invent facts.

User's topic: {query}

Search results:
{news}
""")

                # LCEL chain
                chain = prompt | llm | StrOutputParser()

                result = chain.invoke({
                    "query": query,
                    "news": str(news)
                })

                st.session_state.summary = result
                st.session_state.last_query = query

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Display summary
if st.session_state.summary:
    st.divider()
    st.subheader("📌 News Summary")
    st.caption(f"Topic: {st.session_state.last_query}")
    st.markdown(st.session_state.summary)

    st.download_button(
        label="📥 Download Summary",
        data=st.session_state.summary,
        file_name="ai_news_summary.txt",
        mime="text/plain"
    )

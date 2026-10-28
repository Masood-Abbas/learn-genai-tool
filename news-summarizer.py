from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
search_tool=TavilySearchResults(max_result=5)

llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompt=ChatPromptTemplate.from_template("""
you are helpful assistant 
summarize the following news into clear bullet points
{news}
""")
chain=prompt|llm|StrOutputParser()
result_news=search_tool.run("latest Ai news of 2026")
result=chain.invoke({"news":result_news})
print(result)

from ast import parse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt=ChatPromptTemplate.from_template("Explain {topic} in simple words")

model=ChatGoogleGenerativeAI(model= "gemini-3.5-flash-lite")

parse= StrOutputParser()

chain= prompt|model|parse

result=chain.invoke("explain the javascript")

print(result)
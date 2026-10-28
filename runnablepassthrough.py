
from click import parser
from ast import parse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnablePassthrough

load_dotenv()

code_prompt=ChatPromptTemplate.from_messages([
    ("system","You are  code generator"),(
        "human","{topic}"
    )
])

explainPrompt=ChatPromptTemplate.from_messages([
    ("system","You are  a helpful assistant who explains code in simple terms"),(
        "human","Explain the following code in simple words :\n{code}"
    )
])

model=ChatGoogleGenerativeAI(model= "gemini-3.5-flash-lite")

parse= StrOutputParser()

seq=code_prompt| model |parse
seq2=RunnableParallel({
    "code": RunnablePassthrough(),
    "explanation":explainPrompt | model |parse
})

chain=seq | seq2
result= chain.invoke({"topic":"write a  code of palidreome in python"})

print(result['code'])
print(result['explanation'])
 
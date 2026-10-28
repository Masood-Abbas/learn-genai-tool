
from ast import parse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableLambda

load_dotenv()

shortprompt=ChatPromptTemplate.from_template("Explain {topic} in 1-2 lines")

longprompt=ChatPromptTemplate.from_template("Explain {topic} in detail")

model=ChatGoogleGenerativeAI(model= "gemini-3.5-flash-lite")

parse= StrOutputParser()

chain=RunnableParallel({
    "short":RunnableLambda(lambda x:x['short']) |shortprompt|model|parse,
    "detail":RunnableLambda(lambda x:x['details']) |longprompt|model|parse
})

result=chain.invoke(
    {
        "short":{"topic":"JavaScript"},
        "details":{"topic":"python "},
        }
)
print(result['short'])
print("detil data \n")
print(result['detail'])

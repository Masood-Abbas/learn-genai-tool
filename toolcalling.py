
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from rich import print
from langchain_core.messages import HumanMessage

load_dotenv()

@tool
def get_text_length(text: str) -> int:
    """Return the number of characters in a given text."""
    return len(text)

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
llm_tool = llm.bind_tools([get_text_length])


messages=[]
query=HumanMessage("Return the number of character in the given text :'hellow world'")

messages.append(query)
result=llm_tool.invoke(messages)
messages.append(result)

tools={
    "get_text_length":get_text_length
}
if result.tool_calls:
    tool_name=result.tool_calls[0]["name"]
    tool_messages=tools[tool_name].invoke(result.tool_calls[0])
    messages.append(tool_messages)
result=llm_tool.invoke(messages)
print(result.content[0]["text"])











 









# result = llm_tool.invoke(
#     'Count the characters in "hellow are you" using get_text_length.'
# )
# if result.tool_calls:
#     tool_call = result.tool_calls[0]
#     tool_name= tool_call["name"]
#     tool_args = tool_call["args"]

#     # Execute the tool with its arguments
#     tool_result = get_text_length.invoke(tool_args)

#     print("Tool result:", tool_result)

#     # Ask Gemini to explain the result
#     final_res = llm.invoke(
#         f'The text "hellow are you" has {tool_result} characters. '
#         'Give a short answer.'
#     )

#     print("Final response:", final_res.content[0]["text"])
# else:
#     print("Model response:", result.content)

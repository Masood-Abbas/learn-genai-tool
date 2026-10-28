
from newsupdate import get_city_news
from weatherTool import get_weather
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
from rich import print
import json

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

tools = {
    "get_weather": get_weather,
    "get_city_news": get_city_news,
}

llm_tool = llm.bind_tools(list(tools.values()))

messages = []

print("City Intelligence System")
print("Type 'exit' to quit")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        break

    if not user_input:
        continue

    messages.append(HumanMessage(content=user_input))

    while True:
        result = llm_tool.invoke(messages)
        messages.append(result)

        # Check whether the model requested any tools
        if result.tool_calls:
            for tool_call in result.tool_calls:
                tool_name = tool_call["name"]

                # Human-in-the-loop approval
                confirm = input(
                    f"Agent wants to call {tool_name}. Approve (yes/no)? "
                ).strip().lower()

                if confirm not in ("yes", "y"):
                    tool_result = "Tool call denied by the user."
                    print(f"[yellow]Denied: {tool_name}[/yellow]")

                else:
                    # Execute the tool using its arguments
                    tool_result = tools[tool_name].invoke(
                        tool_call["args"]
                    )

                if isinstance(tool_result, (dict, list)):
                    tool_content = json.dumps(
                        tool_result, ensure_ascii=False
                    )
                else:
                    tool_content = str(tool_result)

                messages.append(
                    ToolMessage(
                        content=tool_content,
                        tool_call_id=tool_call["id"],
                    )
                )

            continue

        print(f"[green]Assistant:[/green] {result.content[0]["text"]}")
        break

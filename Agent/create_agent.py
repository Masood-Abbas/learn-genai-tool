from newsupdate import get_city_news
from weatherTool import get_weather
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from rich import print
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)
@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call."""

    tool_name = request.tool_call["name"]
    tool_call_id = request.tool_call["id"]

    confirm = input(
        f"Agent wants to call '{tool_name}'. Approve? (yes/no): "
    )

    if confirm.strip().lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=tool_call_id,
        )

    return handler(request)
agent = create_agent(
    model=llm,
    tools=[get_weather, get_city_news],
    middleware=[human_approval],
    system_prompt="""
    You are a helpful city intelligence assistant.

    TOOL CALLING RULES:
    - You have two tools: get_weather and get_city_news.
    - If the user asks about weather only, call get_weather.
    - If the user asks about news only, call get_city_news.
    - If the user asks for BOTH weather and news, you MUST call BOTH tools.
    - Do not skip either tool when both are requested.
    - Use the same city for both tools unless the user specifies otherwise.
    - Wait for the tool results before generating your final response.
    - Never invent data.

    WEATHER RESPONSE:
    Include all available fields:
    - City
    - Temperature in Celsius (temperature_c)
    - Feels-like temperature in Celsius (feels_like_c)
    - Humidity percentage (humidity_percent)
    - Weather condition (condition)

    NEWS RESPONSE:
    Display each article separately and include:
    - Title
    - URL
    - Content
    - Published Date

    GENERAL RULES:
    - If a requested field is missing, say "Not available".
    - Present results using clear headings and bullet points.
    - Keep weather and news in separate sections.
    - Include all available information returned by the tools.
    """
)

print("[bold cyan]City Intelligence System[/bold cyan]")
print("Type 'exit' to quit")

while True:
    user_input = input("\nYou: ")

    if user_input.lower().strip() == "exit":
        break

    try:
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": user_input}
            ]
        })

        final_message = result["messages"][-1].content[0]["text"]


        print(final_message)

    except Exception as e:
        print(f"[bold red]Error:[/bold red] {e}")

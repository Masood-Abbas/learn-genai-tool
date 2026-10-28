
import os
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()


@tool
def get_city_news(city: str) -> dict:
    """Search for recent news about a city.
    Args:
        city: City name, such as Lahore, Karachi, or Islamabad.
    """
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return {"error": "TAVILY_API_KEY is missing from .env"}

    try:
        client = TavilyClient(api_key=api_key)

        response = client.search(
            query=f"Latest news in {city}",
            topic="news",
            time_range="week",
            max_results=5
        )

        results = response.get("results", [])

        if not results:
            return {"city": city, "message": "No recent news found."}

        articles = []

        for item in results:
            articles.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content"),
                "published_date": item.get("published_date")
            })

        return {
            "city": city,
            "news": articles
        }

    except Exception as e:
        return {"error": f"News search failed: {str(e)}"}


import asyncio
import os
from tavily import TavilyClient
from dotenv import load_dotenv
from order_app.database import OrderDatabase
import time
import httpx

load_dotenv()
tavily_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=tavily_key)


async def web_search(query):
    result = await asyncio.to_thread(
        client.search,
        query=query,
        max_results=1,
    )
    return result


async def documentation_search(query):
    url = "https://openlibrary.org/search.json"

    params = {
        "q": query,
        "limit": 1,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=2.5)

    data = response.json()
    return data["docs"]


def get_database_orders():
    order_db = OrderDatabase("orders.db")
    return order_db.get_orders()


async def database_search():
    results = await asyncio.to_thread(get_database_orders)

    return results


async def run_source(source_name, coroutine, timeout=2.5):
    try:
        result = await asyncio.wait_for(coroutine, timeout=timeout)

        return {"source": source_name, "status": "success", "result": result}

    except asyncio.TimeoutError:
        return {
            "source": source_name,
            "status": "timeout",
            "error": f"{source_name} timed out",
        }

    except Exception as e:
        return {"source": source_name, "status": "error", "error": str(e)}


async def research(query):
    results = await asyncio.gather(
        run_source("web", web_search(query)),
        run_source("openlibrary", documentation_search(query)),
        run_source("database", database_search()),
    )

    return results


start_time = time.perf_counter()
result = asyncio.run(research("blender"))

print(result)
end_time = time.perf_counter()
print(f"Total: {end_time - start_time:.2f} seconds")

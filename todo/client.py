import asyncio
import contextlib
from collections.abc import AsyncIterator

from mcp import ClientSession
from mcp.client.sse import sse_client

from todo.config import Config


def server_url() -> str:
    return f"http://{Config.Server.HOST}:{Config.Server.PORT}{Config.Server.SSE_PATH}"


@contextlib.asynccontextmanager
async def connect_to_server(url: str = server_url()) -> AsyncIterator[ClientSession]:
    async with sse_client(server_url()) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session


async def main() -> None:
    async with connect_to_server() as session:
        tools = await session.list_tools()
        print(tools.tools)

        tool_result = await session.call_tool("list_tasks", arguments={"max_results": 2})
        print(tool_result.content)


if __name__ == "__main__":
    asyncio.run(main())

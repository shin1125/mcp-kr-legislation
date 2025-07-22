"""
FastMCP 서버 메인 엔트리포인트
""" 

import logging
import sys
import asyncio
from starlette.requests import Request
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Any, Literal, Optional
from fastmcp import FastMCP
from mcp_kr_legislation.config import MCPConfig, LegislationConfig, mcp_config, legislation_config
from mcp_kr_legislation.apis.client import LegislationClient
from mcp_kr_legislation.apis.legislation_api import LegislationAPI
from mcp_kr_legislation.registry.initialize_registry import initialize_registry
import importlib

# 로깅 설정
level_name = mcp_config.log_level.upper()
level = getattr(logging, level_name, logging.INFO)
logger = logging.getLogger("mcp-kr-legislation")
logging.basicConfig(
    level=level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)

@dataclass
class LegislationContext:
    client: Optional[LegislationClient] = None
    legislation_api: Any = None

    def __post_init__(self):
        if self.client is None:
            self.client = LegislationClient(config=legislation_config)
        if self.legislation_api is None:
            self.legislation_api = LegislationAPI(self.client)

    async def __aenter__(self):
        logger.info("🔁 LegislationContext entered (Claude requested tool execution)")
        return self

    async def __aexit__(self, *args):
        logger.info("🔁 LegislationContext exited")

legislation_client = LegislationClient(config=legislation_config)
legislation_context = LegislationContext(client=legislation_client, legislation_api=LegislationAPI(legislation_client))
ctx = legislation_context

@asynccontextmanager
async def legislation_lifespan(app: FastMCP):
    logger.info("Initializing Legislation FastMCP server...")
    try:
        logger.info(f"Server Name: {mcp_config.server_name}")
        logger.info(f"Host: {mcp_config.host}")
        logger.info(f"Port: {mcp_config.port}")
        logger.info(f"Log Level: {mcp_config.log_level}")
        client = LegislationClient(config=legislation_config)
        ctx = LegislationContext(client=client, legislation_api=LegislationAPI(client))
        logger.info("Legislation client and API modules initialized successfully.")
        await asyncio.sleep(0)  # async generator로 인식되도록 보장
        yield ctx
    except Exception as e:
        logger.error(f"Failed to initialize Legislation client: {e}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down Legislation FastMCP server...")

tool_registry = initialize_registry()
mcp = FastMCP(
    "KR Legislation MCP",
    instructions="Korean legislation information MCP server.",
    lifespan=legislation_lifespan,
)

for module_name in ["legislation_tools", "analysis_tools"]:
    importlib.import_module(f"mcp_kr_legislation.tools.{module_name}")

def main():
    logger.info("✅ Initializing Legislation FastMCP server...")
    transport = mcp_config.transport
    port = mcp_config.port
    if transport == "sse":
        asyncio.run(run_server(transport="sse", port=port))
    else:
        mcp.run()

async def run_server(
    transport: Literal["stdio", "sse"] = "stdio",
    port: int = 8001,
) -> None:
    if transport == "stdio":
        await mcp.run_stdio_async()
    elif transport == "sse":
        logger.info(f"Starting server with SSE transport on http://0.0.0.0:{port}")
        await mcp.run_sse_async(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main() 
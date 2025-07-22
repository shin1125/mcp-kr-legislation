"""
한국 법제처 OPEN API 125개 완전 통합 MCP 서버

지원하는 API 카테고리:
- 법령 (16개)
- 부가서비스 (10개)
- 행정규칙 (5개)  
- 자치법규 (4개)
- 판례관련 (8개)
- 위원회결정문 (30개)
- 조약 (2개)
- 별표서식 (4개)
- 학칙공단 (2개)
- 법령용어 (2개)
- 모바일 (15개)
- 맞춤형 (6개)
- 지식베이스 (6개)
- 기타 (1개)
- 중앙부처해석 (14개)
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Any, Literal, Optional
from fastmcp import FastMCP
from mcp_kr_legislation.config import MCPConfig, LegislationConfig, mcp_config, legislation_config
from mcp_kr_legislation.apis.client import LegislationClient
from mcp_kr_legislation.registry.initialize_registry import initialize_registry
import importlib

# 로깅 설정
level_name = mcp_config.log_level.upper()
level = getattr(logging, level_name, logging.INFO)
logger = logging.getLogger("mcp-kr-legislation")
logging.basicConfig(
    level=level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@dataclass
class LegislationContext:
    """법제처 API 통합 컨텍스트"""
    client: Optional[LegislationClient] = None
    
    def __post_init__(self):
        if self.client is None:
            self.client = LegislationClient(config=legislation_config)

    async def __aenter__(self):
        logger.info("🔁 LegislationContext entered (Claude requested tool execution)")
        return self

    async def __aexit__(self, *args):
        logger.info("🔁 LegislationContext exited")

# 전역 컨텍스트 생성
legislation_client = LegislationClient(config=legislation_config)
legislation_context = LegislationContext(client=legislation_client)
ctx = legislation_context

@asynccontextmanager
async def legislation_lifespan(app: FastMCP):
    """법제처 MCP 서버 라이프사이클 관리"""
    logger.info("Initializing Legislation FastMCP server...")
    try:
        logger.info(f"Server Name: {mcp_config.server_name}")
        logger.info(f"Host: {mcp_config.host}")
        logger.info(f"Port: {mcp_config.port}")
        logger.info(f"Log Level: {mcp_config.log_level}")
        
        client = LegislationClient(config=legislation_config)
        ctx = LegislationContext(client=client)
        logger.info("Legislation client initialized successfully.")
        logger.info("🚀 125개 법제처 OPEN API 지원 완료! (법령, 부가서비스, 행정규칙, 자치법규, 판례, 위원회결정문, 조약, 별표서식, 학칙공단, 법령용어, 모바일, 맞춤형, 지식베이스, 기타, 중앙부처해석 등 전체 카테고리 완벽 지원)")
        
        await asyncio.sleep(0)  # async generator로 인식되도록 보장
        yield ctx
    except Exception as e:
        logger.error(f"Failed to initialize Legislation client: {e}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down Legislation FastMCP server...")

# 도구 레지스트리 초기화
tool_registry = initialize_registry()

# FastMCP 인스턴스 생성
mcp = FastMCP(
    "KR Legislation MCP",
    instructions="Korean legislation information MCP server with 125 comprehensive tools covering all categories: laws, additional services, administrative rules, ordinances, precedents, committee decisions, treaties, forms, school regulations, legal terms, mobile services, custom services, knowledge base, miscellaneous, and ministry interpretations.",
    lifespan=legislation_lifespan,
)

# 도구 모듈 동적 로딩
for module_name in ["legislation_tools", "analysis_tools"]:
    try:
        importlib.import_module(f"mcp_kr_legislation.tools.{module_name}")
        logger.info(f"Loaded tool module: {module_name}")
    except ImportError as e:
        logger.warning(f"Failed to load tool module {module_name}: {e}")

def main():
    """메인 서버 실행 함수"""
    logger.info("✅ Initializing Legislation FastMCP server...")
    transport = mcp_config.transport
    port = mcp_config.port
    
    if transport == "sse":
        logger.info(f"🌐 Starting SSE server on port {port}")
        mcp.run(transport="sse", port=port)
    else:
        logger.info("📡 Starting STDIO server")
        mcp.run()

if __name__ == "__main__":
    main() 
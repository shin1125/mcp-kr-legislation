from fastmcp import FastMCP
from typing import Any, Dict

# mcp-kr-legislation 라이브러리
from mcp_kr_legislation.apis.client import LegislationClient
from mcp_kr_legislation.config import legislation_config

mcp = FastMCP("KR Legislation (FastMCP Cloud)")

def _client() -> LegislationClient:
    # 환경변수(LEGISLATION_API_KEY 등)는 Cloud에서 주입
    return LegislationClient(config=legislation_config)

@mcp.tool
def search_law(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    한국 법령을 키워드로 검색합니다.
    - query: 검색어(예: '개인정보보호법')
    - max_results: 최대 결과 수
    """
    c = _client()
    return c.search("law", {"query": query, "max": max_results})

@mcp.tool
def get_law(id_or_name: str) -> Dict[str, Any]:
    """
    법령ID 또는 이름으로 본문/메타 조회
    """
    c = _client()
    return c.search("law_detail", {"id_or_name": id_or_name})

"""
한국 법제처 OPEN API 마지막 2개 도구 추가

121개 완성을 위한 최종 도구들
"""

import logging
import json
import os
from typing import Optional, Union
from mcp.types import TextContent

from ..server import mcp
from .legislation_tools import _make_legislation_request, _format_search_results

logger = logging.getLogger(__name__)

# ===========================================
# 마지막 누락된 2개 API 도구
# ===========================================

@mcp.tool(name="search_administrative_rule_comparison", description="행정규칙 신구비교를 검색합니다. 행정규칙의 개정 전후 비교 정보를 제공합니다.")
def search_administrative_rule_comparison(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """행정규칙 신구비교 목록 조회 (admrulOldAndNewList)"""
    search_query = query or "개인정보보호"
    params = {"target": "admrulOldAndNew", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("admrulOldAndNew", params)
        result = _format_search_results(data, "admrulOldAndNew", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정규칙 신구비교 검색 중 오류: {str(e)}")

@mcp.tool(name="search_human_rights_committee", description="국가인권위원회 결정문을 검색합니다. 인권 관련 위원회 결정사항을 제공합니다.")
def search_human_rights_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """국가인권위원회 결정문 검색 (nhrck)"""
    search_query = query or "인권"
    params = {"target": "nhrck", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("nhrck", params)
        result = _format_search_results(data, "nhrck", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 국가인권위원회 결정문 검색 중 오류: {str(e)}")

logger.info("🎉 마지막 2개 API 도구 완성! 총 121개 전체 도구 로드 완료!") 
"""
한국 법제처 OPEN API - 행정규칙 및 자치법규 도구들

행정규칙, 자치법규(조례, 규칙) 관련 검색 및 조회 기능을 제공합니다.
"""

import logging
import json
import os
import requests
from urllib.parse import urlencode
from typing import Optional, Union
from mcp.types import TextContent

from ..server import mcp
from ..config import legislation_config

logger = logging.getLogger(__name__)

# 유틸리티 함수들 import
from .law_tools import (
    _make_legislation_request,
    _generate_api_url,
    _format_search_results
)

# ===========================================
# 행정규칙 도구들 (5개)
# ===========================================

@mcp.tool(name="search_administrative_rule", description="행정규칙을 검색합니다. 각 부처의 행정규칙과 예규를 제공합니다.")
def search_administrative_rule(query: Optional[str] = None, search: int = 2, display: int = 20, page: int = 1) -> TextContent:
    """행정규칙 검색"""
    if not query or not query.strip():
        return TextContent(type="text", text="❌ 검색어를 입력해주세요.")
    
    search_query = query.strip()
    params = {"target": "admrul", "query": search_query, "search": search, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("admrul", params)
        url = _generate_api_url("admrul", params)
        result = _format_search_results(data, "admrul", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정규칙 검색 중 오류: {str(e)}")

@mcp.tool(name="get_administrative_rule_detail", description="행정규칙 상세내용을 조회합니다. 특정 행정규칙의 본문을 제공합니다.")
def get_administrative_rule_detail(rule_id: Union[str, int]) -> TextContent:
    """행정규칙 본문 조회"""
    params = {"target": "admrul", "ID": str(rule_id)}
    try:
        data = _make_legislation_request("admrul", params)
        url = _generate_api_url("admrul", params)
        result = _format_search_results(data, "admrul", f"행정규칙ID:{rule_id}", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정규칙 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_administrative_rule_comparison", description="행정규칙 신구법 비교를 검색합니다. 행정규칙의 개정 전후 비교 정보를 제공합니다.")
def search_administrative_rule_comparison(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """행정규칙 신구법 비교 목록 조회"""
    if not query or not query.strip():
        return TextContent(type="text", text="❌ 검색어를 입력해주세요.")
    
    search_query = query.strip()
    params = {"target": "admrulOldAndNew", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("admrulOldAndNew", params)
        url = _generate_api_url("admrulOldAndNew", params)
        result = _format_search_results(data, "admrulOldAndNew", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정규칙 신구법 비교 검색 중 오류: {str(e)}")

@mcp.tool(name="get_administrative_rule_comparison_detail", description="행정규칙 신구법 비교 상세내용을 조회합니다. 특정 행정규칙의 신구법 비교 본문을 제공합니다.")
def get_administrative_rule_comparison_detail(comparison_id: Union[str, int]) -> TextContent:
    """행정규칙 신구법 비교 본문 조회"""
    params = {"target": "admrulOldAndNew", "ID": str(comparison_id)}
    try:
        data = _make_legislation_request("admrulOldAndNew", params)
        url = _generate_api_url("admrulOldAndNew", params)
        result = _format_search_results(data, "admrulOldAndNew", f"비교ID:{comparison_id}", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정규칙 신구법 비교 상세 조회 중 오류: {str(e)}")

# ===========================================
# 자치법규 도구들 (4개)
# ===========================================

@mcp.tool(name="search_local_ordinance", description="자치법규(조례, 규칙)를 검색합니다. 지방자치단체의 조례와 규칙을 제공합니다.")
def search_local_ordinance(query: Optional[str] = None, search: int = 2, display: int = 20, page: int = 1) -> TextContent:
    """자치법규 검색"""
    if not query or not query.strip():
        return TextContent(type="text", text="❌ 검색어를 입력해주세요.")
    
    search_query = query.strip()
    params = {"target": "ordinance", "query": search_query, "search": search, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ordinance", params)
        url = _generate_api_url("ordinance", params)
        result = _format_search_results(data, "ordinance", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"자치법규 검색 중 오류: {str(e)}")

@mcp.tool(name="search_ordinance_appendix", description="자치법규 별표서식을 검색합니다. 조례와 규칙의 별표 및 서식을 제공합니다.")
def search_ordinance_appendix(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """자치법규 별표서식 검색"""
    if not query or not query.strip():
        return TextContent(type="text", text="❌ 검색어를 입력해주세요.")
    
    search_query = query.strip()
    params = {"target": "ordinanceApp", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ordinanceApp", params)
        url = _generate_api_url("ordinanceApp", params)
        result = _format_search_results(data, "ordinanceApp", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"자치법규 별표서식 검색 중 오류: {str(e)}")

@mcp.tool(name="search_linked_ordinance", description="연계 자치법규를 검색합니다. 법령과 연계된 조례를 조회할 수 있습니다.")
def search_linked_ordinance(
    query: Optional[str] = None,
    law_id: Optional[str] = None,
    ordinance_id: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> TextContent:
    """연계 자치법규 검색"""
    params = {"target": "ordinanceLink", "display": min(display, 100), "page": page}
    
    if query and query.strip():
        params["query"] = query.strip()
    if law_id:
        params["LID"] = law_id
    if ordinance_id:
        params["OID"] = ordinance_id
    
    try:
        data = _make_legislation_request("ordinanceLink", params)
        url = _generate_api_url("ordinanceLink", params)
        search_term = query or f"법령ID:{law_id}" if law_id else f"자치법규ID:{ordinance_id}" if ordinance_id else "연계 자치법규"
        result = _format_search_results(data, "ordinanceLink", search_term, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"연계 자치법규 검색 중 오류: {str(e)}")

@mcp.tool(name="get_local_ordinance_detail", description="자치법규 상세내용을 조회합니다. 특정 자치법규의 본문을 제공합니다.")
def get_local_ordinance_detail(ordinance_id: Union[str, int]) -> TextContent:
    """자치법규 본문 조회"""
    params = {"target": "ordinance", "ID": str(ordinance_id)}
    try:
        data = _make_legislation_request("ordinance", params)
        url = _generate_api_url("ordinance", params)
        result = _format_search_results(data, "ordinance", f"자치법규ID:{ordinance_id}", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"자치법규 상세 조회 중 오류: {str(e)}") 
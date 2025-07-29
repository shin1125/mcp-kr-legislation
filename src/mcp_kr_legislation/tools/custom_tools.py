"""
한국 법제처 OPEN API - 맞춤형 도구들

사용자 맞춤형 자치법규, 판례 분류에 따른 검색을 제공합니다.
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

# 유틸리티 함수들 import (law_tools로 변경)
from .law_tools import (
    _make_legislation_request,
    _generate_api_url,
    _format_search_results
)

# ===========================================
# 맞춤형 도구들 (자치법규, 판례)
# ===========================================

@mcp.tool(name="search_custom_ordinance", description="""맞춤형 자치법규를 검색합니다.

매개변수:
- query: 검색어 (선택) - 자치법규명 또는 키워드
- display: 결과 개수 (최대 100)
- page: 페이지 번호

사용 예시: search_custom_ordinance("환경보호"), search_custom_ordinance("시설관리", display=50)
참고: 사용자 맞춤형으로 분류된 자치법규를 검색합니다.""")
def search_custom_ordinance(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 자치법규 검색
    
    Args:
        query: 검색어 (자치법규명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "customOrdinance",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "맞춤형 자치법규"
        
        # API 요청
        data = _make_legislation_request("custOrdinListGuide", params)
        result = _format_search_results(data, "customOrdinance", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"맞춤형 자치법규 검색 중 오류: {e}")
        return TextContent(type="text", text=f"맞춤형 자치법규 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_custom_ordinance_articles", description="""맞춤형 자치법규 조문을 검색합니다.

매개변수:
- query: 검색어 (선택) - 자치법규명 또는 조문 내용
- display: 결과 개수 (최대 100)
- page: 페이지 번호

사용 예시: search_custom_ordinance_articles("제1조"), search_custom_ordinance_articles("사용료", display=50)
참고: 사용자 맞춤형으로 분류된 자치법규의 조문별 내용을 검색합니다.""")
def search_custom_ordinance_articles(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 자치법규 조문 검색
    
    Args:
        query: 검색어 (자치법규명 또는 조문)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "customOrdinanceArticles",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "맞춤형 자치법규 조문"
        
        # API 요청
        data = _make_legislation_request("custOrdinJoListGuide", params)
        result = _format_search_results(data, "customOrdinanceArticles", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"맞춤형 자치법규 조문 검색 중 오류: {e}")
        return TextContent(type="text", text=f"맞춤형 자치법규 조문 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_custom_precedent", description="""맞춤형 판례를 검색합니다.

매개변수:
- query: 검색어 (선택) - 판례 관련 키워드
- display: 결과 개수 (최대 100)
- page: 페이지 번호

사용 예시: search_custom_precedent("손해배상"), search_custom_precedent("계약해제", display=50)
참고: 사용자 맞춤형으로 분류된 판례를 검색합니다.""")
def search_custom_precedent(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 판례 검색
    
    Args:
        query: 검색어 (판례 관련)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "customPrecedent",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "맞춤형 판례"
        
        # API 요청
        data = _make_legislation_request("custPrecListGuide", params)
        result = _format_search_results(data, "customPrecedent", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"맞춤형 판례 검색 중 오류: {e}")
        return TextContent(type="text", text=f"맞춤형 판례 검색 중 오류가 발생했습니다: {str(e)}") 
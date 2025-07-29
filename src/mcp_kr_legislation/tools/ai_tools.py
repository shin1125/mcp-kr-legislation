"""
한국 법제처 OPEN API - AI 도구들

AI 기반 종합 법률 검색 등 인공지능 기반 검색 기능을 제공합니다.
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
# AI 도구들 (1개)
# ===========================================

@mcp.tool(name="search_legal_ai", description="""AI 기반 종합 법률 검색을 수행합니다.

매개변수:
- query: 검색어 (필수)
- target: 검색 대상 (기본값: all)
  - all: 전체
  - law: 법령
  - prec: 판례
  - expc: 해석례
  - committee: 위원회결정문
- display: 결과 개수 (1-50, 기본값: 10)
- page: 페이지 번호 (기본값: 1)
- sort: 정렬 방식
  - rel: 관련도순
  - date: 최신순
  - alpha: 가나다순

반환정보: 
- 법령: 법령명, 법령ID, 공포일자, 시행일자
- 판례: 사건명, 판례ID, 선고일자, 법원명
- 해석례: 제목, 해석례ID, 작성일자, 소관부처
- 위원회결정문: 안건명, 결정문ID, 의결일자, 위원회명

사용 예시:
- search_legal_ai("개인정보보호")  # 전체 검색
- search_legal_ai("근로기준", target="law")  # 법령만 검색
- search_legal_ai("손해배상", target="prec", sort="date")  # 판례 최신순 검색

참고: AI가 여러 법률 문서를 종합적으로 검색하여 관련도가 높은 결과를 제공합니다.""")
def search_legal_ai(
    query: Optional[str] = None,
    target: str = "all",
    display: int = 10,
    page: int = 1,
    sort: Optional[str] = None
) -> TextContent:
    """AI 기반 종합 법률 검색
    
    Args:
        query: 검색어 (필수)
        target: 검색 대상 (all=전체, law=법령, prec=판례, expc=해석례, committee=위원회결정문)
        display: 결과 개수 (1-50)
        page: 페이지 번호 
        sort: 정렬 방식 (rel=관련도순, date=최신순, alpha=가나다순)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    
    # AI 검색 파라미터 구성
    params = {
        "query": search_query,
        "target": target,
        "display": min(max(display, 1), 50),
        "page": max(page, 1)
    }
    
    if sort:
        params["sort"] = sort
        
    try:
        # AI 검색 API 호출
        data = _make_legislation_request("legalAi", params)
        url = _generate_api_url("legalAi", params)
        
        # 결과 포맷팅
        if not data:
            return TextContent(type="text", text=f"'{search_query}'에 대한 AI 검색 결과가 없습니다.")
        
        # AI 검색 결과는 특별한 포맷팅이 필요할 수 있음
        result = f"AI 기반 종합 법률 검색 결과: '{search_query}'\n"
        result += f"API URL: {url}\n\n"
        
        # 다양한 응답 형식 처리
        if isinstance(data, dict):
            # 법령 결과
            if 'laws' in data and data['laws']:
                result += "**관련 법령:**\n"
                for i, law in enumerate(data['laws'][:5], 1):
                    result += f"{i}. {law.get('title', '제목없음')}\n"
                result += "\n"
            
            # 판례 결과  
            if 'precedents' in data and data['precedents']:
                result += "**관련 판례:**\n"
                for i, prec in enumerate(data['precedents'][:5], 1):
                    result += f"{i}. {prec.get('title', '제목없음')}\n"
                result += "\n"
            
            # 해석례 결과
            if 'interpretations' in data and data['interpretations']:
                result += "**관련 해석례:**\n"
                for i, interp in enumerate(data['interpretations'][:5], 1):
                    result += f"{i}. {interp.get('title', '제목없음')}\n"
                result += "\n"
            
            # 위원회 결정문 결과
            if 'committees' in data and data['committees']:
                result += "**관련 위원회 결정문:**\n"
                for i, comm in enumerate(data['committees'][:5], 1):
                    result += f"{i}. {comm.get('title', '제목없음')}\n"
                result += "\n"
                
        else:
            # 일반 검색 결과 포맷 사용
            result = _format_search_results(data, "legalAi", search_query, url)
        
        result += f"\n더 자세한 검색을 원하시면 각 분야별 전문 검색 도구를 이용하세요.\n"
        result += f"   - 법령: search_law\n"
        result += f"   - 판례: search_precedent\n" 
        result += f"   - 해석례: search_legal_interpretation\n"
        result += f"   - 위원회: search_*_committee 도구들\n"
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        return TextContent(type="text", text=f"AI 기반 법률 검색 중 오류: {str(e)}") 
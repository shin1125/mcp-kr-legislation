"""
한국 법제처 OPEN API - 판례 관련 도구들

대법원 판례, 헌법재판소 결정례, 법령해석례, 행정심판례 등 
판례 관련 검색 및 조회 기능을 제공합니다.
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
# 판례 관련 도구들 (8개)
# ===========================================

@mcp.tool(name="search_precedent", description="""대법원 판례를 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=판례명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- court_type: 법원종류 (400201=대법원, 400202=하위법원)
- court_name: 법원명 (대법원, 서울고등법원, 광주지법, 인천지방법원 등)
- referenced_law: 참조법령명 (형법, 민법 등)
- sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=선고일자오름차순, ddes=선고일자내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
- date: 판례 선고일자 (YYYYMMDD)
- date_range: 선고일자 범위 (20090101~20090130)
- case_number: 판례 사건번호
- data_source: 데이터출처명 (국세법령정보시스템, 근로복지공단산재판례, 대법원)""")
def search_precedent(
    query: Optional[str] = None,
    search: int = 2,  # 본문검색이 제목검색보다 더 풍부한 결과 제공
    display: int = 20,
    page: int = 1,
    court_type: Optional[str] = None,
    court_name: Optional[str] = None,
    referenced_law: Optional[str] = None,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None,
    date: Optional[str] = None,
    date_range: Optional[str] = None,
    case_number: Optional[str] = None,
    data_source: Optional[str] = None
) -> TextContent:
    """판례 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=판례명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        court_type: 법원종류 (400201=대법원, 400202=하위법원)
        court_name: 법원명 (대법원, 서울고등법원, 광주지법, 인천지방법원 등)
        referenced_law: 참조법령명 (형법, 민법 등)
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=선고일자오름차순, ddes=선고일자내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
        date: 판례 선고일자 (YYYYMMDD)
        date_range: 선고일자 범위 (20090101~20090130)
        case_number: 판례 사건번호
        data_source: 데이터출처명 (국세법령정보시스템, 근로복지공단산재판례, 대법원)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if court_type:
        params["org"] = court_type
    if court_name:
        params["nw"] = court_name  # 실제 API 테스트에서 nw(84건) > curt(36건) 확인
    if referenced_law:
        params["JO"] = referenced_law
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
    if date:
        params["date"] = date
    if date_range:
        params["prncYd"] = date_range
    if case_number:
        params["nb"] = case_number
    if data_source:
        params["datSrcNm"] = data_source
    
    try:
        data = _make_legislation_request("prec", params)
        url = _generate_api_url("prec", params)
        result = _format_search_results(data, "prec", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"판례 검색 중 오류: {str(e)}")

@mcp.tool(name="search_constitutional_court", description="헌법재판소 결정례를 검색합니다. 매개변수: query(필수), display, page")
def search_constitutional_court(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """헌법재판소 결정례 검색"""
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    params = {"target": "detc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("detc", params)
        url = _generate_api_url("detc", params)
        result = _format_search_results(data, "detc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"헌법재판소 결정례 검색 중 오류: {str(e)}")

@mcp.tool(name="search_legal_interpretation", description="법제처 법령해석례를 검색합니다. 매개변수: query(필수), display, page")
def search_legal_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령해석례 검색"""
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("expc", params)
        url = _generate_api_url("expc", params)
        result = _format_search_results(data, "expc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령해석례 검색 중 오류: {str(e)}")

@mcp.tool(name="search_administrative_trial", description="행정심판례를 검색합니다. 매개변수: query(필수), search(1=사건명, 2=본문검색), display, page")
def search_administrative_trial(query: Optional[str] = None, search: int = 1, display: int = 20, page: int = 1) -> TextContent:
    """행정심판례 검색"""
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    params = {"target": "decc", "query": search_query, "search": search, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("decc", params)
        url = _generate_api_url("decc", params)
        result = _format_search_results(data, "decc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정심판례 검색 중 오류: {str(e)}")

@mcp.tool(name="get_administrative_trial_detail", description="""행정심판례 상세내용을 조회합니다.

매개변수:
- trial_id: 행정심판례ID - search_administrative_trial 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_administrative_trial_detail(trial_id="123456")""")
def get_administrative_trial_detail(trial_id: Union[str, int]) -> TextContent:
    """행정심판례 본문 조회"""
    params = {"target": "decc", "ID": str(trial_id)}
    try:
        data = _make_legislation_request("decc", params)
        url = _generate_api_url("decc", params)
        result = _format_search_results(data, "decc", f"행정심판례ID:{trial_id}", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정심판례 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_precedent_detail", description="""판례 상세내용을 조회합니다. 국세청 판례의 경우 HTML만 지원됩니다.

매개변수:
- case_id: 판례ID - search_precedent 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_precedent_detail(case_id="123456")
참고: 국세청 판례는 HTML 형태로만 제공됩니다.""")
def get_precedent_detail(case_id: Union[str, int]) -> TextContent:
    """판례 본문 조회 - 개선된 JSON/HTML 지원"""
    params = {"ID": str(case_id)}
    
    try:
        # 기본 JSON 시도
        data = _make_legislation_request("prec", params)
        url = _generate_api_url("prec", params)
        
        # JSON 응답 확인
        if isinstance(data, dict) and data:
            result = _format_search_results(data, "prec", f"판례ID:{case_id}", url)
            return TextContent(type="text", text=result)
        else:
            # HTML 폴백 (국세청 판례 등)
            oc = os.getenv("LEGISLATION_API_KEY", "lchangoo")
            html_params = {"OC": oc, "target": "prec", "ID": str(case_id)}
            
            url = f"{legislation_config.service_base_url}?{urlencode(html_params)}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            # HTML 응답 포맷팅
            return _format_html_precedent_response(response.text, str(case_id), url)
            
    except json.JSONDecodeError as je:
        # JSON 파싱 실패시 HTML 폴백
        try:
            oc = os.getenv("LEGISLATION_API_KEY", "lchangoo") 
            html_params = {"OC": oc, "target": "prec", "ID": str(case_id)}
            
            url = f"{legislation_config.service_base_url}?{urlencode(html_params)}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            return _format_html_precedent_response(response.text, str(case_id), url)
            
        except Exception as he:
            return TextContent(type="text", text=f"JSON 파싱 오류 (HTML 폴백 실패): {str(je)}\n\nsearch_precedent 도구로 올바른 판례 ID를 먼저 확인해보세요.\n\nAPI URL: {url}")
            
    except Exception as e:
        return TextContent(type="text", text=f"판례 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_constitutional_court_detail", description="""헌법재판소 결정례 상세내용을 조회합니다.

매개변수:
- decision_id: 결정례ID - search_constitutional_court 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_constitutional_court_detail(decision_id="123456")""")
def get_constitutional_court_detail(decision_id: Union[str, int]) -> TextContent:
    """헌법재판소 결정례 본문 조회"""
    params = {"target": "detc", "ID": str(decision_id)}
    try:
        data = _make_legislation_request("detc", params)
        url = _generate_api_url("detc", params)
        result = _format_search_results(data, "detc", f"헌법재판소결정례ID:{decision_id}", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"헌법재판소 결정례 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_legal_interpretation_detail", description="""법령해석례 상세내용을 조회합니다.

매개변수:
- interpretation_id: 해석례ID - search_legal_interpretation 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_legal_interpretation_detail(interpretation_id="123456")""")
def get_legal_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """법령해석례 본문 조회"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("expc", params)
        url = _generate_api_url("expc", params)
        result = _format_search_results(data, "expc", f"법령해석례ID:{interpretation_id}", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령해석례 상세 조회 중 오류: {str(e)}")

def _format_html_precedent_response(html_content: str, case_id: str, url: str) -> TextContent:
    """HTML 판례 응답 포맷팅"""
    try:
        # HTML 태그 제거 (간단한 처리)
        import re
        text_content = re.sub(r'<[^>]+>', '', html_content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        # 길이 제한
        if len(text_content) > 2000:
            text_content = text_content[:2000] + "..."
        
        formatted_result = f"""판례 상세내용 (사건번호: {case_id})

내용
{text_content}

API URL: {url}

참고: 이 판례는 HTML 형식으로 제공됩니다."""
        
        return TextContent(type="text", text=formatted_result)
    except Exception as e:
        return TextContent(type="text", text=f"HTML 판례 응답 처리 중 오류: {str(e)}") 
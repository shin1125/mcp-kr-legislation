"""
한국 법제처 OPEN API - 위원회 결정문 도구들

개인정보보호위원회, 금융위원회, 공정거래위원회, 국민권익위원회, 노동위원회 등
다양한 위원회의 결정문 검색 및 조회 기능을 제공합니다.
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
# 위원회 결정문 도구들 (30개)
# ===========================================

@mcp.tool(name="search_privacy_committee", description="""개인정보보호위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=의안명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=의안명오름차순, ldes=의안명내림차순, dasc=개최일자오름차순, ddes=개최일자내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_privacy_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """개인정보보호위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=의안명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=의안명오름차순, ldes=의안명내림차순, dasc=개최일자오름차순, ddes=개최일자내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("ppc", params)
        url = _generate_api_url("ppc", params)
        result = _format_search_results(data, "ppc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"개인정보보호위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_financial_committee", description="""금융위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=안건명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=안건명오름차순, ldes=안건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_financial_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """금융위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=안건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=안건명오름차순, ldes=안건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("fsc", params)
        url = _generate_api_url("fsc", params)
        result = _format_search_results(data, "fsc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"금융위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_monopoly_committee", description="""공정거래위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=의결내용명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=의결내용명오름차순, ldes=의결내용명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_monopoly_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """공정거래위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=의결내용명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=의결내용명오름차순, ldes=의결내용명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("ftc", params)
        url = _generate_api_url("ftc", params)
        result = _format_search_results(data, "ftc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"공정거래위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_anticorruption_committee", description="""국민권익위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=안건명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=안건명오름차순, ldes=안건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_anticorruption_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """국민권익위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=안건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=안건명오름차순, ldes=안건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("acr", params)
        url = _generate_api_url("acr", params)
        result = _format_search_results(data, "acr", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국민권익위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_labor_committee", description="""노동위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=사건명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=재정일자오름차순, ddes=재정일자내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_labor_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """노동위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=사건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=재정일자오름차순, ddes=재정일자내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("nlrc", params)
        url = _generate_api_url("nlrc", params)
        result = _format_search_results(data, "nlrc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"노동위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_environment_committee", description="""중앙환경분쟁조정위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=사건명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, nasc=의결번호오름차순, ndes=의결번호내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_environment_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """중앙환경분쟁조정위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=사건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, nasc=의결번호오름차순, ndes=의결번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("ecc", params)
        url = _generate_api_url("ecc", params)
        result = _format_search_results(data, "ecc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중앙환경분쟁조정위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_securities_committee", description="""증권선물위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=사건명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_securities_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """증권선물위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=사건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("sfc", params)
        url = _generate_api_url("sfc", params)
        result = _format_search_results(data, "sfc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"증권선물위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_human_rights_committee", description="""국가인권위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=사건명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_human_rights_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """국가인권위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=사건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("nhrck", params)
        url = _generate_api_url("nhrck", params)
        result = _format_search_results(data, "nhrck", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국가인권위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_broadcasting_committee", description="""방송통신위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=안건명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=안건명오름차순, ldes=안건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=안건번호오름차순, ndes=안건번호내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_broadcasting_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """방송통신위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=안건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=안건명오름차순, ldes=안건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=안건번호오름차순, ndes=안건번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("kcc", params)
        url = _generate_api_url("kcc", params)
        result = _format_search_results(data, "kcc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"방송통신위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_industrial_accident_committee", description="""산업재해보상보험 재심사위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=사건, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=사건오름차순, ldes=사건내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_industrial_accident_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """산업재해보상보험재심사위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=사건, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=사건오름차순, ldes=사건내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("iaciac", params)
        url = _generate_api_url("iaciac", params)
        result = _format_search_results(data, "iaciac", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"산업재해보상보험재심사위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_land_tribunal", description="""중앙토지수용위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=제목, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=제목오름차순, ldes=제목내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_land_tribunal(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """중앙토지수용위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=제목, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=제목오름차순, ldes=제목내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("oclt", params)
        url = _generate_api_url("oclt", params)
        result = _format_search_results(data, "oclt", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중앙토지수용위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_employment_insurance_committee", description="""고용보험심사위원회 결정문을 검색합니다.

매개변수:
- query: 검색어 (필수)
- search: 검색범위 (1=사건명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
- alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)""")
def search_employment_insurance_committee(
    query: Optional[str] = None, 
    search: int = 2, 
    display: int = 20, 
    page: int = 1,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """고용보험심사위원회 결정문 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=사건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요.")
    
    search_query = query.strip()
    # search=2 (본문검색) 파라미터로 더 많은 결과 확보
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("eiac", params)
        url = _generate_api_url("eiac", params)
        result = _format_search_results(data, "eiac", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"고용보험심사위원회 결정문 검색 중 오류: {str(e)}")

# ===========================================
# 위원회 결정문 상세 조회 도구들
# ===========================================

@mcp.tool(name="get_privacy_committee_detail", description="""개인정보보호위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_privacy_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_privacy_committee_detail(decision_id="123456")""")
def get_privacy_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """개인정보보호위원회 결정문 본문 조회 (ppc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("ppc", params, is_detail=True)
        url = _generate_api_url("ppc", params, is_detail=True)
        result = _format_search_results(data, "ppc", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"개인정보보호위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(
    name="get_financial_committee_detail", 
    description="""금융위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_financial_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_financial_committee_detail(decision_id="123456")""",
    tags={"금융위원회", "결정문", "상세조회", "금융규제", "위원회"}
)
def get_financial_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """금융위원회 결정문 본문 조회 (fsc)"""
    if not decision_id:
        return TextContent(type="text", text="결정문 ID를 입력해주세요.")
    
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("fsc", params, is_detail=True)
        url = _generate_api_url("fsc", params, is_detail=True)
        
        # 응답 데이터 유효성 검사 강화
        if not data or isinstance(data, str) and "error" in data.lower():
            return TextContent(type="text", text=f"ID '{decision_id}'에 해당하는 금융위원회 결정문을 찾을 수 없습니다.\n\nsearch_financial_committee 도구로 올바른 ID를 먼저 확인해보세요.\n\nAPI URL: {url}")
        
        # JSON 파싱 오류 방지를 위한 안전한 처리
        if isinstance(data, dict) and not data:
            return TextContent(type="text", text=f"ID '{decision_id}'에 해당하는 결정문의 상세 내용이 없습니다.\n\nAPI URL: {url}")
        
        result = _format_search_results(data, "fsc", str(decision_id))
        return TextContent(type="text", text=result)
    except json.JSONDecodeError as e:
        return TextContent(type="text", text=f"응답 데이터 파싱 오류: {str(e)}\n\nAPI 응답 형식에 문제가 있을 수 있습니다. 다른 ID로 시도해보세요.")
    except Exception as e:
        return TextContent(type="text", text=f"금융위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_monopoly_committee_detail", description="""공정거래위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_monopoly_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_monopoly_committee_detail(decision_id="123456")""")
def get_monopoly_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """공정거래위원회 결정문 본문 조회 (ftc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("ftc", params, is_detail=True)
        url = _generate_api_url("ftc", params, is_detail=True)
        result = _format_search_results(data, "ftc", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"공정거래위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_anticorruption_committee_detail", description="""국민권익위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_anticorruption_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_anticorruption_committee_detail(decision_id="123456")""")
def get_anticorruption_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """국민권익위원회 결정문 본문 조회 (acr)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("acr", params)
        url = _generate_api_url("acr", params)
        result = _format_search_results(data, "acr", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국민권익위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_labor_committee_detail", description="""노동위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_labor_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_labor_committee_detail(decision_id="123456")""")
def get_labor_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """노동위원회 결정문 본문 조회 (nlrc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("nlrc", params)
        url = _generate_api_url("nlrc", params)
        result = _format_search_results(data, "nlrc", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"노동위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_environment_committee_detail", description="""중앙환경분쟁조정위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_environment_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_environment_committee_detail(decision_id="123456")""")
def get_environment_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """중앙환경분쟁조정위원회 결정문 본문 조회 (ecc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("ecc", params)
        url = _generate_api_url("ecc", params)
        result = _format_search_results(data, "ecc", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중앙환경분쟁조정위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_securities_committee_detail", description="""증권선물위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_securities_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_securities_committee_detail(decision_id="123456")""")
def get_securities_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """증권선물위원회 결정문 본문 조회 (sfc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("sfc", params)
        url = _generate_api_url("sfc", params)
        result = _format_search_results(data, "sfc", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"증권선물위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_human_rights_committee_detail", description="""국가인권위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_human_rights_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_human_rights_committee_detail(decision_id="123456")""")
def get_human_rights_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """국가인권위원회 결정문 본문 조회 (nhrck)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("nhrck", params)
        url = _generate_api_url("nhrck", params)
        result = _format_search_results(data, "nhrck", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국가인권위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_broadcasting_committee_detail", description="""방송통신위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_broadcasting_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_broadcasting_committee_detail(decision_id="123456")""")
def get_broadcasting_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """방송통신위원회 결정문 본문 조회 (kcc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("kcc", params)
        url = _generate_api_url("kcc", params)
        result = _format_search_results(data, "kcc", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"방송통신위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_industrial_accident_committee_detail", description="""산업재해보상보험 재심사위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_industrial_accident_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_industrial_accident_committee_detail(decision_id="123456")""")
def get_industrial_accident_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """산업재해보상보험 재심사위원회 결정문 본문 조회 (eiac)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("eiac", params)
        url = _generate_api_url("eiac", params)
        result = _format_search_results(data, "eiac", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"산업재해보상보험 재심사위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_land_tribunal_detail", description="""중앙토지수용위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_land_tribunal 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_land_tribunal_detail(decision_id="123456")""")
def get_land_tribunal_detail(decision_id: Union[str, int]) -> TextContent:
    """중앙토지수용위원회 결정문 본문 조회 (lx)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("oclt", params)
        url = _generate_api_url("oclt", params)
        result = _format_search_results(data, "oclt", str(decision_id))
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중앙토지수용위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_employment_insurance_committee_detail", description="""고용보험심사위원회 결정문 상세내용을 조회합니다.

매개변수:
- decision_id: 결정문ID - search_employment_insurance_committee 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_employment_insurance_committee_detail(decision_id="123456")""")
def get_employment_insurance_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """고용보험심사위원회 결정문 본문 조회"""
    params = {"target": "eiac", "ID": str(decision_id)}
    try:
        data = _make_legislation_request("eiac", params)
        result = _format_search_results(data, "eiac", f"결정문ID:{decision_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"고용보험심사위원회 결정문 상세 조회 중 오류: {str(e)}") 
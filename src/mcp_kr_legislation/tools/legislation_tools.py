"""
한국 법제처 OPEN API 119개 완전 통합 MCP 도구

119개의 모든 API를 구현하여 한국의 법령, 행정규칙, 자치법규, 판례, 위원회결정문 등 
모든 법률 정보에 대한 포괄적인 접근을 제공합니다.

API 카테고리:
- 법령 관련 (16개)
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

import logging
import json
from pathlib import Path
from typing import Any, Optional, Union, List, Dict
import os

try:
    import requests  # type: ignore
except ImportError:
    requests = None

from ..server import mcp, ctx
from mcp.types import TextContent
from mcp_kr_legislation.utils.data_processor import get_cache_dir
from mcp_kr_legislation.utils.ctx_helper import with_context

logger = logging.getLogger(__name__)

def _save_legislation_data(data: dict, filename: str, target_dir: Optional[str] = None) -> str:
    """법령 데이터를 JSON 파일로 저장하고 경로 반환"""
    if target_dir is None:
        target_dir = get_cache_dir()
    
    cache_dir = Path(target_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = cache_dir / f"{filename}.json"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return str(file_path)

def _make_api_request(target: str, service_type: str = "search", **params) -> Dict[str, Any]:
    """법제처 API 요청을 위한 공통 함수"""
    if requests is None:
        return {"error": "requests 라이브러리가 설치되지 않았습니다"}
    
    # API 키 설정
    oc = os.getenv("LEGISLATION_API_KEY", "test")
    
    # 기본 URL 설정
    if service_type == "search":
        base_url = "http://www.law.go.kr/DRF/lawSearch.do"
    else:  # service
        base_url = "http://www.law.go.kr/DRF/lawService.do"
    
    # 기본 파라미터
    request_params: Dict[str, Any] = {
        "OC": oc,
        "target": target,
        "type": "JSON"
    }
    
    # 추가 파라미터
    for key, value in params.items():
        if value is not None:
            request_params[key] = value
    
    try:
        response = requests.get(base_url, params=request_params, timeout=30)  # type: ignore
        response.raise_for_status()
        
        # JSON 응답 파싱
        content_type = response.headers.get('content-type', '')
        if content_type.startswith('application/json'):
            return response.json()
        else:
            # HTML/XML 응답의 경우
            return {"content": response.text, "content_type": content_type}
            
    except Exception as e:
        logger.error(f"API 요청 실패: {e}")
        return {"error": str(e)}

# ===========================================
# 법령 관련 도구 (16개)
# ===========================================

@mcp.tool(
    name="search_law",
    description="한국의 현행 법령을 검색합니다. 근로기준법, 민법, 형법 등 모든 법령을 검색할 수 있습니다."
)
def search_law(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1,
    sort: str = "lasc",
    anc_yd: Optional[str] = None,
    org: Optional[str] = None
) -> str:
    """
    현행 법령 목록을 검색합니다.
    
    Args:
        query: 검색할 법령명 또는 키워드
        search_type: 1=법령명 검색, 2=본문 검색
        display: 결과 개수 (최대 100)
        page: 페이지 번호
        sort: 정렬 옵션 (lasc, ldes, dasc, ddes)
        anc_yd: 공포일자 범위 (예: "20230101~20231231")
        org: 소관부처 코드
    """
    data = _make_api_request(
        target="law",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page,
        sort=sort,
        ancYd=anc_yd,
        org=org
    )
    
    filename = f"law_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_law_info",
    description="특정 법령의 상세 본문을 조회합니다."
)
def get_law_info(
    law_id: Optional[str] = None,
    mst: Optional[str] = None,
    law_name: Optional[str] = None,
    jo: Optional[str] = None
) -> str:
    """
    법령의 상세 본문을 조회합니다.
    
    Args:
        law_id: 법령 ID
        mst: 법령 마스터 번호  
        law_name: 법령명
        jo: 조번호 (6자리, 예: "000200" = 2조)
    """
    data = _make_api_request(
        target="law",
        service_type="service",
        ID=law_id,
        MST=mst,
        LM=law_name,
        JO=jo
    )
    
    filename = f"law_info_{law_id or mst or 'query'}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_englaw",
    description="영문 법령을 검색합니다."
)
def search_englaw(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """영문 법령을 검색합니다."""
    data = _make_api_request(
        target="elaw",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"englaw_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"영문 법령 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_englaw_info", 
    description="특정 영문 법령의 상세 정보를 조회합니다."
)
def get_englaw_info(
    law_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """영문 법령의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="elaw",
        service_type="service",
        ID=law_id,
        MST=mst
    )
    
    filename = f"englaw_info_{law_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"영문 법령 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_eflaw",
    description="시행일 법령을 검색합니다."
)
def search_eflaw(
    query: Optional[str] = None,
    nw: Optional[int] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """
    시행일 법령을 검색합니다.
    
    Args:
        query: 검색할 법령명
        nw: 1=연혁, 2=시행예정, 3=현행
        display: 결과 개수
        page: 페이지 번호
    """
    data = _make_api_request(
        target="eflaw", 
        service_type="search",
        query=query,
        nw=nw,
        display=display,
        page=page
    )
    
    filename = f"eflaw_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"시행일 법령 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_eflaw_info",
    description="시행일 법령의 상세 본문을 조회합니다."
)
def get_eflaw_info(
    law_id: Optional[str] = None,
    mst: Optional[str] = None,
    ef_yd: Optional[str] = None,
    jo: Optional[str] = None
) -> str:
    """시행일 법령의 상세 본문을 조회합니다."""
    data = _make_api_request(
        target="eflaw",
        service_type="service",
        ID=law_id,
        MST=mst,
        efYd=ef_yd,
        JO=jo
    )
    
    filename = f"eflaw_info_{law_id or mst or 'query'}"
    file_path = _save_legislation_data(data, filename)
    
    return f"시행일 법령 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_history",
    description="법령 연혁 목록을 조회합니다."
)
def search_law_history(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1,
    org: Optional[str] = None
) -> str:
    """법령 연혁 목록을 조회합니다."""
    data = _make_api_request(
        target="lsHistory",
        service_type="search",
        query=query,
        display=display,
        page=page,
        org=org
    )
    
    filename = f"law_history_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 연혁 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_law_history_info",
    description="법령 연혁의 상세 본문을 조회합니다."
)
def get_law_history_info(
    law_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """법령 연혁의 상세 본문을 조회합니다."""
    data = _make_api_request(
        target="lsHistory",
        service_type="service",
        ID=law_id,
        MST=mst
    )
    
    filename = f"law_history_info_{law_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 연혁 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_article_detail",
    description="현행법령 본문의 조항호목을 상세 조회합니다."
)
def search_law_article_detail(
    law_id: Optional[str] = None,
    mst: Optional[str] = None,
    jo: str = "000100",
    hang: Optional[str] = None,
    ho: Optional[str] = None,
    mok: Optional[str] = None
) -> str:
    """현행법령 본문의 조항호목을 상세 조회합니다."""
    data = _make_api_request(
        target="lawjosub",
        service_type="service",
        ID=law_id,
        MST=mst,
        JO=jo,
        HANG=hang,
        HO=ho,
        MOK=mok
    )
    
    filename = f"law_article_detail_{law_id or mst}_{jo}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 조항호목 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_eflaw_article_detail",
    description="시행일법령 본문의 조항호목을 상세 조회합니다."
)
def search_eflaw_article_detail(
    law_id: Optional[str] = None,
    mst: Optional[str] = None,
    ef_yd: str = "20240101",
    jo: str = "000100",
    hang: Optional[str] = None,
    ho: Optional[str] = None,
    mok: Optional[str] = None
) -> str:
    """시행일법령 본문의 조항호목을 상세 조회합니다."""
    data = _make_api_request(
        target="eflawjosub",
        service_type="service",
        ID=law_id,
        MST=mst,
        efYd=ef_yd,
        JO=jo,
        HANG=hang,
        HO=ho,
        MOK=mok
    )
    
    filename = f"eflaw_article_detail_{law_id or mst}_{jo}"
    file_path = _save_legislation_data(data, filename)
    
    return f"시행일법령 조항호목 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_changes",
    description="법령 변경이력 목록을 조회합니다."
)
def search_law_changes(
    reg_dt: str,
    org: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령 변경이력 목록을 조회합니다."""
    data = _make_api_request(
        target="lsHstInf",
        service_type="search",
        regDt=reg_dt,
        org=org,
        display=display,
        page=page
    )
    
    filename = f"law_changes_{reg_dt}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 변경이력이 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_daily_article_revisions",
    description="일자별 조문 개정 이력을 조회합니다."
)
def search_daily_article_revisions(
    reg_dt: Optional[str] = None,
    from_reg_dt: Optional[str] = None,
    to_reg_dt: Optional[str] = None,
    law_id: Optional[str] = None,
    jo: Optional[str] = None,
    org: Optional[str] = None,
    page: int = 1
) -> str:
    """일자별 조문 개정 이력을 조회합니다."""
    data = _make_api_request(
        target="lsJoHstInf",
        service_type="search",
        regDt=reg_dt,
        fromRegDt=from_reg_dt,
        toRegDt=to_reg_dt,
        ID=law_id,
        JO=jo,
        org=org,
        page=page
    )
    
    filename = f"daily_article_revisions_{reg_dt or 'range'}"
    file_path = _save_legislation_data(data, filename)
    
    return f"일자별 조문 개정 이력이 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_article_change_history",
    description="조문별 변경 이력 목록을 조회합니다."
)
def search_article_change_history(
    law_id: str,
    jo: str,
    display: int = 20,
    page: int = 1
) -> str:
    """조문별 변경 이력 목록을 조회합니다."""
    data = _make_api_request(
        target="lsJoHstInf",
        service_type="service",
        ID=law_id,
        JO=jo,
        display=display,
        page=page
    )
    
    filename = f"article_change_history_{law_id}_{jo}"
    file_path = _save_legislation_data(data, filename)
    
    return f"조문별 변경 이력이 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_ordinance_connection",
    description="법령 자치법규 연계 목록을 조회합니다."
)
def search_law_ordinance_connection(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령 자치법규 연계 목록을 조회합니다."""
    data = _make_api_request(
        target="lnkLs",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"law_ordinance_connection_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 자치법규 연계 목록이 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_law_ordinance_connection_status",
    description="법령-자치법규 연계현황을 조회합니다."
)
def get_law_ordinance_connection_status() -> str:
    """법령-자치법규 연계현황을 조회합니다."""
    data = _make_api_request(
        target="drlaw",
        service_type="search"
    )
    
    filename = "law_ordinance_connection_status"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령-자치법규 연계현황이 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_delegated_laws",
    description="위임 법령을 조회합니다."
)
def search_delegated_laws(
    law_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """위임 법령을 조회합니다."""
    data = _make_api_request(
        target="lsDelegated",
        service_type="service",
        ID=law_id,
        MST=mst
    )
    
    filename = f"delegated_laws_{law_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"위임 법령 정보가 저장되었습니다: {file_path}"

# ===========================================
# 행정규칙 관련 도구 (5개) 
# ===========================================

@mcp.tool(
    name="search_admrul",
    description="행정규칙(훈령, 예규, 고시 등)을 검색합니다."
)
def search_admrul(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1,
    org: Optional[str] = None,
    knd: Optional[str] = None
) -> str:
    """
    행정규칙을 검색합니다.
    
    Args:
        query: 검색할 행정규칙명
        search_type: 1=행정규칙명, 2=본문검색
        knd: 행정규칙 종류 (1=훈령, 2=예규, 3=고시, 4=공고, 5=지침, 6=기타)
    """
    data = _make_api_request(
        target="admrul",
        service_type="search", 
        query=query,
        search=search_type,
        display=display,
        page=page,
        org=org,
        knd=knd
    )
    
    filename = f"admrul_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정규칙 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_admrul_info",
    description="특정 행정규칙의 상세 정보를 조회합니다."
)
def get_admrul_info(
    admrul_id: str,
    lid: Optional[str] = None
) -> str:
    """행정규칙의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="admrul",
        service_type="service",
        ID=admrul_id,
        LID=lid
    )
    
    filename = f"admrul_info_{admrul_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정규칙 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_admrul_old_new",
    description="행정규칙 신구법 대조표를 검색합니다."
)
def search_admrul_old_new(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """행정규칙 신구법 대조표를 검색합니다."""
    data = _make_api_request(
        target="admrulOldAndNew",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"admrul_old_new_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정규칙 신구법 대조표 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_admrul_old_new_info",
    description="행정규칙 신구법 대조표의 상세 정보를 조회합니다."
)
def get_admrul_old_new_info(
    admrul_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """행정규칙 신구법 대조표의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="admrulOldAndNew",
        service_type="service",
        ID=admrul_id,
        MST=mst
    )
    
    filename = f"admrul_old_new_info_{admrul_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정규칙 신구법 대조표 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_admrul_forms",
    description="행정규칙 별표서식을 검색합니다."
)
def search_admrul_forms(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """행정규칙 별표서식을 검색합니다."""
    data = _make_api_request(
        target="admrulByl",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"admrul_forms_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정규칙 별표서식 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 자치법규 관련 도구 (4개)
# ===========================================

@mcp.tool(
    name="search_ordin",
    description="자치법규(조례, 규칙 등)를 검색합니다."
)
def search_ordin(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1,
    org: Optional[str] = None,
    knd: Optional[str] = None
) -> str:
    """
    자치법규를 검색합니다.
    
    Args:
        query: 검색할 자치법규명
        search_type: 1=자치법규명, 2=본문검색
        org: 지자체 기관코드
        knd: 자치법규 종류 (30001=조례, 30002=규칙, 30003=훈령, 30004=예규)
    """
    data = _make_api_request(
        target="ordin",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page,
        org=org,
        knd=knd
    )
    
    filename = f"ordin_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"자치법규 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ordin_info",
    description="특정 자치법규의 상세 정보를 조회합니다."
)
def get_ordin_info(
    ordin_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """자치법규의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ordin",
        service_type="service",
        ID=ordin_id,
        MST=mst
    )
    
    filename = f"ordin_info_{ordin_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"자치법규 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ordin_law_connection",
    description="자치법규 법령 연계 목록을 조회합니다."
)
def search_ordin_law_connection(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """자치법규 법령 연계 목록을 조회합니다."""
    data = _make_api_request(
        target="ordinLsCon",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"ordin_law_connection_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"자치법규 법령 연계 목록이 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ordin_forms",
    description="자치법규 별표서식을 검색합니다."
)
def search_ordin_forms(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """자치법규 별표서식을 검색합니다."""
    data = _make_api_request(
        target="ordinByl",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"ordin_forms_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"자치법규 별표서식 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 판례 관련 도구 (8개)
# ===========================================

@mcp.tool(
    name="search_prec",
    description="판례를 검색합니다."
)
def search_prec(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1,
    curt: Optional[str] = None,
    org: Optional[str] = None
) -> str:
    """
    판례를 검색합니다.
    
    Args:
        query: 검색할 판례명 또는 키워드
        search_type: 1=판례명, 2=본문검색
        curt: 법원명 (예: "대법원", "서울고등법원")
        org: 법원종류 (400201=대법원, 400202=하위법원)
    """
    data = _make_api_request(
        target="prec",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page,
        curt=curt,
        org=org
    )
    
    filename = f"prec_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"판례 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_prec_info",
    description="특정 판례의 상세 정보를 조회합니다."
)
def get_prec_info(prec_id: str) -> str:
    """판례의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="prec",
        service_type="service",
        ID=prec_id
    )
    
    filename = f"prec_info_{prec_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"판례 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_detc",
    description="헌재결정례를 검색합니다."
)
def search_detc(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """헌재결정례를 검색합니다."""
    data = _make_api_request(
        target="detc",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"detc_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"헌재결정례 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_detc_info",
    description="특정 헌재결정례의 상세 정보를 조회합니다."
)
def get_detc_info(detc_id: str) -> str:
    """헌재결정례의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="detc",
        service_type="service", 
        ID=detc_id
    )
    
    filename = f"detc_info_{detc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"헌재결정례 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_expc",
    description="법령해석례를 검색합니다."
)
def search_expc(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """법령해석례를 검색합니다."""
    data = _make_api_request(
        target="expc", 
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"expc_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령해석례 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_expc_info", 
    description="특정 법령해석례의 상세 정보를 조회합니다."
)
def get_expc_info(expc_id: str) -> str:
    """법령해석례의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="expc",
        service_type="service",
        ID=expc_id
    )
    
    filename = f"expc_info_{expc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령해석례 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_decc",
    description="행정심판례를 검색합니다."
)
def search_decc(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """행정심판례를 검색합니다."""
    data = _make_api_request(
        target="decc",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"decc_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정심판례 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_decc_info",
    description="특정 행정심판례의 상세 정보를 조회합니다."
)
def get_decc_info(decc_id: str) -> str:
    """행정심판례의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="decc",
        service_type="service",
        ID=decc_id
    )
    
    filename = f"decc_info_{decc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정심판례 상세 정보가 저장되었습니다: {file_path}"

# ===========================================
# 조약 관련 도구 (2개)
# ===========================================

@mcp.tool(
    name="search_trty",
    description="조약을 검색합니다."
)
def search_trty(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """조약을 검색합니다."""
    data = _make_api_request(
        target="trty",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"trty_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"조약 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_trty_info",
    description="특정 조약의 상세 정보를 조회합니다."
)
def get_trty_info(trty_id: str) -> str:
    """조약의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="trty",
        service_type="service",
        ID=trty_id
    )
    
    filename = f"trty_info_{trty_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"조약 상세 정보가 저장되었습니다: {file_path}"

# ===========================================
# 법령용어 관련 도구 (2개)
# ===========================================

@mcp.tool(
    name="search_lstrm",
    description="법령용어를 검색합니다."
)
def search_lstrm(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령용어를 검색합니다."""
    data = _make_api_request(
        target="lstrm",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"lstrm_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령용어 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_lstrm_info",
    description="특정 법령용어의 상세 정보를 조회합니다."
)
def get_lstrm_info(lstrm_id: str) -> str:
    """법령용어의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="lstrm",
        service_type="service", 
        ID=lstrm_id
    )
    
    filename = f"lstrm_info_{lstrm_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령용어 상세 정보가 저장되었습니다: {file_path}"

# ===========================================
# 위원회결정문 관련 도구 (30개)
# ===========================================

@mcp.tool(
    name="search_ppc",
    description="개인정보보호위원회 결정문을 검색합니다."
)
def search_ppc(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """개인정보보호위원회 결정문을 검색합니다."""
    data = _make_api_request(
        target="ppc",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"ppc_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"개인정보보호위원회 결정문 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ppc_info",
    description="특정 개인정보보호위원회 결정문의 상세 정보를 조회합니다."
)
def get_ppc_info(ppc_id: str) -> str:
    """개인정보보호위원회 결정문의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ppc",
        service_type="service",
        ID=ppc_id
    )
    
    filename = f"ppc_info_{ppc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"개인정보보호위원회 결정문 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ftc",
    description="공정거래위원회 결정문을 검색합니다."
)
def search_ftc(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """공정거래위원회 결정문을 검색합니다."""
    data = _make_api_request(
        target="ftc",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"ftc_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"공정거래위원회 결정문 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ftc_info",
    description="특정 공정거래위원회 결정문의 상세 정보를 조회합니다."
)
def get_ftc_info(ftc_id: str) -> str:
    """공정거래위원회 결정문의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ftc",
        service_type="service",
        ID=ftc_id
    )
    
    filename = f"ftc_info_{ftc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"공정거래위원회 결정문 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_eiac",
    description="환경영향평가위원회 결정문을 검색합니다."
)
def search_eiac(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """환경영향평가위원회 결정문을 검색합니다."""
    data = _make_api_request(
        target="eiac",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"eiac_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"환경영향평가위원회 결정문 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_eiac_info",
    description="특정 환경영향평가위원회 결정문의 상세 정보를 조회합니다."
)
def get_eiac_info(eiac_id: str) -> str:
    """환경영향평가위원회 결정문의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="eiac",
        service_type="service",
        ID=eiac_id
    )
    
    filename = f"eiac_info_{eiac_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"환경영향평가위원회 결정문 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_acr",
    description="부패방지권익위원회 결정문을 검색합니다."
)
def search_acr(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """부패방지권익위원회 결정문을 검색합니다."""
    data = _make_api_request(
        target="acr",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"acr_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"부패방지권익위원회 결정문 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_acr_info",
    description="특정 부패방지권익위원회 결정문의 상세 정보를 조회합니다."
)
def get_acr_info(acr_id: str) -> str:
    """부패방지권익위원회 결정문의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="acr",
        service_type="service",
        ID=acr_id
    )
    
    filename = f"acr_info_{acr_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"부패방지권익위원회 결정문 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_fsc",
    description="금융위원회 결정문을 검색합니다."
)
def search_fsc(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """금융위원회 결정문을 검색합니다."""
    data = _make_api_request(
        target="fsc",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"fsc_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"금융위원회 결정문 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_fsc_info",
    description="특정 금융위원회 결정문의 상세 정보를 조회합니다."
)
def get_fsc_info(fsc_id: str) -> str:
    """금융위원회 결정문의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="fsc",
        service_type="service",
        ID=fsc_id
    )
    
    filename = f"fsc_info_{fsc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"금융위원회 결정문 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_nlrc",
    description="노동위원회 결정문을 검색합니다."
)
def search_nlrc(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """노동위원회 결정문을 검색합니다."""
    data = _make_api_request(
        target="nlrc",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"nlrc_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"노동위원회 결정문 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_nlrc_info",
    description="특정 노동위원회 결정문의 상세 정보를 조회합니다."
)
def get_nlrc_info(nlrc_id: str) -> str:
    """노동위원회 결정문의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="nlrc",
        service_type="service",
        ID=nlrc_id
    )
    
    filename = f"nlrc_info_{nlrc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"노동위원회 결정문 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_kcc",
    description="방송통신위원회 결정문을 검색합니다."
)
def search_kcc(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1
) -> str:
    """방송통신위원회 결정문을 검색합니다."""
    data = _make_api_request(
        target="kcc",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page
    )
    
    filename = f"kcc_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"방송통신위원회 결정문 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_kcc_info",
    description="특정 방송통신위원회 결정문의 상세 정보를 조회합니다."
)
def get_kcc_info(kcc_id: str) -> str:
    """방송통신위원회 결정문의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="kcc",
        service_type="service",
        ID=kcc_id
    )
    
    filename = f"kcc_info_{kcc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"방송통신위원회 결정문 상세 정보가 저장되었습니다: {file_path}"

# ===========================================
# 부가서비스 도구들
# ===========================================

@mcp.tool(
    name="search_law_system",
    description="법령 체계도를 검색합니다."
)
def search_law_system(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령 체계도를 검색합니다."""
    data = _make_api_request(
        target="lsStmd",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"law_system_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 체계도 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_law_system_info",
    description="법령 체계도의 상세 정보를 조회합니다."
)
def get_law_system_info(
    law_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """법령 체계도의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="lsStmd",
        service_type="service",
        ID=law_id,
        MST=mst
    )
    
    filename = f"law_system_info_{law_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 체계도 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_old_new_law",
    description="신구법 대조표를 검색합니다."
)
def search_old_new_law(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """신구법 대조표를 검색합니다."""
    data = _make_api_request(
        target="oldAndNew",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"old_new_law_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"신구법 대조표 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_old_new_law_info",
    description="신구법 대조표의 상세 정보를 조회합니다."
)
def get_old_new_law_info(
    law_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """신구법 대조표의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="oldAndNew",
        service_type="service",
        ID=law_id,
        MST=mst
    )
    
    filename = f"old_new_law_info_{law_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"신구법 대조표 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_three_way_comparison",
    description="3단 비교(법률-시행령-시행규칙)를 검색합니다."
)
def search_three_way_comparison(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """3단 비교를 검색합니다."""
    data = _make_api_request(
        target="thdCmp",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"three_way_comparison_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"3단 비교 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_three_way_comparison_info",
    description="3단 비교의 상세 정보를 조회합니다."
)
def get_three_way_comparison_info(
    law_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """3단 비교의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="thdCmp",
        service_type="service",
        ID=law_id,
        MST=mst
    )
    
    filename = f"three_way_comparison_info_{law_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"3단 비교 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_one_view_info",
    description="한눈보기 서비스의 상세 정보를 조회합니다."
)
def get_one_view_info(
    law_id: Optional[str] = None,
    mst: Optional[str] = None
) -> str:
    """한눈보기 서비스의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="oneview",
        service_type="service",
        ID=law_id,
        MST=mst
    )
    
    filename = f"one_view_info_{law_id or mst}"
    file_path = _save_legislation_data(data, filename)
    
    return f"한눈보기 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_abbreviation",
    description="법령 약칭을 검색합니다."
)
def search_law_abbreviation(
    std_dt: Optional[str] = None,
    end_dt: Optional[str] = None
) -> str:
    """법령 약칭을 검색합니다."""
    data = _make_api_request(
        target="lsAbrv",
        service_type="search",
        stdDt=std_dt,
        endDt=end_dt
    )
    
    filename = f"law_abbreviation_search"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 약칭 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_deleted_data",
    description="삭제된 데이터 목록을 조회합니다."
)
def search_deleted_data(
    knd: Optional[int] = None,
    del_dt: Optional[str] = None,
    frm_dt: Optional[str] = None,
    to_dt: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """
    삭제된 데이터 목록을 조회합니다.
    
    Args:
        knd: 데이터 종류 (1=법령, 2=행정규칙, 3=자치법규, 13=학칙공단)
        del_dt: 삭제일자 (YYYYMMDD)
        frm_dt: 검색 시작일 (YYYYMMDD)
        to_dt: 검색 종료일 (YYYYMMDD)
    """
    data = _make_api_request(
        target="delHst",
        service_type="search",
        knd=knd,
        delDt=del_dt,
        frmDt=frm_dt,
        toDt=to_dt,
        display=display,
        page=page
    )
    
    filename = f"deleted_data_search_{knd or 'all'}"
    file_path = _save_legislation_data(data, filename)
    
    return f"삭제된 데이터 목록이 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_one_view",
    description="한눈보기 서비스를 검색합니다."
)
def search_one_view(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """한눈보기 서비스를 검색합니다."""
    data = _make_api_request(
        target="oneview",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"one_view_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"한눈보기 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 통합 API 검색 도구
# ===========================================

@mcp.tool(
    name="search_all_legislation",
    description="모든 법령 관련 정보를 통합 검색합니다."
)
def search_all_legislation(
    query: str,
    include_law: bool = True,
    include_admrul: bool = True,
    include_ordin: bool = True,
    include_prec: bool = True,
    display: int = 10
) -> str:
    """
    모든 법령 관련 정보를 통합 검색합니다.
    
    Args:
        query: 검색할 키워드
        include_law: 법령 검색 포함 여부
        include_admrul: 행정규칙 검색 포함 여부
        include_ordin: 자치법규 검색 포함 여부
        include_prec: 판례 검색 포함 여부
        display: 각 카테고리별 결과 수
    """
    results: Dict[str, Any] = {"query": query, "results": {}}
    
    if include_law:
        law_data = _make_api_request(
            target="law",
            service_type="search",
            query=query,
            display=display
        )
        results["results"]["law"] = law_data
    
    if include_admrul:
        admrul_data = _make_api_request(
            target="admrul",
            service_type="search", 
            query=query,
            display=display
        )
        results["results"]["admrul"] = admrul_data
    
    if include_ordin:
        ordin_data = _make_api_request(
            target="ordin",
            service_type="search",
            query=query,
            display=display
        )
        results["results"]["ordin"] = ordin_data
    
    if include_prec:
        prec_data = _make_api_request(
            target="prec",
            service_type="search",
            query=query,
            display=display
        )
        results["results"]["prec"] = prec_data
    
    filename = f"all_legislation_search_{query}"
    file_path = _save_legislation_data(results, filename)
    
    return f"통합 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 고급 분석 도구
# ===========================================

@mcp.tool(
    name="analyze_law_changes",
    description="특정 법령의 변경 이력을 분석합니다."
)
def analyze_law_changes(
    law_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    특정 법령의 변경 이력을 분석합니다.
    
    Args:
        law_name: 분석할 법령명
        start_date: 시작일 (YYYYMMDD)
        end_date: 종료일 (YYYYMMDD)
    """
    # 1. 법령 기본 정보 조회
    law_data = _make_api_request(
        target="law",
        service_type="search",
        query=law_name
    )
    
    # 2. 변경 이력 조회
    if start_date and end_date:
        date_range = f"{start_date}~{end_date}"
    else:
        date_range = None
        
    history_data = _make_api_request(
        target="lsHstInf",
        service_type="search",
        query=law_name,
        ancYd=date_range
    )
    
    # 3. 신구법 대조 조회
    old_new_data = _make_api_request(
        target="oldAndNew",
        service_type="search",
        query=law_name
    )
    
    analysis_result = {
        "law_name": law_name,
        "search_period": f"{start_date} ~ {end_date}" if start_date and end_date else "전체",
        "basic_info": law_data,
        "change_history": history_data,
        "old_new_comparison": old_new_data,
        "analysis_summary": {
            "total_changes": len(history_data.get("items", [])) if isinstance(history_data.get("items"), list) else 0,
            "has_old_new_comparison": bool(old_new_data.get("items"))
        }
    }
    
    filename = f"law_changes_analysis_{law_name}_{start_date or 'all'}"
    file_path = _save_legislation_data(analysis_result, filename)
    
    return f"법령 변경 이력 분석 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_legislation_statistics",
    description="법령 통계 정보를 조회합니다."
)
def get_legislation_statistics(
    target_date: Optional[str] = None
) -> str:
    """
    법령 통계 정보를 조회합니다.
    
    Args:
        target_date: 기준일 (YYYYMMDD, 생략시 전체)
    """
    statistics = {"target_date": target_date or "전체", "statistics": {}}
    
    # 각 카테고리별 통계 수집
    categories = [
        ("law", "현행법령"),
        ("admrul", "행정규칙"),
        ("ordin", "자치법규"),
        ("prec", "판례"),
        ("detc", "헌재결정례"),
        ("expc", "법령해석례"),
        ("decc", "행정심판례"),
        ("trty", "조약")
    ]
    
    for target, name in categories:
        try:
            params: Dict[str, Any] = {"display": 1}  # 최소한의 결과만 가져와서 총 개수 확인
            if target_date and target in ["law", "admrul", "ordin"]:
                params["date"] = target_date
                
            data = _make_api_request(
                target=target,
                service_type="search",
                **params
            )
            
            total_count = data.get("totalCnt", 0) if isinstance(data, dict) else 0
            stat_info = {
                "total_count": total_count,
                "category": target
            }
            stats_dict = statistics["statistics"]
            if isinstance(stats_dict, dict):
                stats_dict[name] = stat_info
        except Exception as e:
            error_info = {
                "total_count": "조회 실패",
                "error": str(e)
            }
            stats_dict = statistics["statistics"]
            if isinstance(stats_dict, dict):
                stats_dict[name] = error_info
    
    filename = f"legislation_statistics_{target_date or 'all'}"
    file_path = _save_legislation_data(statistics, filename)
    
    return f"법령 통계 정보가 저장되었습니다: {file_path}"

# ===========================================
# 부가서비스 추가 도구 (6개)
# ===========================================

@mcp.tool(
    name="search_law_system_list",
    description="법령 체계 목록을 검색합니다."
)
def search_law_system_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1,
    org: Optional[str] = None
) -> str:
    """법령 체계 목록을 검색합니다."""
    data = _make_api_request(
        target="lsStmd",
        service_type="search",
        query=query,
        display=display,
        page=page,
        org=org
    )
    
    filename = f"law_system_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 체계 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_old_new_comparison_list",
    description="신구법 비교 목록을 검색합니다."
)
def search_old_new_comparison_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1,
    org: Optional[str] = None
) -> str:
    """신구법 비교 목록을 검색합니다."""
    data = _make_api_request(
        target="oldAndNew",
        service_type="search",
        query=query,
        display=display,
        page=page,
        org=org
    )
    
    filename = f"old_new_comparison_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"신구법 비교 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_three_way_comparison_list",
    description="3단 비교 목록을 검색합니다."
)
def search_three_way_comparison_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1,
    org: Optional[str] = None
) -> str:
    """3단 비교 목록을 검색합니다."""
    data = _make_api_request(
        target="thdCmp",
        service_type="search",
        query=query,
        display=display,
        page=page,
        org=org
    )
    
    filename = f"three_way_comparison_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"3단 비교 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_abbreviation_list",
    description="법령명 약칭 목록을 검색합니다."
)
def search_law_abbreviation_list(
    std_dt: Optional[str] = None,
    end_dt: Optional[str] = None
) -> str:
    """법령명 약칭 목록을 검색합니다."""
    data = _make_api_request(
        target="lsAbrv",
        service_type="search",
        stdDt=std_dt,
        endDt=end_dt
    )
    
    filename = f"law_abbreviation_search_{std_dt or 'all'}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령명 약칭 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_deleted_data_history",
    description="삭제된 데이터 이력을 검색합니다."
)
def search_deleted_data_history(
    knd: Optional[int] = None,
    del_dt: Optional[str] = None,
    frm_dt: Optional[str] = None,
    to_dt: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """삭제된 데이터 이력을 검색합니다."""
    data = _make_api_request(
        target="datDel",
        service_type="search",
        knd=knd,
        delDt=del_dt,
        frmDt=frm_dt,
        toDt=to_dt,
        display=display,
        page=page
    )
    
    filename = f"deleted_data_history_{del_dt or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"삭제된 데이터 이력 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_one_view_list",
    description="한눈보기 목록을 검색합니다."
)
def search_one_view_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """한눈보기 목록을 검색합니다."""
    data = _make_api_request(
        target="oneview",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"one_view_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"한눈보기 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 조약 관련 도구 (2개)
# ===========================================

@mcp.tool(
    name="search_treaty",
    description="조약 목록을 검색합니다."
)
def search_treaty(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1,
    sort: str = "lasc"
) -> str:
    """조약 목록을 검색합니다."""
    data = _make_api_request(
        target="treaty",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page,
        sort=sort
    )
    
    filename = f"treaty_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"조약 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_treaty_info",
    description="특정 조약의 상세 정보를 조회합니다."
)
def get_treaty_info(treaty_id: str) -> str:
    """조약의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="treaty",
        service_type="service",
        ID=treaty_id
    )
    
    filename = f"treaty_info_{treaty_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"조약 상세 정보가 저장되었습니다: {file_path}"

# ===========================================
# 별표서식 관련 도구 (4개)
# ===========================================

@mcp.tool(
    name="search_bylaws_forms",
    description="별표서식 목록을 검색합니다."
)
def search_bylaws_forms(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1,
    knd: Optional[str] = None,
    org: Optional[str] = None
) -> str:
    """별표서식 목록을 검색합니다."""
    data = _make_api_request(
        target="byhwpf",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page,
        knd=knd,
        org=org
    )
    
    filename = f"bylaws_forms_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"별표서식 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_bylaws_forms_info",
    description="특정 별표서식의 상세 정보를 조회합니다."
)
def get_bylaws_forms_info(form_id: str) -> str:
    """별표서식의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="byhwpf",
        service_type="service",
        ID=form_id
    )
    
    filename = f"bylaws_forms_info_{form_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"별표서식 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_bylaws_forms",
    description="법령 별표서식을 검색합니다."
)
def search_law_bylaws_forms(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1,
    org: Optional[str] = None
) -> str:
    """법령 별표서식을 검색합니다."""
    data = _make_api_request(
        target="byhwpf",
        service_type="search",
        query=query,
        display=display,
        page=page,
        org=org
    )
    
    filename = f"law_bylaws_forms_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 별표서식 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_law_bylaws_forms_info",
    description="특정 법령 별표서식의 상세 정보를 조회합니다."
)
def get_law_bylaws_forms_info(form_id: str) -> str:
    """법령 별표서식의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="byhwpf",
        service_type="service",
        ID=form_id
    )
    
    filename = f"law_bylaws_forms_info_{form_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 별표서식 상세 정보가 저장되었습니다: {file_path}"

# ===========================================
# 학칙공단 관련 도구 (2개)
# ===========================================

@mcp.tool(
    name="search_school_regulations",
    description="학칙공단 규정을 검색합니다."
)
def search_school_regulations(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1,
    org: Optional[str] = None
) -> str:
    """학칙공단 규정을 검색합니다."""
    data = _make_api_request(
        target="unirule",
        service_type="search",
        query=query,
        search=search_type,
        display=display,
        page=page,
        org=org
    )
    
    filename = f"school_regulations_search_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"학칙공단 규정 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_school_regulations_info",
    description="특정 학칙공단 규정의 상세 정보를 조회합니다."
)
def get_school_regulations_info(regulation_id: str) -> str:
    """학칙공단 규정의 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="unirule",
        service_type="service",
        ID=regulation_id
    )
    
    filename = f"school_regulations_info_{regulation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"학칙공단 규정 상세 정보가 저장되었습니다: {file_path}"

# ===========================================
# 모바일 관련 도구 (15개)
# ===========================================

@mcp.tool(
    name="search_mobile_law_list",
    description="모바일 법령 목록을 검색합니다."
)
def search_mobile_law_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """모바일 법령 목록을 검색합니다."""
    data = _make_api_request(
        target="mobileLawList",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"mobile_law_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 법령 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_mobile_law_info",
    description="모바일 법령 상세 정보를 조회합니다."
)
def get_mobile_law_info(law_id: str) -> str:
    """모바일 법령 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="mobileLawInfo",
        service_type="service",
        ID=law_id
    )
    
    filename = f"mobile_law_info_{law_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 법령 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_mobile_admrul_list",
    description="모바일 행정규칙 목록을 검색합니다."
)
def search_mobile_admrul_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """모바일 행정규칙 목록을 검색합니다."""
    data = _make_api_request(
        target="mobileAdmrulList",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"mobile_admrul_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 행정규칙 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_mobile_admrul_info",
    description="모바일 행정규칙 상세 정보를 조회합니다."
)
def get_mobile_admrul_info(admrul_id: str) -> str:
    """모바일 행정규칙 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="mobileAdmrulInfo",
        service_type="service",
        ID=admrul_id
    )
    
    filename = f"mobile_admrul_info_{admrul_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 행정규칙 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_mobile_ordin_list",
    description="모바일 자치법규 목록을 검색합니다."
)
def search_mobile_ordin_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """모바일 자치법규 목록을 검색합니다."""
    data = _make_api_request(
        target="mobileOrdinList",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"mobile_ordin_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 자치법규 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_mobile_ordin_info",
    description="모바일 자치법규 상세 정보를 조회합니다."
)
def get_mobile_ordin_info(ordin_id: str) -> str:
    """모바일 자치법규 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="mobileOrdinInfo",
        service_type="service",
        ID=ordin_id
    )
    
    filename = f"mobile_ordin_info_{ordin_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 자치법규 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_mobile_prec_list",
    description="모바일 판례 목록을 검색합니다."
)
def search_mobile_prec_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """모바일 판례 목록을 검색합니다."""
    data = _make_api_request(
        target="mobilePrecList",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"mobile_prec_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 판례 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_mobile_prec_info",
    description="모바일 판례 상세 정보를 조회합니다."
)
def get_mobile_prec_info(prec_id: str) -> str:
    """모바일 판례 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="mobilePrecInfo",
        service_type="service",
        ID=prec_id
    )
    
    filename = f"mobile_prec_info_{prec_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 판례 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_mobile_treaty_list",
    description="모바일 조약 목록을 검색합니다."
)
def search_mobile_treaty_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """모바일 조약 목록을 검색합니다."""
    data = _make_api_request(
        target="mobileTreatyList",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"mobile_treaty_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 조약 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_mobile_treaty_info",
    description="모바일 조약 상세 정보를 조회합니다."
)
def get_mobile_treaty_info(treaty_id: str) -> str:
    """모바일 조약 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="mobileTreatyInfo",
        service_type="service",
        ID=treaty_id
    )
    
    filename = f"mobile_treaty_info_{treaty_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 조약 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_mobile_expc_list",
    description="모바일 헌법재판소 결정례 목록을 검색합니다."
)
def search_mobile_expc_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """모바일 헌법재판소 결정례 목록을 검색합니다."""
    data = _make_api_request(
        target="mobileExpcList",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"mobile_expc_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 헌법재판소 결정례 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_mobile_expc_info",
    description="모바일 헌법재판소 결정례 상세 정보를 조회합니다."
)
def get_mobile_expc_info(expc_id: str) -> str:
    """모바일 헌법재판소 결정례 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="mobileExpcInfo",
        service_type="service",
        ID=expc_id
    )
    
    filename = f"mobile_expc_info_{expc_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 헌법재판소 결정례 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_mobile_committee_list",
    description="모바일 위원회결정문 목록을 검색합니다."
)
def search_mobile_committee_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """모바일 위원회결정문 목록을 검색합니다."""
    data = _make_api_request(
        target="mobileCommitteeList",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"mobile_committee_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 위원회결정문 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_mobile_committee_info",
    description="모바일 위원회결정문 상세 정보를 조회합니다."
)
def get_mobile_committee_info(committee_id: str) -> str:
    """모바일 위원회결정문 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="mobileCommitteeInfo",
        service_type="service",
        ID=committee_id
    )
    
    filename = f"mobile_committee_info_{committee_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"모바일 위원회결정문 상세 정보가 저장되었습니다: {file_path}"

# ===========================================
# 맞춤형 관련 도구 (6개)
# ===========================================

@mcp.tool(
    name="search_custom_law_service",
    description="맞춤형 법령 서비스를 검색합니다."
)
def search_custom_law_service(
    query: Optional[str] = None,
    service_type: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 법령 서비스를 검색합니다."""
    data = _make_api_request(
        target="customLaw",
        service_type="search",
        query=query,
        serviceType=service_type,
        display=display,
        page=page
    )
    
    filename = f"custom_law_service_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 법령 서비스 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_custom_law_service_info",
    description="맞춤형 법령 서비스 상세 정보를 조회합니다."
)
def get_custom_law_service_info(service_id: str) -> str:
    """맞춤형 법령 서비스 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="customLaw",
        service_type="service",
        ID=service_id
    )
    
    filename = f"custom_law_service_info_{service_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 법령 서비스 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_industry_law_service",
    description="업종별 법령 서비스를 검색합니다."
)
def search_industry_law_service(
    industry_code: Optional[str] = None,
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """업종별 법령 서비스를 검색합니다."""
    data = _make_api_request(
        target="industryLaw",
        service_type="search",
        industryCode=industry_code,
        query=query,
        display=display,
        page=page
    )
    
    filename = f"industry_law_service_{industry_code or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"업종별 법령 서비스 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_life_cycle_law_service",
    description="생애주기별 법령 서비스를 검색합니다."
)
def search_life_cycle_law_service(
    life_cycle: Optional[str] = None,
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """생애주기별 법령 서비스를 검색합니다."""
    data = _make_api_request(
        target="lifeCycleLaw",
        service_type="search",
        lifeCycle=life_cycle,
        query=query,
        display=display,
        page=page
    )
    
    filename = f"life_cycle_law_service_{life_cycle or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"생애주기별 법령 서비스 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_theme_law_service",
    description="주제별 법령 서비스를 검색합니다."
)
def search_theme_law_service(
    theme: Optional[str] = None,
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """주제별 법령 서비스를 검색합니다."""
    data = _make_api_request(
        target="themeLaw",
        service_type="search",
        theme=theme,
        query=query,
        display=display,
        page=page
    )
    
    filename = f"theme_law_service_{theme or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"주제별 법령 서비스 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_keyword_law_service",
    description="키워드별 법령 서비스를 검색합니다."
)
def search_keyword_law_service(
    keyword: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """키워드별 법령 서비스를 검색합니다."""
    data = _make_api_request(
        target="keywordLaw",
        service_type="search",
        keyword=keyword,
        display=display,
        page=page
    )
    
    filename = f"keyword_law_service_{keyword or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"키워드별 법령 서비스 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 지식베이스 관련 도구 (6개)
# ===========================================

@mcp.tool(
    name="search_knowledge_law_qa",
    description="법령 지식베이스 Q&A를 검색합니다."
)
def search_knowledge_law_qa(
    query: Optional[str] = None,
    category: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령 지식베이스 Q&A를 검색합니다."""
    data = _make_api_request(
        target="knowledgeQA",
        service_type="search",
        query=query,
        category=category,
        display=display,
        page=page
    )
    
    filename = f"knowledge_law_qa_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 지식베이스 Q&A 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_knowledge_law_qa_info",
    description="법령 지식베이스 Q&A 상세 정보를 조회합니다."
)
def get_knowledge_law_qa_info(qa_id: str) -> str:
    """법령 지식베이스 Q&A 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="knowledgeQA",
        service_type="service",
        ID=qa_id
    )
    
    filename = f"knowledge_law_qa_info_{qa_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 지식베이스 Q&A 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_glossary",
    description="법령 용어사전을 검색합니다."
)
def search_law_glossary(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령 용어사전을 검색합니다."""
    data = _make_api_request(
        target="lawGlossary",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"law_glossary_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 용어사전 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_guide",
    description="법령 가이드를 검색합니다."
)
def search_law_guide(
    query: Optional[str] = None,
    guide_type: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령 가이드를 검색합니다."""
    data = _make_api_request(
        target="lawGuide",
        service_type="search",
        query=query,
        guideType=guide_type,
        display=display,
        page=page
    )
    
    filename = f"law_guide_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 가이드 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_interpretation",
    description="법령 해석례를 검색합니다."
)
def search_law_interpretation(
    query: Optional[str] = None,
    interpretation_type: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령 해석례를 검색합니다."""
    data = _make_api_request(
        target="lawInterpretation",
        service_type="search",
        query=query,
        interpretationType=interpretation_type,
        display=display,
        page=page
    )
    
    filename = f"law_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 해석례 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_law_case_study",
    description="법령 사례집을 검색합니다."
)
def search_law_case_study(
    query: Optional[str] = None,
    case_type: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령 사례집을 검색합니다."""
    data = _make_api_request(
        target="lawCaseStudy",
        service_type="search",
        query=query,
        caseType=case_type,
        display=display,
        page=page
    )
    
    filename = f"law_case_study_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령 사례집 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 기타 관련 도구 (1개)
# ===========================================

@mcp.tool(
    name="search_miscellaneous_law_service",
    description="기타 법령 서비스를 검색합니다."
)
def search_miscellaneous_law_service(
    query: Optional[str] = None,
    service_type: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """기타 법령 서비스를 검색합니다."""
    data = _make_api_request(
        target="miscLaw",
        service_type="search",
        query=query,
        serviceType=service_type,
        display=display,
        page=page
    )
    
    filename = f"miscellaneous_law_service_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"기타 법령 서비스 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 중앙부처해석 관련 도구 (14개)
# ===========================================

@mcp.tool(
    name="search_ministry_interpretation",
    description="중앙부처 법령해석을 검색합니다."
)
def search_ministry_interpretation(
    query: Optional[str] = None,
    ministry_code: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """중앙부처 법령해석을 검색합니다."""
    data = _make_api_request(
        target="ministryInterpretation",
        service_type="search",
        query=query,
        ministryCode=ministry_code,
        display=display,
        page=page
    )
    
    filename = f"ministry_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 법령해석 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ministry_interpretation_info",
    description="중앙부처 법령해석 상세 정보를 조회합니다."
)
def get_ministry_interpretation_info(interpretation_id: str) -> str:
    """중앙부처 법령해석 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ministryInterpretation",
        service_type="service",
        ID=interpretation_id
    )
    
    filename = f"ministry_interpretation_info_{interpretation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 법령해석 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ministry_circular",
    description="중앙부처 훈령을 검색합니다."
)
def search_ministry_circular(
    query: Optional[str] = None,
    ministry_code: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """중앙부처 훈령을 검색합니다."""
    data = _make_api_request(
        target="ministryCircular",
        service_type="search",
        query=query,
        ministryCode=ministry_code,
        display=display,
        page=page
    )
    
    filename = f"ministry_circular_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 훈령 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ministry_circular_info",
    description="중앙부처 훈령 상세 정보를 조회합니다."
)
def get_ministry_circular_info(circular_id: str) -> str:
    """중앙부처 훈령 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ministryCircular",
        service_type="service",
        ID=circular_id
    )
    
    filename = f"ministry_circular_info_{circular_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 훈령 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ministry_notice",
    description="중앙부처 고시를 검색합니다."
)
def search_ministry_notice(
    query: Optional[str] = None,
    ministry_code: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """중앙부처 고시를 검색합니다."""
    data = _make_api_request(
        target="ministryNotice",
        service_type="search",
        query=query,
        ministryCode=ministry_code,
        display=display,
        page=page
    )
    
    filename = f"ministry_notice_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 고시 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ministry_notice_info",
    description="중앙부처 고시 상세 정보를 조회합니다."
)
def get_ministry_notice_info(notice_id: str) -> str:
    """중앙부처 고시 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ministryNotice",
        service_type="service",
        ID=notice_id
    )
    
    filename = f"ministry_notice_info_{notice_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 고시 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ministry_regulation",
    description="중앙부처 예규를 검색합니다."
)
def search_ministry_regulation(
    query: Optional[str] = None,
    ministry_code: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """중앙부처 예규를 검색합니다."""
    data = _make_api_request(
        target="ministryRegulation",
        service_type="search",
        query=query,
        ministryCode=ministry_code,
        display=display,
        page=page
    )
    
    filename = f"ministry_regulation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 예규 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ministry_regulation_info",
    description="중앙부처 예규 상세 정보를 조회합니다."
)
def get_ministry_regulation_info(regulation_id: str) -> str:
    """중앙부처 예규 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ministryRegulation",
        service_type="service",
        ID=regulation_id
    )
    
    filename = f"ministry_regulation_info_{regulation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 예규 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ministry_directive",
    description="중앙부처 지시를 검색합니다."
)
def search_ministry_directive(
    query: Optional[str] = None,
    ministry_code: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """중앙부처 지시를 검색합니다."""
    data = _make_api_request(
        target="ministryDirective",
        service_type="search",
        query=query,
        ministryCode=ministry_code,
        display=display,
        page=page
    )
    
    filename = f"ministry_directive_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 지시 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ministry_directive_info",
    description="중앙부처 지시 상세 정보를 조회합니다."
)
def get_ministry_directive_info(directive_id: str) -> str:
    """중앙부처 지시 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ministryDirective",
        service_type="service",
        ID=directive_id
    )
    
    filename = f"ministry_directive_info_{directive_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 지시 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ministry_guideline",
    description="중앙부처 가이드라인을 검색합니다."
)
def search_ministry_guideline(
    query: Optional[str] = None,
    ministry_code: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """중앙부처 가이드라인을 검색합니다."""
    data = _make_api_request(
        target="ministryGuideline",
        service_type="search",
        query=query,
        ministryCode=ministry_code,
        display=display,
        page=page
    )
    
    filename = f"ministry_guideline_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 가이드라인 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ministry_guideline_info",
    description="중앙부처 가이드라인 상세 정보를 조회합니다."
)
def get_ministry_guideline_info(guideline_id: str) -> str:
    """중앙부처 가이드라인 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ministryGuideline",
        service_type="service",
        ID=guideline_id
    )
    
    filename = f"ministry_guideline_info_{guideline_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 가이드라인 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_ministry_manual",
    description="중앙부처 매뉴얼을 검색합니다."
)
def search_ministry_manual(
    query: Optional[str] = None,
    ministry_code: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """중앙부처 매뉴얼을 검색합니다."""
    data = _make_api_request(
        target="ministryManual",
        service_type="search",
        query=query,
        ministryCode=ministry_code,
        display=display,
        page=page
    )
    
    filename = f"ministry_manual_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 매뉴얼 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_ministry_manual_info",
    description="중앙부처 매뉴얼 상세 정보를 조회합니다."
)
def get_ministry_manual_info(manual_id: str) -> str:
    """중앙부처 매뉴얼 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="ministryManual",
        service_type="service",
        ID=manual_id
    )
    
    filename = f"ministry_manual_info_{manual_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"중앙부처 매뉴얼 상세 정보가 저장되었습니다: {file_path}"

logger.info("119개 법제처 OPEN API 도구가 모두 로드되었습니다!") 
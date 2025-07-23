"""
한국 법제처 OPEN API 146개 완전 통합 MCP 도구

146개의 모든 API를 구현하여 한국의 법령, 행정규칙, 자치법규, 판례, 위원회결정문 등 
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
- 맞춤형 (12개)  
- 지식베이스 (13개)
- 기타 (1개)
- 중앙부처해석 (27개)
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
    description="한국의 모든 현행 법령을 검색합니다. 법령명, 법령번호, 소관부처별 검색이 가능하며, 약 2만여 개의 법률, 대통령령, 부령이 포함됩니다. 법무/법제 연구, 컴플라이언스 검토, 정책 분석에 활용됩니다."
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
    description="특정 법령의 전체 조문과 부칙, 별표를 포함한 상세 본문을 조회합니다. 조항별 내용, 시행일, 제·개정 이력 등 완전한 법령 정보를 제공하여 정확한 법령 해석과 적용을 지원합니다."
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
    description="한국 법령의 공식 영문 번역본을 검색합니다. 국제 계약, 외국인 투자, 글로벌 컴플라이언스 검토 시 필수적이며, 약 400여 개의 주요 법령이 영어로 제공됩니다."
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
    description="특정 시점에 시행되는 법령을 검색합니다. 과거 또는 미래의 특정 날짜에 효력이 있는 법령을 확인할 수 있어, 시간적 적용 범위 분석과 과도기적 법령 적용에 중요합니다."
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
    description="특정 날짜의 법령 제·개정 현황을 조회합니다. 일자별 법령 변화 추적으로 법무팀의 법령 모니터링과 컴플라이언스 업데이트에 필수적이며, 규제 변화에 대한 선제적 대응을 가능하게 합니다."
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
    description="행정기관의 내부 규정인 훈령, 예규, 고시, 지침 등을 검색합니다. 약 8만여 건의 행정규칙으로 실무 운영 기준과 세부 해석 기준을 제공하여 행정업무와 민원 처리의 구체적 기준을 확인할 수 있습니다."
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
    description="특정 행정규칙의 상세 정보를 조회합니다. 훈령, 예규, 고시 등의 전체 조문과 부칙, 제·개정 이력을 포함하여 행정업무의 구체적 운영 기준과 세부 해석 지침을 확인할 수 있습니다."
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
    description="지방자치단체의 조례와 규칙을 검색합니다. 전국 243개 지자체의 약 40만여 건 자치법규로 지역별 특성을 반영한 법규를 확인할 수 있어, 지역 사업과 투자 시 필수적인 정보를 제공합니다."
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
    description="특정 자치법규의 상세 정보를 조회합니다. 지방자치단체별 조례와 규칙의 전체 조문, 부칙, 제·개정 이력을 포함하여 지역별 특성과 정책을 반영한 상세 규정을 확인할 수 있습니다."
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
    description="자치법규와 상위 법령 간의 연계 관계를 조회합니다. 지방자치단체의 조례와 규칙이 어떤 법률이나 시행령을 근거로 제정되었는지 확인하여 법령 체계상의 위치와 권한 범위를 파악할 수 있습니다."
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
    description="대법원과 각급 법원의 판례를 검색합니다. 약 160만여 건의 판례로 법령 해석의 실제 적용례와 법원의 판단 기준을 확인할 수 있어, 법리 연구와 소송 전략 수립에 핵심적인 자료를 제공합니다."
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
    description="헌법재판소의 결정례를 검색합니다. 위헌심판, 헌법소원, 권한쟁의 등 약 3만여 건의 헌재 결정으로 헌법적 쟁점과 기본권 해석의 권위있는 기준을 제공합니다."
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
    description="법제처의 공식 법령해석례를 검색합니다. 약 12만여 건의 해석례로 법령 조문의 구체적 의미와 적용 범위에 대한 정부의 공식 견해를 제공하여 법령 적용의 불확실성을 해소합니다."
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
    description="행정심판례를 검색합니다. 행정청의 위법·부당한 처분에 대한 구제 사례로 행정처분의 적법성 판단 기준과 권리구제 절차를 확인할 수 있어, 행정쟁송과 민원 해결에 실무적 지침을 제공합니다."
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
    description="한국이 체결한 양자·다자 조약과 국제협정을 검색합니다. 약 2천여 건의 조약으로 국제거래, 투자협정, 통상협정의 법적 근거를 확인할 수 있어 국제업무와 해외진출에 필수적인 정보를 제공합니다."
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
    description="법령에서 사용되는 전문용어의 정의와 해석을 검색합니다. 약 4천여 개의 법령용어 사전으로 법률 문서 작성, 계약서 검토, 법령 해석 시 정확한 용어 이해를 지원합니다."
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
    description="개인정보보호위원회의 결정문과 가이드라인을 검색합니다. 개인정보 처리 기준, 위반 사례, 과징금 부과 기준 등을 통해 개인정보보호법 준수와 프라이버시 컴플라이언스 구축에 필수적인 정보를 제공합니다."
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
    description="공정거래위원회 결정문을 검색합니다. 독점금지, 불공정거래행위, 기업결합 제재 사례와 심결 기준을 통해 공정거래법 위반 리스크 파악과 기업 컴플라이언스 체계 구축에 필수적인 정보를 제공합니다."
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
    description="금융위원회 결정문을 검색합니다. 금융업 인허가, 금융소비자 보호, 자본시장 제재 사례와 심결 기준을 통해 금융 규제 준수와 금융업계 컴플라이언스 체계 구축에 필수적인 정보를 제공합니다."
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
    description="중앙노동위원회와 지방노동위원회의 결정문을 검색합니다. 부당해고 구제, 부당노동행위 판정, 노동쟁의 조정 사례 등을 통해 노사관계와 근로자 권익 보호의 실무 기준을 제공합니다."
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
    description="방송통신위원회 결정문을 검색합니다. 방송 심의, 통신 규제, 온라인 플랫폼 제재 사례와 심결 기준을 통해 방송통신 관련 법규 준수와 미디어 컴플라이언스 구축에 필요한 실무 기준을 제공합니다."
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
    description="법령 간의 위계질서와 상호관계를 보여주는 체계도를 검색합니다. 법률-시행령-시행규칙의 구조적 관계와 근거법령을 시각적으로 파악하여 법령 적용의 우선순위와 적용범위를 명확히 이해할 수 있습니다."
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
    description="법령 개정 시 변경된 조문의 신구법 대조표를 검색합니다. 개정 전후 조문을 나란히 비교하여 정확한 변경사항을 파악할 수 있어, 법령 개정이 기존 업무와 계약에 미치는 영향을 정밀하게 분석할 수 있습니다."
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
    description="법률-시행령-시행규칙의 3단계 법령 구조를 통합 비교합니다. 상위법과 하위법간의 위임관계와 구체적 시행 기준을 체계적으로 파악하여 법령 적용의 전체적인 맥락과 실무 적용 방법을 명확히 이해할 수 있습니다."
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
    description="법령, 행정규칙, 자치법규, 판례를 한번에 통합 검색합니다. 키워드로 모든 법령 정보를 횡단검색하여 포괄적인 법적 근거와 관련 정보를 빠르게 파악할 수 있는 원스톱 검색 도구입니다."
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
    description="특정 법령의 제·개정 이력을 시계열로 분석합니다. 법령의 변화 추이, 주요 개정 사항, 정책 방향성을 파악하여 향후 규제 변화 예측과 장기적 컴플라이언스 전략 수립을 지원합니다."
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
    description="전체 법령 현황의 통계적 분석 정보를 제공합니다. 법령 유형별 분포, 제·개정 추이, 소관부처별 현황 등 거시적 관점의 법령 데이터로 정책 연구와 입법 동향 분석에 기초 자료를 제공합니다."
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
    description="모바일 최적화된 간편 법령 정보를 검색합니다. 핵심 법령을 간결하고 직관적인 형태로 제공하여 현장 업무나 이동 중에도 신속한 법령 확인과 즉시 적용이 가능합니다."
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
    display: int = 20,
    page: int = 1
) -> str:
    """기타 법령 서비스를 검색합니다."""
    data = _make_api_request(
        target="miscellaneousLaw",
        service_type="search",
        query=query,
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

# ===========================================
# 중앙부처별 법령해석 관련 도구 (14개)
# ===========================================

@mcp.tool(
    name="search_customs_interpretation",
    description="관세청 법령해석을 검색합니다. 관세 및 무역 관련 법령의 구체적 해석과 적용 기준을 제공하여 수출입 업무와 관세 정책에 대한 정확한 이해를 지원합니다."
)
def search_customs_interpretation(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """관세청 법령해석을 검색합니다."""
    data = _make_api_request(
        target="kcsCgmExpc",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"customs_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"관세청 법령해석 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_customs_interpretation_info",
    description="관세청 법령해석 상세 정보를 조회합니다."
)
def get_customs_interpretation_info(interpretation_id: str) -> str:
    """관세청 법령해석 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="kcsCgmExpc",
        service_type="service",
        ID=interpretation_id
    )
    
    filename = f"customs_interpretation_info_{interpretation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"관세청 법령해석 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_environment_interpretation",
    description="환경부 법령해석을 검색합니다. 환경 규제와 오염 방지 관련 법령의 해석을 통해 환경법 준수와 환경영향평가에 필요한 기준을 제공합니다."
)
def search_environment_interpretation(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """환경부 법령해석을 검색합니다."""
    data = _make_api_request(
        target="meCgmExpc",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"environment_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"환경부 법령해석 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_environment_interpretation_info",
    description="환경부 법령해석 상세 정보를 조회합니다."
)
def get_environment_interpretation_info(interpretation_id: str) -> str:
    """환경부 법령해석 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="meCgmExpc",
        service_type="service",
        ID=interpretation_id
    )
    
    filename = f"environment_interpretation_info_{interpretation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"환경부 법령해석 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_finance_interpretation",
    description="기획재정부 법령해석을 검색합니다. 경제정책, 재정관리, 예산 관련 법령의 해석을 통해 경제 활동과 재정 정책에 대한 명확한 기준을 제공합니다."
)
def search_finance_interpretation(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """기획재정부 법령해석을 검색합니다."""
    data = _make_api_request(
        target="moefCgmExpc",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"finance_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"기획재정부 법령해석 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_labor_interpretation",
    description="고용노동부 법령해석을 검색합니다. 근로기준법, 산업안전보건법 등 노동 관련 법령의 해석을 통해 근로자 권익과 기업의 노무 관리에 필요한 기준을 제공합니다."
)
def search_labor_interpretation(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """고용노동부 법령해석을 검색합니다."""
    data = _make_api_request(
        target="moelCgmExpc",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"labor_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"고용노동부 법령해석 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_labor_interpretation_info",
    description="고용노동부 법령해석 상세 정보를 조회합니다."
)
def get_labor_interpretation_info(interpretation_id: str) -> str:
    """고용노동부 법령해석 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="moelCgmExpc",
        service_type="service",
        ID=interpretation_id
    )
    
    filename = f"labor_interpretation_info_{interpretation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"고용노동부 법령해석 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_maritime_interpretation",
    description="해양수산부 법령해석을 검색합니다. 항만, 어업, 해운 관련 법령의 해석을 통해 해양 산업과 수산업 정책에 대한 정확한 기준을 제공합니다."
)
def search_maritime_interpretation(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """해양수산부 법령해석을 검색합니다."""
    data = _make_api_request(
        target="mofCgmExpc",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"maritime_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"해양수산부 법령해석 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_maritime_interpretation_info",
    description="해양수산부 법령해석 상세 정보를 조회합니다."
)
def get_maritime_interpretation_info(interpretation_id: str) -> str:
    """해양수산부 법령해석 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="mofCgmExpc",
        service_type="service",
        ID=interpretation_id
    )
    
    filename = f"maritime_interpretation_info_{interpretation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"해양수산부 법령해석 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_public_safety_interpretation",
    description="행정안전부 법령해석을 검색합니다. 행정절차, 지방자치, 재해안전 관련 법령의 해석을 통해 공공행정과 안전관리에 필요한 기준을 제공합니다."
)
def search_public_safety_interpretation(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """행정안전부 법령해석을 검색합니다."""
    data = _make_api_request(
        target="moisCgmExpc",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"public_safety_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정안전부 법령해석 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_public_safety_interpretation_info",
    description="행정안전부 법령해석 상세 정보를 조회합니다."
)
def get_public_safety_interpretation_info(interpretation_id: str) -> str:
    """행정안전부 법령해석 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="moisCgmExpc",
        service_type="service",
        ID=interpretation_id
    )
    
    filename = f"public_safety_interpretation_info_{interpretation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정안전부 법령해석 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_transport_interpretation",
    description="국토교통부 법령해석을 검색합니다. 건설, 교통, 도시계획 관련 법령의 해석을 통해 건설업계와 교통정책에 필요한 구체적 기준을 제공합니다."
)
def search_transport_interpretation(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """국토교통부 법령해석을 검색합니다."""
    data = _make_api_request(
        target="molitCgmExpc",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"transport_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"국토교통부 법령해석 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="get_transport_interpretation_info",
    description="국토교통부 법령해석 상세 정보를 조회합니다."
)
def get_transport_interpretation_info(interpretation_id: str) -> str:
    """국토교통부 법령해석 상세 정보를 조회합니다."""
    data = _make_api_request(
        target="molitCgmExpc",
        service_type="service",
        ID=interpretation_id
    )
    
    filename = f"transport_interpretation_info_{interpretation_id}"
    file_path = _save_legislation_data(data, filename)
    
    return f"국토교통부 법령해석 상세 정보가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_tax_interpretation",
    description="국세청 법령해석을 검색합니다. 세법의 구체적 해석과 적용 기준을 통해 세무 신고, 과세 처분, 조세 정책에 대한 정확한 이해를 지원합니다."
)
def search_tax_interpretation(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """국세청 법령해석을 검색합니다."""
    data = _make_api_request(
        target="ntsCgmExpc",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"tax_interpretation_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"국세청 법령해석 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 법령정보지식베이스 관련 도구 (7개)
# ===========================================

@mcp.tool(
    name="search_legal_term_ai",
    description="AI 기반 법령용어를 검색합니다. 법령에서 사용되는 전문용어의 정의와 동음이의어를 구분하여 정확한 법령 해석과 문서 작성을 지원합니다."
)
def search_legal_term_ai(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1,
    homonym: Optional[str] = None
) -> str:
    """AI 기반 법령용어를 검색합니다."""
    data = _make_api_request(
        target="lstrmAI",
        service_type="search",
        query=query,
        display=display,
        page=page,
        homonymYn=homonym
    )
    
    filename = f"legal_term_ai_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"AI 기반 법령용어 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_daily_term",
    description="일상용어를 검색합니다. 법령용어와 연계된 일반적인 용어를 찾아 법령의 내용을 쉽게 이해할 수 있도록 지원합니다."
)
def search_daily_term(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """일상용어를 검색합니다."""
    data = _make_api_request(
        target="dlytrm",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"daily_term_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"일상용어 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_legal_term_relation",
    description="법령용어와 일상용어 간의 연계 관계를 검색합니다. 동의어, 반의어, 상하위어 등의 관계를 통해 용어의 정확한 의미를 파악할 수 있습니다."
)
def search_legal_term_relation(
    query: Optional[str] = None,
    mst: Optional[str] = None,
    relation_code: Optional[int] = None
) -> str:
    """법령용어-일상용어 연계를 검색합니다."""
    data = _make_api_request(
        target="lstrmRlt",
        service_type="service",
        query=query,
        MST=mst,
        trmRltCd=relation_code
    )
    
    filename = f"legal_term_relation_{query or mst or 'all'}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령용어 연계 관계 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_daily_term_relation",
    description="일상용어와 법령용어 간의 연계 관계를 검색합니다. 일반적인 용어에서 시작하여 관련된 법령용어를 찾을 수 있습니다."
)
def search_daily_term_relation(
    query: Optional[str] = None,
    mst: Optional[str] = None,
    relation_code: Optional[int] = None
) -> str:
    """일상용어-법령용어 연계를 검색합니다."""
    data = _make_api_request(
        target="dlytrmRlt",
        service_type="service",
        query=query,
        MST=mst,
        trmRltCd=relation_code
    )
    
    filename = f"daily_term_relation_{query or mst or 'all'}"
    file_path = _save_legislation_data(data, filename)
    
    return f"일상용어 연계 관계 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_legal_term_article_relation",
    description="법령용어와 조문 간의 연계 관계를 검색합니다. 특정 용어가 어떤 법령의 어떤 조문에서 사용되는지 확인할 수 있습니다."
)
def search_legal_term_article_relation(
    query: str
) -> str:
    """법령용어-조문 연계를 검색합니다."""
    data = _make_api_request(
        target="lstrmRltJo",
        service_type="service",
        query=query
    )
    
    filename = f"legal_term_article_relation_{query}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령용어-조문 연계 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_article_legal_term_relation",
    description="조문과 법령용어 간의 연계 관계를 검색합니다. 특정 조문에서 사용되는 법령용어들을 확인할 수 있습니다."
)
def search_article_legal_term_relation(
    query: str
) -> str:
    """조문-법령용어 연계를 검색합니다."""
    data = _make_api_request(
        target="joRltLstrm",
        service_type="service",
        query=query
    )
    
    filename = f"article_legal_term_relation_{query}"
    file_path = _save_legislation_data(data, filename)
    
    return f"조문-법령용어 연계 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_related_legislation",
    description="관련 법령 간의 연계 관계를 검색합니다. 특정 법령과 관련된 다른 법령들을 찾아 법령 체계의 전체적인 구조를 파악할 수 있습니다."
)
def search_related_legislation(
    query: Optional[str] = None,
    law_id: Optional[int] = None,
    relation_code: Optional[int] = None
) -> str:
    """관련 법령을 검색합니다."""
    data = _make_api_request(
        target="lsRlt",
        service_type="search",
        query=query,
        ID=law_id,
        lsRltCd=relation_code
    )
    
    filename = f"related_legislation_{query or law_id or 'all'}"
    file_path = _save_legislation_data(data, filename)
    
    return f"관련 법령 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 맞춤형 법령서비스 관련 도구 (6개)
# ===========================================

@mcp.tool(
    name="search_custom_law_list",
    description="맞춤형 법령 목록을 검색합니다. 특정 분야나 주제별로 분류된 법령을 효율적으로 찾을 수 있어 업무 영역별 전문적인 법령 검토를 지원합니다."
)
def search_custom_law_list(
    classification_code: str,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 법령 목록을 검색합니다."""
    data = _make_api_request(
        target="couseLs",
        service_type="search",
        vcode=classification_code,
        display=display,
        page=page
    )
    
    filename = f"custom_law_list_{classification_code}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 법령 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_custom_law_article_list",
    description="맞춤형 법령 조문 목록을 검색합니다. 특정 분야의 법령에서 중요한 조문들만 선별하여 제공함으로써 핵심 규정을 빠르게 파악할 수 있습니다."
)
def search_custom_law_article_list(
    classification_code: str,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 법령 조문 목록을 검색합니다."""
    data = _make_api_request(
        target="couseLs",
        service_type="search",
        vcode=classification_code,
        lj="jo",
        display=display,
        page=page
    )
    
    filename = f"custom_law_article_list_{classification_code}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 법령 조문 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_custom_admrul_list",
    description="맞춤형 행정규칙 목록을 검색합니다. 특정 분야의 행정규칙을 분류별로 체계화하여 제공함으로써 실무에 필요한 세부 기준을 효율적으로 확인할 수 있습니다."
)
def search_custom_admrul_list(
    classification_code: str,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 행정규칙 목록을 검색합니다."""
    data = _make_api_request(
        target="couseAdmrul",
        service_type="search",
        vcode=classification_code,
        display=display,
        page=page
    )
    
    filename = f"custom_admrul_list_{classification_code}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 행정규칙 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_custom_admrul_article_list",
    description="맞춤형 행정규칙 조문 목록을 검색합니다. 특정 분야의 행정규칙에서 핵심적인 조문들을 선별하여 실무 적용에 필요한 구체적 기준을 제공합니다."
)
def search_custom_admrul_article_list(
    classification_code: str,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 행정규칙 조문 목록을 검색합니다."""
    data = _make_api_request(
        target="couseAdmrul",
        service_type="search",
        vcode=classification_code,
        lj="jo",
        display=display,
        page=page
    )
    
    filename = f"custom_admrul_article_list_{classification_code}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 행정규칙 조문 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_custom_ordinance_list",
    description="맞춤형 자치법규 목록을 검색합니다. 지역별·분야별로 분류된 자치법규를 체계적으로 제공하여 지방자치단체별 특화된 규정을 효과적으로 파악할 수 있습니다."
)
def search_custom_ordinance_list(
    classification_code: str,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 자치법규 목록을 검색합니다."""
    data = _make_api_request(
        target="couseOrdin",
        service_type="search",
        vcode=classification_code,
        display=display,
        page=page
    )
    
    filename = f"custom_ordinance_list_{classification_code}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 자치법규 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_custom_ordinance_article_list",
    description="맞춤형 자치법규 조문 목록을 검색합니다. 특정 분야의 자치법규에서 중요한 조문들을 선별하여 지역 특성에 맞는 핵심 규정을 빠르게 확인할 수 있습니다."
)
def search_custom_ordinance_article_list(
    classification_code: str,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 자치법규 조문 목록을 검색합니다."""
    data = _make_api_request(
        target="couseOrdin",
        service_type="search",
        vcode=classification_code,
        lj="jo",
        display=display,
        page=page
    )
    
    filename = f"custom_ordinance_article_list_{classification_code}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 자치법규 조문 목록 검색 결과가 저장되었습니다: {file_path}"

# ===========================================
# 추가 누락된 API들 구현 (새롭게 추가된 API만)
# ===========================================

@mcp.tool(
    name="search_customs_interpretation_list",
    description="관세청 법령해석 목록을 검색합니다."
)
def search_customs_interpretation_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """관세청 법령해석 목록을 검색합니다."""
    data = _make_api_request(
        target="cgmExpcKcs",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"customs_interpretation_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"관세청 법령해석 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_environment_interpretation_list",
    description="환경부 법령해석 목록을 검색합니다."
)
def search_environment_interpretation_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """환경부 법령해석 목록을 검색합니다."""
    data = _make_api_request(
        target="cgmExpcMe",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"environment_interpretation_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"환경부 법령해석 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_finance_interpretation_list",
    description="기획재정부 법령해석 목록을 검색합니다."
)
def search_finance_interpretation_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """기획재정부 법령해석 목록을 검색합니다."""
    data = _make_api_request(
        target="cgmExpcMoef",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"finance_interpretation_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"기획재정부 법령해석 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_labor_interpretation_list",
    description="고용노동부 법령해석 목록을 검색합니다."
)
def search_labor_interpretation_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """고용노동부 법령해석 목록을 검색합니다."""
    data = _make_api_request(
        target="cgmExpcMoel",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"labor_interpretation_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"고용노동부 법령해석 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_maritime_interpretation_list",
    description="해양수산부 법령해석 목록을 검색합니다."
)
def search_maritime_interpretation_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """해양수산부 법령해석 목록을 검색합니다."""
    data = _make_api_request(
        target="cgmExpcMof",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"maritime_interpretation_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"해양수산부 법령해석 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_interior_interpretation_list",
    description="행정안전부 법령해석 목록을 검색합니다."
)
def search_interior_interpretation_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """행정안전부 법령해석 목록을 검색합니다."""
    data = _make_api_request(
        target="cgmExpcMois",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"interior_interpretation_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"행정안전부 법령해석 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_transport_interpretation_list",
    description="국토교통부 법령해석 목록을 검색합니다."
)
def search_transport_interpretation_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """국토교통부 법령해석 목록을 검색합니다."""
    data = _make_api_request(
        target="cgmExpcMolit",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"transport_interpretation_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"국토교통부 법령해석 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_tax_interpretation_list",
    description="국세청 법령해석 목록을 검색합니다."
)
def search_tax_interpretation_list(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """국세청 법령해석 목록을 검색합니다."""
    data = _make_api_request(
        target="cgmExpcNts",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"tax_interpretation_list_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"국세청 법령해석 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_custom_administrative_rule_article_list",
    description="맞춤형 행정규칙 조문 목록을 검색합니다."
)
def search_custom_administrative_rule_article_list(
    classification_code: str,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 행정규칙 조문 목록을 검색합니다."""
    data = _make_api_request(
        target="custAdmrul",
        service_type="search",
        vcode=classification_code,
        lj="jo",
        display=display,
        page=page
    )
    
    filename = f"custom_admin_rule_article_list_{classification_code}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 행정규칙 조문 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_custom_administrative_rule_list",
    description="맞춤형 행정규칙 목록을 검색합니다."
)
def search_custom_administrative_rule_list(
    classification_code: str,
    display: int = 20,
    page: int = 1
) -> str:
    """맞춤형 행정규칙 목록을 검색합니다."""
    data = _make_api_request(
        target="custAdmrul",
        service_type="search",
        vcode=classification_code,
        display=display,
        page=page
    )
    
    filename = f"custom_admin_rule_list_{classification_code}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"맞춤형 행정규칙 목록 검색 결과가 저장되었습니다: {file_path}"

@mcp.tool(
    name="search_legal_term_relation_article",
    description="법령용어 연계 조문을 검색합니다."
)
def search_legal_term_relation_article(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> str:
    """법령용어 연계 조문을 검색합니다."""
    data = _make_api_request(
        target="lstrmRltJo",
        service_type="search",
        query=query,
        display=display,
        page=page
    )
    
    filename = f"legal_term_relation_article_{query or 'all'}_{page}"
    file_path = _save_legislation_data(data, filename)
    
    return f"법령용어 연계 조문 검색 결과가 저장되었습니다: {file_path}"

logger.info("146개 법제처 OPEN API 도구가 모두 로드되었습니다!") 
"""
한국 법제처 OPEN API 추가 도구 (Part 3)

중앙부처해석 API와 기타 누락된 API들을 구현
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
# 중앙부처해석 상세 조회 API들
# ===========================================

@mcp.tool(name="get_moef_interpretation_detail", description="기획재정부 법령해석 상세내용을 조회합니다.")
def get_moef_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """기획재정부 법령해석 본문 조회"""
    params = {"target": "moefCgmExpc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moefCgmExpc", params)
        result = _format_search_results(data, "moefCgmExpc", f"해석ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 기획재정부 법령해석 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_molit_interpretation_detail", description="국토교통부 법령해석 상세내용을 조회합니다.")
def get_molit_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """국토교통부 법령해석 본문 조회"""
    params = {"target": "molitCgmExpc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("molitCgmExpc", params)
        result = _format_search_results(data, "molitCgmExpc", f"해석ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 국토교통부 법령해석 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_moel_interpretation_detail", description="고용노동부 법령해석 상세내용을 조회합니다.")
def get_moel_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """고용노동부 법령해석 본문 조회"""
    params = {"target": "moelCgmExpc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moelCgmExpc", params)
        result = _format_search_results(data, "moelCgmExpc", f"해석ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 고용노동부 법령해석 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mof_interpretation_detail", description="해양수산부 법령해석 상세내용을 조회합니다.")
def get_mof_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """해양수산부 법령해석 본문 조회"""
    params = {"target": "mofCgmExpc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("mofCgmExpc", params)
        result = _format_search_results(data, "mofCgmExpc", f"해석ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 해양수산부 법령해석 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mohw_interpretation_detail", description="보건복지부 법령해석 상세내용을 조회합니다.")
def get_mohw_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """보건복지부 법령해석 본문 조회"""
    params = {"target": "mohwCgmExpc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("mohwCgmExpc", params)
        result = _format_search_results(data, "mohwCgmExpc", f"해석ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 보건복지부 법령해석 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_moe_interpretation_detail", description="교육부 법령해석 상세내용을 조회합니다.")
def get_moe_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """교육부 법령해석 본문 조회"""
    params = {"target": "moeCgmExpc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moeCgmExpc", params)
        result = _format_search_results(data, "moeCgmExpc", f"해석ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 교육부 법령해석 상세 조회 중 오류: {str(e)}")

# ===========================================
# 추가 중앙부처해석 API들
# ===========================================

@mcp.tool(name="search_mois_interpretation", description="행정안전부 법령해석을 검색합니다.")
def search_mois_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """행정안전부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "moisCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("moisCgmExpc", params)
        result = _format_search_results(data, "moisCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정안전부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="get_mois_interpretation_detail", description="행정안전부 법령해석 상세내용을 조회합니다.")
def get_mois_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """행정안전부 법령해석 본문 조회"""
    params = {"target": "moisCgmExpc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moisCgmExpc", params)
        result = _format_search_results(data, "moisCgmExpc", f"해석ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정안전부 법령해석 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_me_interpretation", description="환경부 법령해석을 검색합니다.")
def search_me_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """환경부 법령해석 검색"""
    search_query = query or "환경보호"
    params = {"target": "meCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("meCgmExpc", params)
        result = _format_search_results(data, "meCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 환경부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="get_me_interpretation_detail", description="환경부 법령해석 상세내용을 조회합니다.")
def get_me_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """환경부 법령해석 본문 조회"""
    params = {"target": "meCgmExpc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("meCgmExpc", params)
        result = _format_search_results(data, "meCgmExpc", f"해석ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 환경부 법령해석 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_kicogm_interpretation", description="한국산업인력공단 법령해석을 검색합니다.")
def search_kicogm_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """한국산업인력공단 법령해석 검색"""
    search_query = query or "산업인력"
    params = {"target": "kicoCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("kicoCgmExpc", params)
        result = _format_search_results(data, "kicoCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 한국산업인력공단 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_kcg_interpretation", description="해양경찰청 법령해석을 검색합니다.")
def search_kcg_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """해양경찰청 법령해석 검색"""
    search_query = query or "해양경찰"
    params = {"target": "kcgCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("kcgCgmExpc", params)
        result = _format_search_results(data, "kcgCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 해양경찰청 법령해석 검색 중 오류: {str(e)}")

# ===========================================
# 연계 법령 API들
# ===========================================

@mcp.tool(name="search_linked_law_by_ordinance", description="조례별 연계 법령을 검색합니다. 특정 조례와 관련된 상위 법령을 조회할 수 있습니다.")
def search_linked_law_by_ordinance(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """조례별 연계 법령 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "lnkLsOrd", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lnkLsOrd", params)
        result = _format_search_results(data, "lnkLsOrd", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 조례별 연계 법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_linked_law_by_ministry", description="소관부처별 연계 법령을 검색합니다. 특정 부처가 관할하는 법령들을 조회할 수 있습니다.")
def search_linked_law_by_ministry(org: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """소관부처별 연계 법령 검색"""
    params = {"target": "lnkOrg", "display": min(display, 100), "page": page}
    if org:
        params["org"] = org
    try:
        data = _make_legislation_request("lnkOrg", params)
        result = _format_search_results(data, "lnkOrg", f"소관부처:{org}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 소관부처별 연계 법령 검색 중 오류: {str(e)}")

# ===========================================
# 모바일 API 추가들
# ===========================================

@mcp.tool(name="get_mobile_law_detail", description="모바일 법령 상세내용을 조회합니다. 모바일 기기에 최적화된 법령 본문을 제공합니다.")
def get_mobile_law_detail(law_id: Union[str, int]) -> TextContent:
    """모바일 법령 본문 조회"""
    params = {"target": "law", "ID": str(law_id), "mobileYn": "Y"}
    try:
        data = _make_legislation_request("law", params)
        result = _format_search_results(data, "law", f"모바일법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 법령 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_english_law_detail", description="모바일 영문법령 상세내용을 조회합니다.")
def get_mobile_english_law_detail(law_id: Union[str, int]) -> TextContent:
    """모바일 영문법령 본문 조회"""
    params = {"target": "englaw", "ID": str(law_id), "mobileYn": "Y"}
    try:
        data = _make_legislation_request("englaw", params)
        result = _format_search_results(data, "englaw", f"모바일영문법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 영문법령 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_administrative_rule_detail", description="모바일 행정규칙 상세내용을 조회합니다.")
def get_mobile_administrative_rule_detail(rule_id: Union[str, int]) -> TextContent:
    """모바일 행정규칙 본문 조회"""
    params = {"target": "admrul", "ID": str(rule_id), "mobileYn": "Y"}
    try:
        data = _make_legislation_request("admrul", params)
        result = _format_search_results(data, "admrul", f"모바일행정규칙ID:{rule_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 행정규칙 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_local_ordinance_detail", description="모바일 자치법규 상세내용을 조회합니다.")
def get_mobile_local_ordinance_detail(ordinance_id: Union[str, int]) -> TextContent:
    """모바일 자치법규 본문 조회"""
    params = {"target": "ordin", "ID": str(ordinance_id), "mobileYn": "Y"}
    try:
        data = _make_legislation_request("ordin", params)
        result = _format_search_results(data, "ordin", f"모바일자치법규ID:{ordinance_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 자치법규 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_precedent_detail", description="모바일 판례 상세내용을 조회합니다.")
def get_mobile_precedent_detail(case_id: Union[str, int]) -> TextContent:
    """모바일 판례 본문 조회"""
    params = {"target": "prec", "ID": str(case_id), "mobileYn": "Y"}
    try:
        data = _make_legislation_request("prec", params)
        result = _format_search_results(data, "prec", f"모바일판례ID:{case_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 판례 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_treaty_detail", description="모바일 조약 상세내용을 조회합니다.")
def get_mobile_treaty_detail(treaty_id: Union[str, int]) -> TextContent:
    """모바일 조약 본문 조회"""
    params = {"target": "trty", "ID": str(treaty_id), "mobileYn": "Y"}
    try:
        data = _make_legislation_request("trty", params)
        result = _format_search_results(data, "trty", f"모바일조약ID:{treaty_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 조약 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_law_appendix_detail", description="모바일 법령 별표서식 상세내용을 조회합니다.")
def get_mobile_law_appendix_detail(appendix_id: Union[str, int]) -> TextContent:
    """모바일 법령 별표서식 본문 조회"""
    params = {"target": "licbyl", "ID": str(appendix_id), "mobileYn": "Y"}
    try:
        data = _make_legislation_request("licbyl", params)
        result = _format_search_results(data, "licbyl", f"모바일별표서식ID:{appendix_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 법령 별표서식 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_legal_term_detail", description="모바일 법령용어 상세내용을 조회합니다.")
def get_mobile_legal_term_detail(term_id: Union[str, int]) -> TextContent:
    """모바일 법령용어 본문 조회"""
    params = {"target": "lstrm", "ID": str(term_id), "mobileYn": "Y"}
    try:
        data = _make_legislation_request("lstrm", params)
        result = _format_search_results(data, "lstrm", f"모바일용어ID:{term_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 법령용어 상세 조회 중 오류: {str(e)}")

# ===========================================
# 지식베이스 상세 조회 API들
# ===========================================

@mcp.tool(name="get_legal_ai_detail", description="법령 AI 지식베이스 상세내용을 조회합니다.")
def get_legal_ai_detail(ai_id: Union[str, int]) -> TextContent:
    """법령 AI 지식베이스 본문 조회"""
    params = {"target": "lstrmAI", "ID": str(ai_id)}
    try:
        data = _make_legislation_request("lstrmAI", params)
        result = _format_search_results(data, "lstrmAI", f"AI지식베이스ID:{ai_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 AI 지식베이스 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_knowledge_base_detail", description="지식베이스 상세내용을 조회합니다.")
def get_knowledge_base_detail(knowledge_id: Union[str, int]) -> TextContent:
    """지식베이스 본문 조회"""
    params = {"target": "knowledge", "ID": str(knowledge_id)}
    try:
        data = _make_legislation_request("knowledge", params)
        result = _format_search_results(data, "knowledge", f"지식베이스ID:{knowledge_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 지식베이스 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_faq_detail", description="FAQ 상세내용을 조회합니다.")
def get_faq_detail(faq_id: Union[str, int]) -> TextContent:
    """FAQ 본문 조회"""
    params = {"target": "faq", "ID": str(faq_id)}
    try:
        data = _make_legislation_request("faq", params)
        result = _format_search_results(data, "faq", f"FAQ ID:{faq_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ FAQ 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_qna_detail", description="질의응답 상세내용을 조회합니다.")
def get_qna_detail(qna_id: Union[str, int]) -> TextContent:
    """질의응답 본문 조회"""
    params = {"target": "qna", "ID": str(qna_id)}
    try:
        data = _make_legislation_request("qna", params)
        result = _format_search_results(data, "qna", f"QnA ID:{qna_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 질의응답 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_counsel_detail", description="상담 상세내용을 조회합니다.")
def get_counsel_detail(counsel_id: Union[str, int]) -> TextContent:
    """상담 본문 조회"""
    params = {"target": "counsel", "ID": str(counsel_id)}
    try:
        data = _make_legislation_request("counsel", params)
        result = _format_search_results(data, "counsel", f"상담ID:{counsel_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 상담 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_precedent_counsel_detail", description="판례 상담 상세내용을 조회합니다.")
def get_precedent_counsel_detail(counsel_id: Union[str, int]) -> TextContent:
    """판례 상담 본문 조회"""
    params = {"target": "precCounsel", "ID": str(counsel_id)}
    try:
        data = _make_legislation_request("precCounsel", params)
        result = _format_search_results(data, "precCounsel", f"판례상담ID:{counsel_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 판례 상담 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_civil_petition_detail", description="민원 상세내용을 조회합니다.")
def get_civil_petition_detail(petition_id: Union[str, int]) -> TextContent:
    """민원 본문 조회"""
    params = {"target": "minwon", "ID": str(petition_id)}
    try:
        data = _make_legislation_request("minwon", params)
        result = _format_search_results(data, "minwon", f"민원ID:{petition_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 민원 상세 조회 중 오류: {str(e)}")

logger.info("✅ 추가 중앙부처해석 및 상세조회 API 도구들이 로드되었습니다!") 
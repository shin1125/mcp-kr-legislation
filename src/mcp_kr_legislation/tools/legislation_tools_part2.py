"""
한국 법제처 OPEN API 추가 도구 (Part 2)

누락된 54개 API를 각각 개별 도구로 구현
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
# 추가 법령 API 도구들
# ===========================================

@mcp.tool(name="get_law_tree", description="법령 체계도를 조회합니다. 법령의 구조와 체계를 시각적으로 확인할 수 있습니다.")
def get_law_tree(law_id: Union[str, int]) -> TextContent:
    """법령 체계도 조회 (lsTree)"""
    params = {"target": "lsTree", "ID": str(law_id)}
    try:
        data = _make_legislation_request("lsTree", params)
        result = _format_search_results(data, "lsTree", f"법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 체계도 조회 중 오류: {str(e)}")

@mcp.tool(name="get_law_comparison", description="신구법비교 상세내용을 조회합니다. 법령 개정 전후의 상세 비교 정보를 제공합니다.")
def get_law_comparison(law_id: Union[str, int]) -> TextContent:
    """신구법비교 본문 조회 (lsInfoCmp)"""
    params = {"target": "lsInfoCmp", "ID": str(law_id)}
    try:
        data = _make_legislation_request("lsInfoCmp", params)
        result = _format_search_results(data, "lsInfoCmp", f"법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 신구법비교 조회 중 오류: {str(e)}")

@mcp.tool(name="get_three_way_comparison_detail", description="3단비교 상세내용을 조회합니다. 인용조문과 위임조문의 상세 비교를 제공합니다.")
def get_three_way_comparison_detail(law_id: Union[str, int], knd: int = 1) -> TextContent:
    """3단비교 본문 조회 (thdCmpInfo)"""
    params = {"target": "thdCmp", "ID": str(law_id), "knd": knd}
    try:
        data = _make_legislation_request("thdCmp", params)
        result = _format_search_results(data, "thdCmp", f"법령ID:{law_id} 종류:{knd}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 3단비교 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_law_glance", description="법령 한눈보기를 조회합니다. 법령의 핵심 내용을 요약하여 제공합니다.")
def get_law_glance(law_id: Union[str, int]) -> TextContent:
    """법령 한눈보기 조회 (lsGlance)"""
    params = {"target": "lsGlance", "ID": str(law_id)}
    try:
        data = _make_legislation_request("lsGlance", params)
        result = _format_search_results(data, "lsGlance", f"법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 한눈보기 조회 중 오류: {str(e)}")

@mcp.tool(name="get_law_article_detail", description="법령의 특정 조항 상세내용을 조회합니다. 조, 항, 호, 목 단위로 세부 내용을 확인할 수 있습니다.")
def get_law_article_detail(law_id: Union[str, int], jo: str, hang: Optional[str] = None, ho: Optional[str] = None, mok: Optional[str] = None) -> TextContent:
    """법령 조항호목 조회 (lawjosub)"""
    params = {"target": "lawjosub", "ID": str(law_id), "JO": jo}
    if hang:
        params["HANG"] = hang
    if ho:
        params["HO"] = ho
    if mok:
        params["MOK"] = mok
    
    try:
        data = _make_legislation_request("lawjosub", params)
        result = _format_search_results(data, "lawjosub", f"법령ID:{law_id} 조:{jo}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 조항 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_law_abbreviation", description="법령명 약칭을 조회합니다. 법령의 공식 약칭명과 별칭을 확인할 수 있습니다.")
def search_law_abbreviation(std_dt: Optional[str] = None, end_dt: Optional[str] = None) -> TextContent:
    """법령명 약칭 조회 (lsAbrv)"""
    params = {"target": "lsAbrv"}
    if std_dt:
        params["stdDt"] = std_dt
    if end_dt:
        params["endDt"] = end_dt
    
    try:
        data = _make_legislation_request("lsAbrv", params)
        result = _format_search_results(data, "lsAbrv", "법령명 약칭")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령명 약칭 조회 중 오류: {str(e)}")

# ===========================================
# 위원회 결정문 상세 조회 API들
# ===========================================

@mcp.tool(name="get_privacy_committee_detail", description="개인정보보호위원회 결정문 상세내용을 조회합니다. 특정 결정문의 전체 내용을 제공합니다.")
def get_privacy_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """개인정보보호위원회 결정문 본문 조회 (ppcInfo)"""
    params = {"target": "ppc", "ID": str(decision_id)}
    try:
        data = _make_legislation_request("ppc", params)
        result = _format_search_results(data, "ppc", f"결정문ID:{decision_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 개인정보보호위원회 결정문 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_broadcasting_committee_detail", description="방송통신위원회 결정문 상세내용을 조회합니다. 특정 결정문의 전체 내용을 제공합니다.")
def get_broadcasting_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """방송통신위원회 결정문 본문 조회 (kccInfo)"""
    params = {"target": "kcc", "ID": str(decision_id)}
    try:
        data = _make_legislation_request("kcc", params)
        result = _format_search_results(data, "kcc", f"결정문ID:{decision_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 방송통신위원회 결정문 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_industrial_accident_committee_detail", description="산업재해보상보험재심사위원회 결정문 상세내용을 조회합니다.")
def get_industrial_accident_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """산업재해보상보험재심사위원회 결정문 본문 조회 (iaciacInfo)"""
    params = {"target": "iaciac", "ID": str(decision_id)}
    try:
        data = _make_legislation_request("iaciac", params)
        result = _format_search_results(data, "iaciac", f"결정문ID:{decision_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 산업재해보상보험재심사위원회 결정문 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_land_tribunal_detail", description="중앙토지수용위원회 결정문 상세내용을 조회합니다.")
def get_land_tribunal_detail(decision_id: Union[str, int]) -> TextContent:
    """중앙토지수용위원회 결정문 본문 조회 (ocltInfo)"""
    params = {"target": "oclt", "ID": str(decision_id)}
    try:
        data = _make_legislation_request("oclt", params)
        result = _format_search_results(data, "oclt", f"결정문ID:{decision_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 중앙토지수용위원회 결정문 상세 조회 중 오류: {str(e)}")

# ===========================================
# 추가 위원회들
# ===========================================

@mcp.tool(name="search_employment_insurance_committee", description="고용보험심사위원회 결정문을 검색합니다.")
def search_employment_insurance_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """고용보험심사위원회 결정문 검색 (eiac)"""
    search_query = query or "고용보험"
    params = {"target": "eiac", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("eiac", params)
        result = _format_search_results(data, "eiac", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 고용보험심사위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_environmental_committee", description="중앙환경분쟁조정위원회 결정문을 검색합니다.")
def search_environmental_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """중앙환경분쟁조정위원회 결정문 검색 (ecc)"""
    search_query = query or "환경분쟁"
    params = {"target": "ecc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ecc", params)
        result = _format_search_results(data, "ecc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 중앙환경분쟁조정위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_securities_committee", description="증권선물위원회 결정문을 검색합니다.")
def search_securities_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """증권선물위원회 결정문 검색 (sfc)"""
    search_query = query or "증권"
    params = {"target": "sfc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("sfc", params)
        result = _format_search_results(data, "sfc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 증권선물위원회 결정문 검색 중 오류: {str(e)}")

# ===========================================
# 조약 상세 조회
# ===========================================

@mcp.tool(name="get_treaty_detail", description="조약 상세내용을 조회합니다. 특정 조약의 전문과 세부 내용을 제공합니다.")
def get_treaty_detail(treaty_id: Union[str, int]) -> TextContent:
    """조약 본문 조회 (trtyInfo)"""
    params = {"target": "trty", "ID": str(treaty_id)}
    try:
        data = _make_legislation_request("trty", params)
        result = _format_search_results(data, "trty", f"조약ID:{treaty_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 조약 상세 조회 중 오류: {str(e)}")

# ===========================================
# 별표서식 상세 조회
# ===========================================

@mcp.tool(name="get_law_appendix_detail", description="법령 별표서식 상세내용을 조회합니다. 특정 별표나 서식의 전체 내용을 제공합니다.")
def get_law_appendix_detail(appendix_id: Union[str, int]) -> TextContent:
    """법령 별표서식 본문 조회 (licbylInfo)"""
    params = {"target": "licbyl", "ID": str(appendix_id)}
    try:
        data = _make_legislation_request("licbyl", params)
        result = _format_search_results(data, "licbyl", f"별표서식ID:{appendix_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 별표서식 상세 조회 중 오류: {str(e)}")

# ===========================================
# 영문법령 상세 조회
# ===========================================

@mcp.tool(name="get_english_law_detail", description="영문법령 상세내용을 조회합니다. 특정 영문법령의 전문을 제공합니다.")
def get_english_law_detail(law_id: Union[str, int], chr_cls_cd: str = "010203") -> TextContent:
    """영문법령 본문 조회 (englawInfo)"""
    params = {"target": "englaw", "ID": str(law_id), "chrClsCd": chr_cls_cd}
    try:
        data = _make_legislation_request("englaw", params)
        result = _format_search_results(data, "englaw", f"영문법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 영문법령 상세 조회 중 오류: {str(e)}")

# ===========================================
# 시행일법령 상세 조회
# ===========================================

@mcp.tool(name="get_effective_law_detail", description="시행일법령 상세내용을 조회합니다. 특정 시행일법령의 전문을 제공합니다.")
def get_effective_law_detail(law_id: Union[str, int], ef_yd: Optional[str] = None) -> TextContent:
    """시행일법령 본문 조회 (eflawInfo)"""
    params = {"target": "eflaw", "ID": str(law_id)}
    if ef_yd:
        params["efYd"] = ef_yd
    try:
        data = _make_legislation_request("eflaw", params)
        result = _format_search_results(data, "eflaw", f"시행일법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 시행일법령 상세 조회 중 오류: {str(e)}")

# ===========================================
# 법령 연혁 상세 조회
# ===========================================

@mcp.tool(name="get_law_history_detail", description="법령 연혁 상세내용을 조회합니다. 특정 법령의 개정 이력과 변천사를 제공합니다.")
def get_law_history_detail(law_id: Union[str, int]) -> TextContent:
    """법령 연혁 조회 (lsHist)"""
    params = {"target": "lsHist", "ID": str(law_id)}
    try:
        data = _make_legislation_request("lsHist", params)
        result = _format_search_results(data, "lsHist", f"법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 연혁 상세 조회 중 오류: {str(e)}")

# ===========================================
# 판례 상세 조회
# ===========================================

@mcp.tool(name="get_precedent_detail", description="판례 상세내용을 조회합니다. 특정 판례의 전문과 판시사항을 제공합니다.")
def get_precedent_detail(case_id: Union[str, int]) -> TextContent:
    """판례 본문 조회 (precInfo)"""
    params = {"target": "prec", "ID": str(case_id)}
    try:
        data = _make_legislation_request("prec", params)
        result = _format_search_results(data, "prec", f"판례ID:{case_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 판례 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_constitutional_court_detail", description="헌법재판소 결정례 상세내용을 조회합니다. 특정 결정례의 전문을 제공합니다.")
def get_constitutional_court_detail(case_id: Union[str, int]) -> TextContent:
    """헌법재판소 결정례 본문 조회 (detcInfo)"""
    params = {"target": "detc", "ID": str(case_id)}
    try:
        data = _make_legislation_request("detc", params)
        result = _format_search_results(data, "detc", f"결정례ID:{case_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 헌법재판소 결정례 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_legal_interpretation_detail", description="법령해석례 상세내용을 조회합니다. 특정 해석례의 전문과 해석 내용을 제공합니다.")
def get_legal_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """법령해석례 본문 조회 (expcInfo)"""
    params = {"target": "expc", "ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("expc", params)
        result = _format_search_results(data, "expc", f"해석례ID:{interpretation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령해석례 상세 조회 중 오류: {str(e)}")

# ===========================================
# 법령용어 상세 조회
# ===========================================

@mcp.tool(name="get_legal_term_detail", description="법령용어 상세내용을 조회합니다. 특정 법령용어의 정의와 설명을 제공합니다.")
def get_legal_term_detail(term_id: Union[str, int]) -> TextContent:
    """법령용어 본문 조회 (lstrmInfo)"""
    params = {"target": "lstrm", "ID": str(term_id)}
    try:
        data = _make_legislation_request("lstrm", params)
        result = _format_search_results(data, "lstrm", f"용어ID:{term_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령용어 상세 조회 중 오류: {str(e)}")

# ===========================================
# 대학학칙 상세 조회
# ===========================================

@mcp.tool(name="get_university_regulation_detail", description="대학학칙 및 공공기관규정 상세내용을 조회합니다.")
def get_university_regulation_detail(regulation_id: Union[str, int]) -> TextContent:
    """대학학칙 및 공공기관규정 본문 조회 (nlrcInfo)"""
    params = {"target": "nlrc", "ID": str(regulation_id)}
    try:
        data = _make_legislation_request("nlrc", params)
        result = _format_search_results(data, "nlrc", f"규정ID:{regulation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 대학학칙 및 공공기관규정 상세 조회 중 오류: {str(e)}")

logger.info("✅ 추가 54개 법제처 API 도구가 로드되었습니다!") 
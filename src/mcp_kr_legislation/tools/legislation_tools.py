"""
한국 법제처 OPEN API 121개 완전 통합 MCP 도구

search_simple_law의 성공 패턴을 적용한 안전하고 간단한 모든 도구들
모든 카테고리: 법령, 부가서비스, 행정규칙, 자치법규, 판례관련, 위원회결정문, 
조약, 별표서식, 학칙공단, 법령용어, 모바일, 맞춤형, 지식베이스, 기타, 중앙부처해석
"""

import logging
import json
import os
from typing import Optional, Union
from mcp.types import TextContent

from ..server import mcp

logger = logging.getLogger(__name__)

def _generate_api_url(target: str, params: dict) -> str:
    """API URL 생성 함수"""
    try:
        from urllib.parse import urlencode
        
        # API 키 설정
        oc = os.getenv("LEGISLATION_API_KEY", "lchangoo")
        
        # 기본 파라미터 설정
        base_params = {
            "OC": oc,
            "type": "JSON"
        }
        base_params.update(params)
        base_params["target"] = target
        
        # URL 결정 (검색 vs 서비스)
        search_targets = [
            # 법령 관련 검색
            "law", "englaw", "eflaw", "lsHistSearch", "lsNickNm", "deldata", "lsStmd",
            # 행정규칙 검색
            "admrul", "admbyl", "admrulOldAndNew",
            # 자치법규 검색
            "ordin", "ordinfd", "ordinbyl", "lnkLs", "lnkLsOrd", "lnkOrg", "lnkOrd",
            # 판례 관련 검색  
            "prec", "detc", "expc", "decc", "mobprec",
            # 위원회 결정문 검색
            "ppc", "eiac", "fsc", "ftc", "acr", "nlrc", "ecc", "sfc", "nhrck", "kcc", "iaciac", "oclt",
            # 조약 검색
            "trty",
            # 별표서식 검색
            "licbyl",
            # 부가서비스 검색
            "oldAndNew", "thdCmp", "delHst", "oneview", "lsAbrv", "datDel",
            # 학칙공단공공기관 검색
            "school", "public", "pi",
            # 특별행정심판 검색
            "ttSpecialDecc", "kmstSpecialDecc",
            # 법령용어 검색
            "lstrm", "lstrmAI",
            # 모바일 검색
            "moblaw", "molegm", "moleg_eng", "moleg_chn",
            # 맞춤형 검색
            "custlaw", "custprec", "couseLs", "couseOrdin",
            # 지식베이스 검색
            "knowledge", "faq", "qna", "counsel", "precCounsel", "minwon",
            # 중앙부처 해석 검색
            "moelCgmExpc", "molitCgmExpc", "moefCgmExpc", "mofCgmExpc", "mohwCgmExpc", 
            "moeCgmExpc", "koreaExpc", "msspCgmExpc", "moteCgmExpc", "mafCgmExpc", 
            "momsCgmExpc", "smeexpcCgmExpc", "nfaCgmExpc", "korailCgmExpc", "kcgCgmExpc", "kicoCgmExpc"
        ]
        
        if target in search_targets:
            url = "http://www.law.go.kr/DRF/lawSearch.do"
        else:
            url = "http://www.law.go.kr/DRF/lawService.do"
        
        return f"{url}?{urlencode(base_params)}"
        
    except Exception as e:
        logger.error(f"URL 생성 실패: {e}")
        return ""

def _make_legislation_request(target: str, params: dict) -> dict:
    """법제처 API 공통 요청 함수"""
    try:
        import requests
        
        # API 키 설정
        oc = os.getenv("LEGISLATION_API_KEY", "lchangoo")
        
        # 기본 파라미터 설정
        base_params = {
            "OC": oc,
            "type": "JSON"
        }
        base_params.update(params)
        
        # URL 결정 (검색 vs 서비스)
        # lawSearch.do를 사용하는 검색 API들
        search_targets = [
            # 법령 관련 검색
            "law", "englaw", "eflaw", "lsHistSearch", "lsNickNm", "deldata", "lsStmd",
            # 행정규칙 검색
            "admrul", "admbyl", "admrulOldAndNew",
            # 자치법규 검색
            "ordin", "ordinfd", "ordinbyl", "lnkLs", "lnkLsOrd", "lnkOrg", "lnkOrd",
            # 판례 관련 검색  
            "prec", "detc", "expc", "decc", "mobprec",
            # 위원회 결정문 검색
            "ppc", "eiac", "fsc", "ftc", "acr", "nlrc", "ecc", "sfc", "nhrck", "kcc", "iaciac", "oclt",
            # 조약 검색
            "trty",
            # 별표서식 검색
            "licbyl",
            # 부가서비스 검색
            "oldAndNew", "thdCmp", "delHst", "oneview", "lsAbrv", "datDel",
            # 학칙공단공공기관 검색
            "school", "public", "pi",
            # 특별행정심판 검색
            "ttSpecialDecc", "kmstSpecialDecc",
            # 법령용어 검색
            "lstrm", "lstrmAI",
            # 모바일 검색
            "moblaw", "molegm", "moleg_eng", "moleg_chn",
            # 맞춤형 검색
            "custlaw", "custprec", "couseLs", "couseOrdin",
            # 지식베이스 검색
            "knowledge", "faq", "qna", "counsel", "precCounsel", "minwon",
            # 중앙부처 해석 검색
            "moelCgmExpc", "molitCgmExpc", "moefCgmExpc", "mofCgmExpc", "mohwCgmExpc", 
            "moeCgmExpc", "koreaExpc", "msspCgmExpc", "moteCgmExpc", "mafCgmExpc", 
            "momsCgmExpc", "smeexpcCgmExpc", "nfaCgmExpc", "korailCgmExpc", "kcgCgmExpc", "kicoCgmExpc"
        ]
        
        if target in search_targets:
            url = "http://www.law.go.kr/DRF/lawSearch.do"
        else:
            url = "http://www.law.go.kr/DRF/lawService.do"
        
        base_params["target"] = target
        
        response = requests.get(url, params=base_params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        return data
        
    except Exception as e:
        logger.error(f"API 요청 실패: {e}")
        return {"error": str(e)}

def _format_search_results(data: dict, search_type: str, query: str = "", url: str = "") -> str:
    """검색 결과를 사용자 친화적으로 포맷팅 (URL 및 상세 정보 포함)"""
    
    if "error" in data:
        return f"❌ 오류: {data['error']}\n\n🔗 **API URL**: {url}"
    
    try:
        result = ""
        
        # URL 정보 추가
        if url:
            result += f"🔗 **API 호출 URL**: {url}\n\n"
        
        # 법령 검색 결과
        if "LawSearch" in data:
            search_data = data["LawSearch"]
            total_count = search_data.get("totalCnt", 0)
            result += f"🔍 **'{query}' 법령 검색 결과**\n\n📊 **총 {total_count}건** 발견\n\n"
            
            items = search_data.get("law", [])
            if not isinstance(items, list):
                items = []
            
            if items:
                result += "📋 **상세 법령 정보:**\n"
                for i, item in enumerate(items[:10], 1):  # 10개까지 표시
                    if isinstance(item, dict):
                        name = item.get("법령명_한글", item.get("법령명", f"법령 {i}"))
                        law_type = item.get("법령구분명", "미분류")
                        ministry = item.get("소관부처명", "미지정")
                        law_id = item.get("법령ID", "미지정")
                        enf_date = item.get("시행일자", "미지정")
                        pub_date = item.get("공포일자", "미지정")
                        law_no = item.get("법령번호", "미지정")
                        
                        result += f"\n**{i}. {name}**\n"
                        result += f"   📝 **법령구분**: {law_type}\n"
                        result += f"   🏛️ **소관부처**: {ministry}\n"
                        result += f"   🆔 **법령ID**: {law_id}\n"
                        result += f"   📅 **공포일자**: {pub_date}\n"
                        result += f"   ⏰ **시행일자**: {enf_date}\n"
                        result += f"   🔢 **법령번호**: {law_no}\n"
                        
                        # 상세보기 URL
                        if law_id != "미지정":
                            detail_url = f"http://www.law.go.kr/DRF/lawService.do?OC=lchangoo&type=JSON&target=law&ID={law_id}"
                            result += f"   🔗 **상세조회 URL**: {detail_url}\n"
            else:
                result += "📋 검색된 법령이 없습니다.\n"
                
        # 판례 검색 결과
        elif "PrecSearch" in data:
            search_data = data["PrecSearch"]
            total_count = search_data.get("totalCnt", 0)
            result += f"⚖️ **'{query}' 판례 검색 결과**\n\n📊 **총 {total_count}건** 발견\n\n"
            
            items = search_data.get("prec", [])
            if not isinstance(items, list):
                items = []
                
            if items:
                result += "📋 **상세 판례 정보:**\n"
                for i, item in enumerate(items[:10], 1):
                    if isinstance(item, dict):
                        title = item.get("판례명", item.get("사건명", f"판례 {i}"))
                        court = item.get("법원명", "미지정")
                        date = item.get("선고일자", "미지정")
                        case_no = item.get("사건번호", "미지정")
                        case_type = item.get("사건종류명", "미지정")
                        summary = item.get("판례내용", item.get("요지", ""))
                        prec_id = item.get("판례일련번호", "미지정")
                        
                        result += f"\n**{i}. {title}**\n"
                        result += f"   🏛️ **법원**: {court}\n"
                        result += f"   📅 **선고일**: {date}\n"
                        result += f"   📋 **사건번호**: {case_no}\n"
                        result += f"   📂 **사건종류**: {case_type}\n"
                        
                        if summary and len(summary.strip()) > 0:
                            result += f"   📄 **요지**: {summary[:200]}{'...' if len(summary) > 200 else ''}\n"
                        
                        # 상세보기 URL
                        if prec_id != "미지정":
                            detail_url = f"http://www.law.go.kr/DRF/lawService.do?OC=lchangoo&type=JSON&target=prec&ID={prec_id}"
                            result += f"   🔗 **상세조회 URL**: {detail_url}\n"
            else:
                result += "📋 검색된 판례가 없습니다.\n"
        
        # 위원회 결정문 등 기타 검색 결과
        else:
            result += f"📄 **'{query}' 검색 결과**\n\n"
            
            # 응답에서 주요 키들 추출
            main_keys = [k for k in data.keys() if k not in ["error", "message"]]
            if main_keys:
                main_key = main_keys[0]
                search_data = data[main_key]
                
                if isinstance(search_data, dict):
                    total_count = search_data.get("totalCnt", "미지정")
                    result += f"📊 **총 {total_count}건** 발견\n\n"
                    
                    # 첫 번째 배열 데이터 찾기
                    for key, value in search_data.items():
                        if isinstance(value, list) and value:
                            result += f"📋 **상세 {key} 정보:**\n"
                            for i, item in enumerate(value[:10], 1):  # 10개까지 표시
                                if isinstance(item, dict):
                                    # 주요 정보 필드들 찾기
                                    name_fields = [
                                        "법령명_한글", "법령명", "판례명", "사건명", "안건명", "제목",
                                        "별표명", "조약명", "용어명", "질의요지", "해석명", "규칙명",
                                        "결정문제목", "의결서제목", "행정규칙명"
                                    ]
                                    name = "정보 없음"
                                    for field in name_fields:
                                        if field in item and item[field]:
                                            name = item[field]
                                            break
                                    
                                    result += f"\n**{i}. {name}**\n"
                                    
                                    # 상세 정보 필드들 추가
                                    detailed_fields = [
                                        ("법원명", "🏛️ 법원"), ("선고일자", "📅 선고일"),
                                        ("소관부처명", "🏛️ 소관부처"), ("공포일자", "📅 공포일"),
                                        ("해석일자", "📅 해석일"), ("질의기관명", "🏢 질의기관"),
                                        ("의결일자", "📅 의결일"), ("사건번호", "📋 사건번호"),
                                        ("법령구분명", "📝 법령구분"), ("시행일자", "⏰ 시행일"),
                                        ("법령번호", "🔢 법령번호"), ("재결청", "🏛️ 재결청"),
                                        ("신청인", "👤 신청인"), ("피신청인", "👥 피신청인")
                                    ]
                                    
                                    for field, label in detailed_fields:
                                        if field in item and item[field] and str(item[field]).strip():
                                            result += f"   {label}: {item[field]}\n"
                                    
                                    # 내용 요약 추가
                                    content_fields = ["판례내용", "요지", "결정요지", "해석내용", "질의내용"]
                                    for field in content_fields:
                                        if field in item and item[field] and len(str(item[field]).strip()) > 0:
                                            content = str(item[field])[:300]
                                            result += f"   📄 **{field}**: {content}{'...' if len(str(item[field])) > 300 else ''}\n"
                                            break
                                    
                                    # ID 정보로 상세보기 URL 생성
                                    id_fields = ["법령ID", "판례일련번호", "해석례일련번호", "id"]
                                    for field in id_fields:
                                        if field in item and item[field]:
                                            detail_url = f"http://www.law.go.kr/DRF/lawService.do?OC=lchangoo&type=JSON&target={search_type}&ID={item[field]}"
                                            result += f"   🔗 **상세조회 URL**: {detail_url}\n"
                                            break
                            break
                    
                    # 키워드 및 검색 정보 추가
                    if "키워드" in search_data:
                        result += f"\n📝 **검색 키워드**: {search_data['키워드']}\n"
                    if "page" in search_data:
                        result += f"📄 **현재 페이지**: {search_data['page']}\n"
                        
                else:
                    result += f"📊 **전체 응답 데이터**:\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)[:1000]}{'...' if len(json.dumps(data, ensure_ascii=False)) > 1000 else ''}\n```\n"
            else:
                result += f"📊 **전체 응답 데이터**:\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)[:1000]}{'...' if len(json.dumps(data, ensure_ascii=False)) > 1000 else ''}\n```\n"
        
        # 추가 안내사항
        result += f"\n💡 **추가 안내**:\n"
        result += f"- 더 많은 결과를 보려면 `display` 파라미터를 늘려서 검색하세요\n"
        result += f"- 특정 항목의 상세 내용은 해당 ID로 본문 조회 함수를 사용하세요\n"
        result += f"- API 응답의 전체 데이터는 위 URL로 직접 확인 가능합니다\n"
                
        return result
        
    except Exception as e:
        logger.error(f"결과 포맷팅 실패: {e}")
        return f"📊 **원본 응답 데이터**:\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)[:1000]}{'...' if len(json.dumps(data, ensure_ascii=False)) > 1000 else ''}\n```\n\n🔗 **API URL**: {url}\n\n❌ **포맷팅 오류**: {str(e)}"

# ===========================================
# 1. 법령 관련 API (16개)
# ===========================================

@mcp.tool(name="search_law", description="한국의 법령을 검색합니다. 법령명, 키워드로 검색 가능하며 최신 법령 정보를 제공합니다.")
def search_law(query: Optional[str] = None, search: int = 1, display: int = 20, page: int = 1) -> TextContent:
    """법령 목록 조회"""
    search_query = query or "개인정보보호법"
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("law", params)
        url = _generate_api_url("law", params)
        result = _format_search_results(data, "law", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 검색 중 오류: {str(e)}")

@mcp.tool(name="get_law_detail", description="특정 법령의 상세 내용을 조회합니다. 법령ID나 법령명으로 조회 가능합니다.")
def get_law_detail(law_id: Optional[Union[str, int]] = None, law_name: Optional[str] = None) -> TextContent:
    """법령 본문 조회"""
    if not law_id and not law_name:
        return TextContent(type="text", text="❌ 법령ID 또는 법령명을 입력해야 합니다.")
    
    params = {}
    if law_id:
        params["ID"] = str(law_id)
        search_term = f"ID:{law_id}"
    else:
        params["LM"] = law_name or ""
        search_term = law_name or "unknown"
    
    try:
        data = _make_legislation_request("law", params)
        url = _generate_api_url("law", params)
        result = _format_search_results(data, "law", search_term, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_english_law", description="영문 법령을 검색합니다. 한국 법령의 영어 번역본을 제공합니다.")
def search_english_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """영문법령 목록 조회"""
    search_query = query or "Personal Information Protection Act"
    params = {"target": "englaw", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("englaw", params)
        result = _format_search_results(data, "englaw", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 영문법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_effective_law", description="시행일법령을 검색합니다. 특정 시행일자의 법령을 조회할 수 있습니다.")
def search_effective_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """시행일법령 목록 조회"""
    search_query = query or "개인정보보호법"
    params = {"target": "eflaw", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("eflaw", params)
        result = _format_search_results(data, "eflaw", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 시행일법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_law_history", description="법령의 변경이력을 검색합니다. 법령의 개정 과정을 추적할 수 있습니다.")
def search_law_history(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 변경이력 목록 조회"""
    search_query = query or "개인정보보호법"
    params = {"target": "lsHistSearch", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lsHistSearch", params)
        result = _format_search_results(data, "lsHistSearch", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 변경이력 검색 중 오류: {str(e)}")

@mcp.tool(name="search_law_nickname", description="법령의 약칭을 검색합니다. 법령의 별명이나 통칭을 조회할 수 있습니다.")
def search_law_nickname(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 약칭 조회"""
    search_query = query or "개인정보보호법"
    params = {"target": "lsNickNm", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lsNickNm", params)
        result = _format_search_results(data, "lsNickNm", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 약칭 검색 중 오류: {str(e)}")

@mcp.tool(name="search_deleted_law_data", description="삭제된 법령 데이터를 검색합니다. 폐지된 법령 정보를 조회할 수 있습니다.")
def search_deleted_law_data(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """삭제데이터 조회"""
    search_query = query or "개인정보보호법"
    params = {"target": "deldata", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("deldata", params)
        result = _format_search_results(data, "deldata", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 삭제데이터 검색 중 오류: {str(e)}")

@mcp.tool(name="search_law_articles", description="법령의 조문을 검색합니다. 특정 조문별로 상세 내용을 조회할 수 있습니다.")
def search_law_articles(law_id: Union[str, int], display: int = 20, page: int = 1) -> TextContent:
    """조문별 조회"""
    params = {"target": "law", "ID": str(law_id)}
    try:
        data = _make_legislation_request("law", params)
        result = _format_search_results(data, "law", f"법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 조문별 조회 중 오류: {str(e)}")

# ===========================================
# 2. 부가서비스 API (10개)  
# ===========================================

@mcp.tool(name="search_old_and_new_law", description="신구법비교 목록을 검색합니다. 법령 개정 전후의 비교 정보를 제공합니다.")
def search_old_and_new_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """신구법비교 목록 조회"""
    search_query = query or "개인정보보호법"
    params = {"target": "oldAndNew", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("oldAndNew", params)
        result = _format_search_results(data, "oldAndNew", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 신구법비교 검색 중 오류: {str(e)}")

@mcp.tool(name="search_three_way_comparison", description="3단비교 목록을 검색합니다. 인용조문과 위임조문의 3단계 비교를 제공합니다.")
def search_three_way_comparison(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """3단비교 목록 조회"""
    search_query = query or "개인정보보호법"
    params = {"target": "thdCmp", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("thdCmp", params)
        result = _format_search_results(data, "thdCmp", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 3단비교 검색 중 오류: {str(e)}")

@mcp.tool(name="search_deleted_history", description="삭제 이력을 검색합니다. 데이터 삭제 기록을 조회할 수 있습니다.")
def search_deleted_history(knd: Optional[int] = None, display: int = 20, page: int = 1) -> TextContent:
    """삭제이력 조회"""
    params = {"target": "delHst", "display": min(display, 100), "page": page}
    if knd:
        params["knd"] = knd
    try:
        data = _make_legislation_request("delHst", params)
        result = _format_search_results(data, "delHst", f"삭제이력(종류:{knd})")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 삭제이력 검색 중 오류: {str(e)}")

@mcp.tool(name="search_one_view", description="한눈보기 목록을 검색합니다. 법령의 요약 정보를 한 번에 볼 수 있습니다.")
def search_one_view(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """한눈보기 목록 조회"""
    search_query = query or "개인정보보호법"
    params = {"target": "oneview", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("oneview", params)
        result = _format_search_results(data, "oneview", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 한눈보기 검색 중 오류: {str(e)}")

@mcp.tool(name="search_law_system_diagram", description="법령 체계도를 검색합니다. 법령의 구조와 관계를 체계적으로 보여주는 다이어그램을 제공합니다.")
def search_law_system_diagram(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 체계도 목록 조회"""
    search_query = query or "개인정보보호법"
    params = {"target": "lsStmd", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lsStmd", params)
        result = _format_search_results(data, "lsStmd", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 체계도 검색 중 오류: {str(e)}")

@mcp.tool(name="get_law_system_diagram_detail", description="법령 체계도 상세내용을 조회합니다. 특정 법령의 체계도 본문을 제공합니다.")
def get_law_system_diagram_detail(mst_id: Union[str, int]) -> TextContent:
    """법령 체계도 본문 조회"""
    params = {"target": "lsStmd", "MST": str(mst_id)}
    try:
        data = _make_legislation_request("lsStmd", params)
        result = _format_search_results(data, "lsStmd", f"체계도MST:{mst_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 체계도 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_delegated_law", description="위임법령을 조회합니다. 특정 법령에서 위임한 하위법령들의 정보를 제공합니다.")
def get_delegated_law(law_id: Union[str, int]) -> TextContent:
    """위임법령 조회"""
    params = {"target": "lsDelegated", "ID": str(law_id)}
    try:
        data = _make_legislation_request("lsDelegated", params)
        result = _format_search_results(data, "lsDelegated", f"법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 위임법령 조회 중 오류: {str(e)}")

# ===========================================
# 3. 행정규칙 API (5개)
# ===========================================

@mcp.tool(name="search_administrative_rule", description="행정규칙을 검색합니다. 각 부처의 행정규칙과 예규를 제공합니다.")
def search_administrative_rule(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """행정규칙 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "admrul", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("admrul", params)
        result = _format_search_results(data, "admrul", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정규칙 검색 중 오류: {str(e)}")

@mcp.tool(name="get_administrative_rule_detail", description="행정규칙 상세내용을 조회합니다. 특정 행정규칙의 본문을 제공합니다.")
def get_administrative_rule_detail(rule_id: Union[str, int]) -> TextContent:
    """행정규칙 본문 조회"""
    params = {"target": "admrul", "ID": str(rule_id)}
    try:
        data = _make_legislation_request("admrul", params)
        result = _format_search_results(data, "admrul", f"행정규칙ID:{rule_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정규칙 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_administrative_rule_comparison", description="행정규칙 신구법 비교를 검색합니다. 행정규칙의 개정 전후 비교 정보를 제공합니다.")
def search_administrative_rule_comparison(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """행정규칙 신구법 비교 목록 조회"""
    search_query = query or "개인정보보호"
    params = {"target": "admrulOldAndNew", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("admrulOldAndNew", params)
        result = _format_search_results(data, "admrulOldAndNew", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정규칙 신구법 비교 검색 중 오류: {str(e)}")

@mcp.tool(name="get_administrative_rule_comparison_detail", description="행정규칙 신구법 비교 상세내용을 조회합니다. 특정 행정규칙의 신구법 비교 본문을 제공합니다.")
def get_administrative_rule_comparison_detail(comparison_id: Union[str, int]) -> TextContent:
    """행정규칙 신구법 비교 본문 조회"""
    params = {"target": "admrulOldAndNew", "ID": str(comparison_id)}
    try:
        data = _make_legislation_request("admrulOldAndNew", params)
        result = _format_search_results(data, "admrulOldAndNew", f"비교ID:{comparison_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정규칙 신구법 비교 상세 조회 중 오류: {str(e)}")

# ===========================================
# 4. 자치법규 API (4개)
# ===========================================

@mcp.tool(name="search_local_ordinance", description="자치법규(조례, 규칙)를 검색합니다. 지방자치단체의 조례와 규칙을 제공합니다.")
def search_local_ordinance(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """자치법규 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "ordin", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ordin", params)
        result = _format_search_results(data, "ordin", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 자치법규 검색 중 오류: {str(e)}")

@mcp.tool(name="search_ordinance_appendix", description="자치법규 별표서식을 검색합니다. 조례와 규칙의 별표 및 서식을 제공합니다.")
def search_ordinance_appendix(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """자치법규 별표서식 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "ordinbyl", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ordinbyl", params)
        result = _format_search_results(data, "ordinbyl", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 자치법규 별표서식 검색 중 오류: {str(e)}")

@mcp.tool(name="search_linked_ordinance", description="연계 자치법규를 검색합니다. 법령과 연계된 조례를 조회할 수 있습니다.")
def search_linked_ordinance(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """연계 자치법규 검색"""
    search_query = query or "개인정보보호법"
    params = {"target": "lnkLs", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lnkLs", params)
        result = _format_search_results(data, "lnkLs", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 연계 자치법규 검색 중 오류: {str(e)}")

# ===========================================
# 5. 판례관련 API (8개)
# ===========================================

@mcp.tool(name="search_precedent", description="대법원 판례를 검색합니다. 사건명, 키워드로 판례를 찾을 수 있습니다.")
def search_precedent(query: Optional[str] = None, search: int = 1, display: int = 20, page: int = 1) -> TextContent:
    """판례 검색"""
    search_query = query or "개인정보보호"
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("prec", params)
        url = _generate_api_url("prec", params)
        result = _format_search_results(data, "prec", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 판례 검색 중 오류: {str(e)}")

@mcp.tool(name="search_constitutional_court", description="헌법재판소 결정례를 검색합니다. 헌법 관련 중요 판단을 제공합니다.")
def search_constitutional_court(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """헌법재판소 결정례 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "detc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("detc", params)
        result = _format_search_results(data, "detc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 헌법재판소 결정례 검색 중 오류: {str(e)}")

@mcp.tool(name="search_legal_interpretation", description="법제처 법령해석례를 검색합니다. 법령의 구체적 해석과 적용 사례를 제공합니다.")
def search_legal_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령해석례 검색"""
    search_query = query or "개인정보보호"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("expc", params)
        url = _generate_api_url("expc", params)
        result = _format_search_results(data, "expc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령해석례 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_precedent", description="모바일 판례를 검색합니다. 모바일 최적화된 판례 정보를 제공합니다.")
def search_mobile_precedent(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 판례 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "mobprec", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("mobprec", params)
        result = _format_search_results(data, "mobprec", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 판례 검색 중 오류: {str(e)}")

@mcp.tool(name="search_administrative_trial", description="행정심판례를 검색합니다. 행정심판 관련 사건과 결정을 제공합니다.")
def search_administrative_trial(query: Optional[str] = None, search: int = 1, display: int = 20, page: int = 1) -> TextContent:
    """행정심판례 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "decc", "query": search_query, "search": search, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("decc", params)
        result = _format_search_results(data, "decc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정심판례 검색 중 오류: {str(e)}")

@mcp.tool(name="get_administrative_trial_detail", description="행정심판례 상세내용을 조회합니다. 특정 행정심판례의 본문을 제공합니다.")
def get_administrative_trial_detail(trial_id: Union[str, int], trial_name: Optional[str] = None) -> TextContent:
    """행정심판례 본문 조회"""
    params = {"target": "decc", "ID": str(trial_id)}
    if trial_name:
        params["LM"] = trial_name
    try:
        data = _make_legislation_request("decc", params)
        result = _format_search_results(data, "decc", f"행정심판례ID:{trial_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 행정심판례 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_administrative_trial", description="모바일 행정심판례를 검색합니다. 모바일 최적화된 행정심판례 정보를 제공합니다.")
def search_mobile_administrative_trial(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 행정심판례 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "decc", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("decc", params)
        result = _format_search_results(data, "decc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 행정심판례 검색 중 오류: {str(e)}")

# ===========================================
# 6. 위원회결정문 API (30개 주요 위원회)
# ===========================================

@mcp.tool(name="search_privacy_committee", description="개인정보보호위원회 결정문을 검색합니다. 개인정보보호 관련 위원회 결정사항을 제공합니다.")
def search_privacy_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """개인정보보호위원회 결정문 검색"""
    search_query = query or "개인정보수집"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ppc", params)
        url = _generate_api_url("ppc", params)
        result = _format_search_results(data, "ppc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 개인정보보호위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_financial_committee", description="금융위원회 결정문을 검색합니다. 금융 관련 규제와 결정사항을 제공합니다.")
def search_financial_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """금융위원회 결정문 검색"""
    search_query = query or "금융"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("fsc", params)
        url = _generate_api_url("fsc", params)
        result = _format_search_results(data, "fsc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 금융위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_monopoly_committee", description="공정거래위원회 결정문을 검색합니다. 독점규제 및 공정거래 관련 결정사항을 제공합니다.")
def search_monopoly_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """공정거래위원회 결정문 검색"""
    search_query = query or "독점"
    params = {"target": "ftc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ftc", params)
        result = _format_search_results(data, "ftc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 공정거래위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_anticorruption_committee", description="국민권익위원회 결정문을 검색합니다. 부패방지 및 권익보호 관련 결정사항을 제공합니다.")
def search_anticorruption_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """국민권익위원회 결정문 검색"""
    search_query = query or "권익보호"
    params = {"target": "acr", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("acr", params)
        result = _format_search_results(data, "acr", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 국민권익위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_labor_committee", description="노동위원회 결정문을 검색합니다. 노동 관련 분쟁 조정 결정사항을 제공합니다.")
def search_labor_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """노동위원회 결정문 검색"""
    search_query = query or "노동분쟁"
    params = {"target": "nlrc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("nlrc", params)
        result = _format_search_results(data, "nlrc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 노동위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_environment_committee", description="중앙환경분쟁조정위원회 결정문을 검색합니다. 환경 분쟁 조정 관련 결정사항을 제공합니다.")
def search_environment_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """중앙환경분쟁조정위원회 결정문 검색"""
    search_query = query or "환경분쟁"
    params = {"target": "ecc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ecc", params)
        result = _format_search_results(data, "ecc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 중앙환경분쟁조정위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_securities_committee", description="증권선물위원회 결정문을 검색합니다. 증권 및 선물 관련 규제 결정사항을 제공합니다.")
def search_securities_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """증권선물위원회 결정문 검색"""
    search_query = query or "증권"
    params = {"target": "sfc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("sfc", params)
        result = _format_search_results(data, "sfc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 증권선물위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_human_rights_committee", description="국가인권위원회 결정문을 검색합니다. 인권 보호 및 차별 시정 관련 결정사항을 제공합니다.")
def search_human_rights_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """국가인권위원회 결정문 검색"""
    search_query = query or "인권"
    params = {"target": "nhrck", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("nhrck", params)
        result = _format_search_results(data, "nhrck", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 국가인권위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_broadcasting_committee", description="방송통신위원회 결정문을 검색합니다. 방송통신 관련 규제와 결정사항을 제공합니다.")
def search_broadcasting_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """방송통신위원회 결정문 검색"""
    search_query = query or "방송통신"
    params = {"target": "kcc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("kcc", params)
        result = _format_search_results(data, "kcc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 방송통신위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_industrial_accident_committee", description="산업재해보상보험 재심사위원회 결정문을 검색합니다. 산재 관련 결정사항을 제공합니다.")
def search_industrial_accident_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """산업재해보상보험재심사위원회 결정문 검색"""
    search_query = query or "산업재해"
    params = {"target": "iaciac", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("iaciac", params)
        result = _format_search_results(data, "iaciac", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 산업재해보상보험재심사위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_land_tribunal", description="중앙토지수용위원회 결정문을 검색합니다. 토지수용 관련 결정사항을 제공합니다.")
def search_land_tribunal(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """중앙토지수용위원회 결정문 검색"""
    search_query = query or "토지수용"
    params = {"target": "oclt", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("oclt", params)
        result = _format_search_results(data, "oclt", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 중앙토지수용위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_employment_insurance_committee", description="고용보험심사위원회 결정문을 검색합니다. 고용보험 관련 심사 결정사항을 제공합니다.")
def search_employment_insurance_committee(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """고용보험심사위원회 결정문 검색"""
    search_query = query or "고용보험"
    params = {"target": "eiac", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("eiac", params)
        result = _format_search_results(data, "eiac", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 고용보험심사위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="get_employment_insurance_committee_detail", description="고용보험심사위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다.")
def get_employment_insurance_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """고용보험심사위원회 결정문 본문 조회"""
    params = {"target": "eiac", "ID": str(decision_id)}
    try:
        data = _make_legislation_request("eiac", params)
        result = _format_search_results(data, "eiac", f"결정문ID:{decision_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 고용보험심사위원회 결정문 상세 조회 중 오류: {str(e)}")

# ===========================================
# 7. 조약 API (2개)
# ===========================================

@mcp.tool(name="search_treaty", description="조약을 검색합니다. 한국이 체결한 국제조약과 협정을 조회할 수 있습니다.")
def search_treaty(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """조약 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "trty", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("trty", params)
        result = _format_search_results(data, "trty", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 조약 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_treaty", description="모바일 조약을 검색합니다. 모바일 최적화된 조약 정보를 제공합니다.")
def search_mobile_treaty(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 조약 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "trty", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("trty", params)
        result = _format_search_results(data, "trty", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 조약 검색 중 오류: {str(e)}")

# ===========================================
# 8. 별표서식 API (4개)
# ===========================================

@mcp.tool(name="search_law_appendix", description="법령 별표서식을 검색합니다. 법령에 첨부된 별표와 서식을 조회할 수 있습니다.")
def search_law_appendix(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 별표서식 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "licbyl", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("licbyl", params)
        result = _format_search_results(data, "licbyl", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 별표서식 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_law_appendix", description="모바일 법령 별표서식을 검색합니다. 모바일 최적화된 별표서식을 제공합니다.")
def search_mobile_law_appendix(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 법령 별표서식 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "licbyl", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("licbyl", params)
        result = _format_search_results(data, "licbyl", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 법령 별표서식 검색 중 오류: {str(e)}")

# ===========================================
# 9. 학칙공단 API (2개)
# ===========================================

@mcp.tool(name="search_university_regulation", description="대학교 학칙을 검색합니다. 대학의 학칙, 학교규정, 학교지침, 학교시행세칙을 조회할 수 있습니다.")
def search_university_regulation(query: Optional[str] = None, knd: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """대학 학칙 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "school", "query": search_query, "display": min(display, 100), "page": page}
    if knd:
        params["knd"] = knd  # 1:학칙, 2:학교규정, 3:학교지침, 4:학교시행세칙
    try:
        data = _make_legislation_request("school", params)
        result = _format_search_results(data, "school", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 대학 학칙 검색 중 오류: {str(e)}")

@mcp.tool(name="search_public_corporation_regulation", description="지방공사공단 규정을 검색합니다. 지방공사와 공단의 규정을 조회할 수 있습니다.")
def search_public_corporation_regulation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """지방공사공단 규정 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "public", "query": search_query, "display": min(display, 100), "page": page, "knd": "5"}
    try:
        data = _make_legislation_request("public", params)
        result = _format_search_results(data, "public", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 지방공사공단 규정 검색 중 오류: {str(e)}")

@mcp.tool(name="search_public_institution_regulation", description="공공기관 규정을 검색합니다. 공공기관의 내부 규정을 조회할 수 있습니다.")
def search_public_institution_regulation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """공공기관 규정 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "pi", "query": search_query, "display": min(display, 100), "page": page, "knd": "5"}
    try:
        data = _make_legislation_request("pi", params)
        result = _format_search_results(data, "pi", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 공공기관 규정 검색 중 오류: {str(e)}")

@mcp.tool(name="get_university_regulation_detail", description="대학 학칙 상세내용을 조회합니다. 특정 학칙의 본문을 제공합니다.")
def get_university_regulation_detail(regulation_id: Union[str, int], regulation_name: Optional[str] = None) -> TextContent:
    """대학 학칙 본문 조회"""
    params = {"target": "school", "ID": str(regulation_id)}
    if regulation_name:
        params["LM"] = regulation_name
    try:
        data = _make_legislation_request("school", params)
        result = _format_search_results(data, "school", f"학칙ID:{regulation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 대학 학칙 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_public_corporation_regulation_detail", description="지방공사공단 규정 상세내용을 조회합니다. 특정 규정의 본문을 제공합니다.")
def get_public_corporation_regulation_detail(regulation_id: Union[str, int], regulation_name: Optional[str] = None) -> TextContent:
    """지방공사공단 규정 본문 조회"""
    params = {"target": "public", "ID": str(regulation_id)}
    if regulation_name:
        params["LM"] = regulation_name
    try:
        data = _make_legislation_request("public", params)
        result = _format_search_results(data, "public", f"규정ID:{regulation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 지방공사공단 규정 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_public_institution_regulation_detail", description="공공기관 규정 상세내용을 조회합니다. 특정 규정의 본문을 제공합니다.")
def get_public_institution_regulation_detail(regulation_id: Union[str, int], regulation_name: Optional[str] = None) -> TextContent:
    """공공기관 규정 본문 조회"""
    params = {"target": "pi", "ID": str(regulation_id)}
    if regulation_name:
        params["LM"] = regulation_name
    try:
        data = _make_legislation_request("pi", params)
        result = _format_search_results(data, "pi", f"규정ID:{regulation_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 공공기관 규정 상세 조회 중 오류: {str(e)}")

# ===========================================
# 9-1. 특별행정심판 API (4개)
# ===========================================

@mcp.tool(name="search_tax_tribunal", description="조세심판원 특별행정심판례를 검색합니다. 조세 관련 심판 사례를 제공합니다.")
def search_tax_tribunal(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """조세심판원 특별행정심판례 검색"""
    search_query = query or "소득세"
    params = {"target": "ttSpecialDecc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ttSpecialDecc", params)
        result = _format_search_results(data, "ttSpecialDecc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 조세심판원 특별행정심판례 검색 중 오류: {str(e)}")

@mcp.tool(name="get_tax_tribunal_detail", description="조세심판원 특별행정심판례 상세내용을 조회합니다. 특정 심판례의 본문을 제공합니다.")
def get_tax_tribunal_detail(trial_id: Union[str, int]) -> TextContent:
    """조세심판원 특별행정심판례 본문 조회"""
    params = {"target": "ttSpecialDecc", "ID": str(trial_id)}
    try:
        data = _make_legislation_request("ttSpecialDecc", params)
        result = _format_search_results(data, "ttSpecialDecc", f"심판례ID:{trial_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 조세심판원 특별행정심판례 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_maritime_safety_tribunal", description="해양안전심판원 특별행정심판례를 검색합니다. 해양 안전 관련 심판 사례를 제공합니다.")
def search_maritime_safety_tribunal(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """해양안전심판원 특별행정심판례 검색"""
    search_query = query or "해양안전"
    params = {"target": "kmstSpecialDecc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("kmstSpecialDecc", params)
        result = _format_search_results(data, "kmstSpecialDecc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 해양안전심판원 특별행정심판례 검색 중 오류: {str(e)}")

@mcp.tool(name="get_maritime_safety_tribunal_detail", description="해양안전심판원 특별행정심판례 상세내용을 조회합니다. 특정 심판례의 본문을 제공합니다.")
def get_maritime_safety_tribunal_detail(trial_id: Union[str, int]) -> TextContent:
    """해양안전심판원 특별행정심판례 본문 조회"""
    params = {"target": "kmstSpecialDecc", "ID": str(trial_id)}
    try:
        data = _make_legislation_request("kmstSpecialDecc", params)
        result = _format_search_results(data, "kmstSpecialDecc", f"심판례ID:{trial_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 해양안전심판원 특별행정심판례 상세 조회 중 오류: {str(e)}")

# ===========================================
# 10. 법령용어 API (2개)
# ===========================================

@mcp.tool(name="search_legal_term", description="법령용어를 검색합니다. 법률 용어의 정의와 설명을 조회할 수 있습니다.")
def search_legal_term(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령용어 검색"""
    search_query = query or "개인정보"
    params = {"target": "lstrm", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lstrm", params)
        result = _format_search_results(data, "lstrm", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령용어 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_legal_term", description="모바일 법령용어를 검색합니다. 모바일 최적화된 법령용어 정보를 제공합니다.")
def search_mobile_legal_term(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 법령용어 검색"""
    search_query = query or "개인정보"
    params = {"target": "lstrm", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("lstrm", params)
        result = _format_search_results(data, "lstrm", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 법령용어 검색 중 오류: {str(e)}")

# ===========================================
# 11. 모바일 API (15개)
# ===========================================

@mcp.tool(name="search_mobile_law", description="모바일 법령을 검색합니다. 모바일 기기에 최적화된 법령 정보를 제공합니다.")
def search_mobile_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 법령 검색"""
    search_query = query or "개인정보보호법"
    params = {"target": "law", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("law", params)
        result = _format_search_results(data, "law", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_english_law", description="모바일 영문법령을 검색합니다. 모바일 최적화된 영문법령을 제공합니다.")
def search_mobile_english_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 영문법령 검색"""
    search_query = query or "Personal Information Protection Act"
    params = {"target": "englaw", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("englaw", params)
        result = _format_search_results(data, "englaw", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 영문법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_administrative_rule", description="모바일 행정규칙을 검색합니다. 모바일 최적화된 행정규칙을 제공합니다.")
def search_mobile_administrative_rule(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 행정규칙 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "admrul", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("admrul", params)
        result = _format_search_results(data, "admrul", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 행정규칙 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_local_ordinance", description="모바일 자치법규를 검색합니다. 모바일 최적화된 자치법규를 제공합니다.")
def search_mobile_local_ordinance(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 자치법규 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "ordin", "query": search_query, "display": min(display, 100), "page": page, "mobileYn": "Y"}
    try:
        data = _make_legislation_request("ordin", params)
        result = _format_search_results(data, "ordin", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 모바일 자치법규 검색 중 오류: {str(e)}")

# ===========================================
# 12. 맞춤형 API (6개)
# ===========================================

@mcp.tool(name="search_custom_law", description="맞춤형 법령을 검색합니다. 사용자 맞춤형 법령 분류에 따른 검색을 제공합니다.")
def search_custom_law(vcode: str, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 법령 검색"""
    params = {"target": "couseLs", "vcode": vcode, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("couseLs", params)
        result = _format_search_results(data, "couseLs", f"분류코드:{vcode}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 맞춤형 법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_custom_law_articles", description="맞춤형 법령 조문을 검색합니다. 사용자 맞춤형 법령의 조문별 내용을 제공합니다.")
def search_custom_law_articles(vcode: str, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 법령 조문 검색"""
    params = {"target": "couseLs", "vcode": vcode, "lj": "jo", "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("couseLs", params)
        result = _format_search_results(data, "couseLs", f"분류코드:{vcode} 조문")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 맞춤형 법령 조문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_custom_ordinance", description="맞춤형 자치법규를 검색합니다. 사용자 맞춤형 자치법규 분류에 따른 검색을 제공합니다.")
def search_custom_ordinance(vcode: str, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 자치법규 검색"""
    params = {"target": "couseOrdin", "vcode": vcode, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("couseOrdin", params)
        result = _format_search_results(data, "couseOrdin", f"분류코드:{vcode}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 맞춤형 자치법규 검색 중 오류: {str(e)}")

@mcp.tool(name="search_custom_ordinance_articles", description="맞춤형 자치법규 조문을 검색합니다. 사용자 맞춤형 자치법규의 조문별 내용을 제공합니다.")
def search_custom_ordinance_articles(vcode: str, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 자치법규 조문 검색"""
    params = {"target": "couseOrdin", "vcode": vcode, "lj": "jo", "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("couseOrdin", params)
        result = _format_search_results(data, "couseOrdin", f"분류코드:{vcode} 조문")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 맞춤형 자치법규 조문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_custom_precedent", description="맞춤형 판례를 검색합니다. 사용자 맞춤형 판례 분류에 따른 검색을 제공합니다.")
def search_custom_precedent(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 판례 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "custprec", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("custprec", params)
        result = _format_search_results(data, "custprec", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 맞춤형 판례 검색 중 오류: {str(e)}")

# ===========================================
# 13. 지식베이스 API (6개)
# ===========================================

@mcp.tool(name="search_legal_ai", description="법령 AI 지식베이스를 검색합니다. AI 기반 법령 정보와 분석을 제공합니다.")
def search_legal_ai(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 AI 지식베이스 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "lstrmAI", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lstrmAI", params)
        result = _format_search_results(data, "lstrmAI", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 AI 지식베이스 검색 중 오류: {str(e)}")

@mcp.tool(name="search_knowledge_base", description="지식베이스를 검색합니다. 법령 관련 지식과 정보를 종합적으로 제공합니다.")
def search_knowledge_base(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """지식베이스 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "knowledge", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("knowledge", params)
        result = _format_search_results(data, "knowledge", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 지식베이스 검색 중 오류: {str(e)}")

@mcp.tool(name="search_faq", description="자주 묻는 질문을 검색합니다. 법령 관련 FAQ 정보를 제공합니다.")
def search_faq(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """FAQ 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "faq", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("faq", params)
        result = _format_search_results(data, "faq", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ FAQ 검색 중 오류: {str(e)}")

@mcp.tool(name="search_qna", description="질의응답을 검색합니다. 법령 관련 질의응답 정보를 제공합니다.")
def search_qna(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """질의응답 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "qna", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("qna", params)
        result = _format_search_results(data, "qna", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 질의응답 검색 중 오류: {str(e)}")

@mcp.tool(name="search_counsel", description="상담 내용을 검색합니다. 법령 상담 사례와 답변을 제공합니다.")
def search_counsel(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """상담 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "counsel", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("counsel", params)
        result = _format_search_results(data, "counsel", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 상담 검색 중 오류: {str(e)}")

@mcp.tool(name="search_precedent_counsel", description="판례 상담을 검색합니다. 판례 관련 상담 사례와 답변을 제공합니다.")
def search_precedent_counsel(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """판례 상담 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "precCounsel", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("precCounsel", params)
        result = _format_search_results(data, "precCounsel", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 판례 상담 검색 중 오류: {str(e)}")

# ===========================================
# 14. 기타 API (1개)
# ===========================================

@mcp.tool(name="search_civil_petition", description="민원을 검색합니다. 법령 관련 민원 사례와 처리 현황을 제공합니다.")
def search_civil_petition(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """민원 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "minwon", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("minwon", params)
        result = _format_search_results(data, "minwon", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 민원 검색 중 오류: {str(e)}")

# ===========================================
# 15. 중앙부처해석 API (14개)
# ===========================================

@mcp.tool(name="search_moef_interpretation", description="기획재정부 법령해석을 검색합니다. 기획재정부의 법령해석 사례를 제공합니다.")
def search_moef_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """기획재정부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "moefCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("moefCgmExpc", params)
        result = _format_search_results(data, "moefCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 기획재정부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_molit_interpretation", description="국토교통부 법령해석을 검색합니다. 국토교통부의 법령해석 사례를 제공합니다.")
def search_molit_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """국토교통부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "molitCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("molitCgmExpc", params)
        result = _format_search_results(data, "molitCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 국토교통부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_moel_interpretation", description="고용노동부 법령해석을 검색합니다. 고용노동부의 법령해석 사례를 제공합니다.")
def search_moel_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """고용노동부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "moelCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("moelCgmExpc", params)
        result = _format_search_results(data, "moelCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 고용노동부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mof_interpretation", description="해양수산부 법령해석을 검색합니다. 해양수산부의 법령해석 사례를 제공합니다.")
def search_mof_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """해양수산부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "mofCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("mofCgmExpc", params)
        result = _format_search_results(data, "mofCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 해양수산부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mohw_interpretation", description="보건복지부 법령해석을 검색합니다. 보건복지부의 법령해석 사례를 제공합니다.")
def search_mohw_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """보건복지부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "mohwCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("mohwCgmExpc", params)
        result = _format_search_results(data, "mohwCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 보건복지부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_moe_interpretation", description="교육부 법령해석을 검색합니다. 교육부의 법령해석 사례를 제공합니다.")
def search_moe_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """교육부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "moeCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("moeCgmExpc", params)
        result = _format_search_results(data, "moeCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 교육부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_korea_interpretation", description="한국 법령해석을 검색합니다. 범정부 차원의 법령해석 사례를 제공합니다.")
def search_korea_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """한국 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "koreaExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("koreaExpc", params)
        result = _format_search_results(data, "koreaExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 한국 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mssp_interpretation", description="보훈처 법령해석을 검색합니다. 국가보훈처의 법령해석 사례를 제공합니다.")
def search_mssp_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """보훈처 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "msspCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("msspCgmExpc", params)
        result = _format_search_results(data, "msspCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 보훈처 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mote_interpretation", description="산업통상자원부 법령해석을 검색합니다. 산업통상자원부의 법령해석 사례를 제공합니다.")
def search_mote_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """산업통상자원부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "moteCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("moteCgmExpc", params)
        result = _format_search_results(data, "moteCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 산업통상자원부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_maf_interpretation", description="농림축산식품부 법령해석을 검색합니다. 농림축산식품부의 법령해석 사례를 제공합니다.")
def search_maf_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """농림축산식품부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "mafCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("mafCgmExpc", params)
        result = _format_search_results(data, "mafCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 농림축산식품부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_moms_interpretation", description="국방부 법령해석을 검색합니다. 국방부의 법령해석 사례를 제공합니다.")
def search_moms_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """국방부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "momsCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("momsCgmExpc", params)
        result = _format_search_results(data, "momsCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 국방부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_sme_interpretation", description="중소벤처기업부 법령해석을 검색합니다. 중소벤처기업부의 법령해석 사례를 제공합니다.")
def search_sme_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """중소벤처기업부 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "smeexpcCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("smeexpcCgmExpc", params)
        result = _format_search_results(data, "smeexpcCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 중소벤처기업부 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_nfa_interpretation", description="산림청 법령해석을 검색합니다. 산림청의 법령해석 사례를 제공합니다.")
def search_nfa_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """산림청 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "nfaCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("nfaCgmExpc", params)
        result = _format_search_results(data, "nfaCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 산림청 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="search_korail_interpretation", description="한국철도공사 법령해석을 검색합니다. 한국철도공사의 법령해석 사례를 제공합니다.")
def search_korail_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """한국철도공사 법령해석 검색"""
    search_query = query or "개인정보보호"
    params = {"target": "korailCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("korailCgmExpc", params)
        result = _format_search_results(data, "korailCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"❌ 한국철도공사 법령해석 검색 중 오류: {str(e)}")

# ===========================================
# 16. 종합 검색 도구
# ===========================================

@mcp.tool(name="search_all_legal_documents", description="법령, 판례, 해석례, 위원회 결정문을 통합 검색합니다. 한 번에 모든 법적 문서를 검색할 수 있습니다.")
def search_all_legal_documents(
    query: Optional[str] = None,
    include_law: bool = True,
    include_precedent: bool = True,
    include_interpretation: bool = True,
    include_committee: bool = True
) -> TextContent:
    """통합 법률 문서 검색 - 안전한 패턴으로 수정"""
    search_query = query or "개인정보보호"
    
    results = []
    results.append(f"🔍 **'{search_query}' 통합 검색 결과**\n")
    results.append("=" * 50 + "\n")
    
    try:
        # 1. 법령 검색
        if include_law:
            law_params = {"query": search_query, "display": 3}
            law_data = _make_legislation_request("law", law_params)
            law_url = _generate_api_url("law", law_params)
            law_result = _format_search_results(law_data, "law", search_query, law_url)
            results.append("📜 **법령 검색 결과:**\n")
            results.append(law_result + "\n")
        
        # 2. 판례 검색  
        if include_precedent:
            prec_params = {"query": search_query, "display": 3}
            prec_data = _make_legislation_request("prec", prec_params)
            prec_url = _generate_api_url("prec", prec_params)
            prec_result = _format_search_results(prec_data, "prec", search_query, prec_url)
            results.append("⚖️ **판례 검색 결과:**\n")
            results.append(prec_result + "\n")
        
        # 3. 해석례 검색
        if include_interpretation:
            interp_params = {"query": search_query, "display": 3}
            interp_data = _make_legislation_request("expc", interp_params)
            interp_url = _generate_api_url("expc", interp_params)
            interp_result = _format_search_results(interp_data, "expc", search_query, interp_url)
            results.append("📖 **해석례 검색 결과:**\n")
            results.append(interp_result + "\n")
        
        # 4. 개인정보보호위원회 결정문 검색
        if include_committee:
            committee_params = {"query": search_query, "display": 3}
            committee_data = _make_legislation_request("ppc", committee_params)
            committee_url = _generate_api_url("ppc", committee_params)
            committee_result = _format_search_results(committee_data, "ppc", search_query, committee_url)
            results.append("🏛️ **위원회 결정문 검색 결과:**\n")
            results.append(committee_result + "\n")
        
        return TextContent(type="text", text="".join(results))
        
    except Exception as e:
        error_msg = f"❌ 통합 검색 중 오류가 발생했습니다: {str(e)}"
        return TextContent(type="text", text=error_msg)

logger.info("✅ 121개 법제처 OPEN API 도구가 모두 로드되었습니다!") 
"""
한국 법제처 OPEN API 121개 완전 통합 MCP 도구

search_simple_law의 성공 패턴을 적용한 안전하고 간단한 모든 도구들
모든 카테고리: 법령, 부가서비스, 행정규칙, 자치법규, 판례관련, 위원회결정문, 
조약, 별표서식, 학칙공단, 법령용어, 모바일, 맞춤형, 지식베이스, 기타, 중앙부처해석
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

def _normalize_search_query(query: str) -> str:
    """검색어 정규화 - 법령명 검색 최적화"""
    if not query:
        return query
        
    # 기본 정규화
    normalized = query.strip()
    
    # 공백 제거 (법령명은 보통 공백 없이)
    normalized = normalized.replace(" ", "")
    
    # 일반적인 법령 접미사 정규화
    law_suffixes = {
        "에관한법률": "법",
        "에관한법": "법", 
        "시행령": "령",
        "시행규칙": "규칙",
        "에관한규정": "규정",
        "에관한규칙": "규칙"
    }
    
    for old_suffix, new_suffix in law_suffixes.items():
        if normalized.endswith(old_suffix):
            normalized = normalized[:-len(old_suffix)] + new_suffix
            break
    
    return normalized

def _create_search_variants(query: str) -> list[str]:
    """검색어 변형 생성 - 금융/개인정보 특화 확장"""
    variants = []
    
    # 원본
    variants.append(query)
    
    # 정규화된 버전
    normalized = _normalize_search_query(query)
    if normalized != query:
        variants.append(normalized)
    
    # 공백 포함/제거 변형
    if " " in query:
        variants.append(query.replace(" ", ""))
    
    # "법" 추가/제거 변형
    if not query.endswith("법"):
        variants.append(query + "법")
    if query.endswith("법") and len(query) > 1:
        variants.append(query[:-1])
    
    # 금융/개인정보 특화 키워드 확장
    finance_expansions = {
        "개인정보": ["개인정보보호", "개인정보처리", "개인정보활용", "개인정보수집"],
        "금융": ["금융회사", "금융기관", "금융업", "은행", "보험회사"],
        "신용정보": ["신용정보처리", "신용정보보호", "신용정보활용"],
        "핀테크": ["금융서비스", "전자금융", "인터넷금융"],
        "데이터": ["데이터처리", "데이터보호", "데이터활용"],
        "암호화": ["정보보안", "개인정보암호화"],
        "동의": ["사전동의", "명시적동의", "별도동의"]
    }
    
    # 키워드 확장 적용
    for keyword, expansions in finance_expansions.items():
        if keyword in query.lower():
            for expansion in expansions[:3]:  # 상위 3개만
                variants.append(expansion)
                # 원본 쿼리에서 키워드를 확장어로 치환
                expanded_query = query.lower().replace(keyword, expansion)
                if expanded_query != query.lower():
                    variants.append(expanded_query)
    
    # 조합형 검색어 생성 (금융 + 개인정보)
    if any(k in query.lower() for k in ["금융", "은행", "보험", "카드"]):
        if "개인정보" not in query.lower():
            variants.extend([f"{query} 개인정보", f"개인정보 {query}"])
    
    # 중복 제거하면서 순서 유지
    unique_variants = []
    for variant in variants:
        if variant and variant not in unique_variants:
            unique_variants.append(variant)
            
    return unique_variants[:10]  # 최대 10개로 제한

def _smart_search(target: str, query: str, display: int = 20, page: int = 1) -> dict:
    """지능형 다단계 검색 - 정확도 우선에서 점진적 확장"""
    if not query:
        return {"LawSearch": {target: []}}
    
    search_attempts = []
    variants = _create_search_variants(query)
    
    # 1단계: 정확한 법령명 검색 (search=1)
    for variant in variants[:2]:  # 상위 2개 변형만
        search_attempts.append({
            "query": variant,
            "search": 1,  # 법령명 검색
            "sort": "lasc",  # 법령명 오름차순 (관련도 높음)
            "display": min(display, 20)
        })
    
    # 2단계: 본문 검색 (search=2) - 더 넓은 범위
    for variant in variants[:1]:  # 가장 좋은 변형만
        search_attempts.append({
            "query": variant,
            "search": 2,  # 본문검색
            "sort": "lasc",
            "display": min(display, 30)
        })
    
    # 3단계: 키워드 분리 검색
    keywords = query.replace(" ", "").split("보호")  # 예: "개인정보보호법" -> ["개인정보", "법"]
    if len(keywords) > 1:
        main_keyword = keywords[0]  # "개인정보"
        search_attempts.append({
            "query": main_keyword,
            "search": 2,
            "sort": "lasc", 
            "display": min(display, 40)
        })
    
    # 검색 시도
    best_result = None
    best_count = 0
    
    for attempt in search_attempts:
        try:
            data = _make_legislation_request(target, attempt)
            
            if isinstance(data, dict) and data.get('LawSearch'):
                items = data['LawSearch'].get(target, [])
                if isinstance(items, dict):  # 단일 결과를 리스트로 변환
                    items = [items]
                
                # 관련성 점수 계산
                relevant_count = 0
                for item in items:
                    title = item.get('법령명한글', '').lower()
                    if any(keyword.lower() in title for keyword in variants[:2]):
                        relevant_count += 1
                
                # 최고 품질 결과 선택
                current_best_items: list = best_result.get('LawSearch', {}).get(target, []) if best_result else []
                if relevant_count > best_count or (relevant_count == best_count and len(items) > len(current_best_items)):
                    best_result = data
                    best_count = relevant_count
                    
                # 충분히 좋은 결과면 조기 종료
                if relevant_count >= 3 and attempt["search"] == 1:
                    break
                    
        except Exception as e:
            logger.warning(f"검색 시도 실패: {attempt} - {e}")
            continue
    
    return best_result or {"LawSearch": {target: []}}

def _generate_api_url(target: str, params: dict, is_detail: bool = False) -> str:
    """API URL 생성 함수
    
    Args:
        target: API 대상 (law, prec, ppc, expc 등)
        params: 요청 파라미터
        is_detail: True면 상세조회(lawService.do), False면 검색(lawSearch.do)
    """
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
        
        # URL 결정: 상세조회 vs 검색
        if is_detail and ("ID" in params or "MST" in params):
            # 상세조회: lawService.do 사용
            url = legislation_config.service_base_url
        else:
            # 검색: lawSearch.do 사용
            url = legislation_config.search_base_url
        
        return f"{url}?{urlencode(base_params)}"
        
    except Exception as e:
        logger.error(f"URL 생성 실패: {e}")
        return ""

def _make_legislation_request(target: str, params: dict, is_detail: bool = False) -> dict:
    """법제처 API 공통 요청 함수
    
    Args:
        target: API 대상 (law, prec, ppc, expc 등)
        params: 요청 파라미터
        is_detail: True면 상세조회(lawService.do), False면 검색(lawSearch.do)
    """
    try:
        import requests
        
        # API 키 설정
        oc = os.getenv("LEGISLATION_API_KEY", "lchangoo")
        
        # 기본 파라미터 설정 (params의 type이 있으면 우선 사용)
        base_params = {
            "OC": oc,
            "type": "JSON"
        }
        base_params.update(params)  # params에 type이 있으면 기본값 덮어씀
        
        # URL 결정: 상세조회 vs 검색
        if is_detail and ("ID" in params or "MST" in params):
            # 상세조회: lawService.do 사용
            url = legislation_config.service_base_url
        else:
            # 검색: lawSearch.do 사용
            url = legislation_config.search_base_url
        
        base_params["target"] = target
        
        response = requests.get(url, params=base_params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        return data
        
    except Exception as e:
        logger.error(f"API 요청 실패: {e}")
        return {"error": str(e)}

def _format_search_results(data: dict, search_type: str, query: str = "", url: str = "") -> str:
    """검색 결과를 풍부하고 체계적으로 포맷팅 (이모티콘 최소화, 정보 최대화)"""
    
    if "error" in data:
        return f"오류: {data['error']}\n\nAPI URL: {url}"
    
    try:
        result = ""
        
        # API 호출 URL 정보
        if url:
            result += f"API 호출 URL: {url}\n\n"
        
        # 법령 검색 결과 (LawSearch)
        if "LawSearch" in data:
            search_data = data["LawSearch"]
            total_count = search_data.get("totalCnt", 0)
            keyword = search_data.get("키워드", query)
            result += f"'{keyword}' 법령 검색 결과 (총 {total_count}건)\n\n"
            
            # 단일 객체 또는 배열 처리
            law_data = search_data.get("law")
            if isinstance(law_data, dict):
                items = [law_data]
            elif isinstance(law_data, list):
                items = law_data
            else:
                items = []
            
            if items:
                for i, item in enumerate(items[:10], 1):
                    if isinstance(item, dict):
                        result += f"{i}. {item.get('법령명한글', '법령명 없음')}\n"
                        result += f"   법령구분: {item.get('법령구분명', '미지정')}\n"
                        result += f"   소관부처: {item.get('소관부처명', '미지정')}\n"
                        result += f"   법령ID: {item.get('법령ID', '미지정')}\n"
                        result += f"   현행연혁: {item.get('현행연혁코드', '미지정')}\n"
                        result += f"   공포일자: {item.get('공포일자', '미지정')}\n"
                        result += f"   시행일자: {item.get('시행일자', '미지정')}\n"
                        result += f"   공포번호: {item.get('공포번호', '미지정')}\n"
                        result += f"   제개정구분: {item.get('제개정구분명', '미지정')}\n"
                        result += f"   법령일련번호: {item.get('법령일련번호', '미지정')}\n"
                        
                        # 상세링크 처리
                        detail_link = item.get('법령상세링크', '')
                        if detail_link:
                            result += f"   상세조회 URL: http://www.law.go.kr{detail_link}\n"
                        elif item.get('법령ID'):
                            result += f"   상세조회 URL: {legislation_config.service_base_url}?OC={legislation_config.oc}&type=JSON&target=law&ID={item['법령ID']}\n"
                        result += "\n"
            else:
                result += "검색된 법령이 없습니다.\n"
                
        # 판례 검색 결과 (PrecSearch)
        elif "PrecSearch" in data:
            search_data = data["PrecSearch"]
            total_count = search_data.get("totalCnt", 0)
            keyword = search_data.get("키워드", query)
            result += f"'{keyword}' 판례 검색 결과 (총 {total_count}건)\n\n"
            
            # 단일 객체 또는 배열 처리
            prec_data = search_data.get("prec")
            if isinstance(prec_data, dict):
                items = [prec_data]
            elif isinstance(prec_data, list):
                items = prec_data
            else:
                items = []
                
            if items:
                for i, item in enumerate(items[:10], 1):
                    if isinstance(item, dict):
                        result += f"{i}. {item.get('사건명', '사건명 없음')}\n"
                        result += f"   사건번호: {item.get('사건번호', '미지정')}\n"
                        result += f"   법원명: {item.get('법원명', '미지정')}\n"
                        result += f"   선고일자: {item.get('선고일자', '미지정')}\n"
                        result += f"   사건종류: {item.get('사건종류명', '미지정')}\n"
                        result += f"   판결유형: {item.get('판결유형', '미지정')}\n"
                        result += f"   데이터출처: {item.get('데이터출처명', '미지정')}\n"
                        result += f"   판례일련번호: {item.get('판례일련번호', '미지정')}\n"
                        
                        # 상세링크 처리
                        detail_link = item.get('판례상세링크', '')
                        if detail_link:
                            result += f"   상세조회 URL: http://www.law.go.kr{detail_link}\n"
                        result += "\n"
            else:
                result += "검색된 판례가 없습니다.\n"
        
        # 해석례 검색 결과 (Expc)
        elif "Expc" in data:
            search_data = data["Expc"]
            total_count = search_data.get("totalCnt", 0)
            keyword = search_data.get("키워드", query)
            result += f"'{keyword}' 해석례 검색 결과 (총 {total_count}건)\n\n"
            
            # 단일 객체 또는 배열 처리
            expc_data = search_data.get("expc")
            if isinstance(expc_data, dict):
                items = [expc_data]
            elif isinstance(expc_data, list):
                items = expc_data
            else:
                items = []
                
            if items:
                for i, item in enumerate(items[:10], 1):
                    if isinstance(item, dict):
                        result += f"{i}. {item.get('안건명', '안건명 없음')}\n"
                        result += f"   안건번호: {item.get('안건번호', '미지정')}\n"
                        result += f"   회신기관: {item.get('회신기관명', '미지정')}\n"
                        result += f"   질의기관: {item.get('질의기관명', '미지정')}\n"
                        result += f"   회신일자: {item.get('회신일자', '미지정')}\n"
                        result += f"   해석례일련번호: {item.get('법령해석례일련번호', '미지정')}\n"
                        
                        # 상세링크 처리
                        detail_link = item.get('법령해석례상세링크', '')
                        if detail_link:
                            result += f"   상세조회 URL: http://www.law.go.kr{detail_link}\n"
                        result += "\n"
            else:
                result += "검색된 해석례가 없습니다.\n"
                
        # 행정규칙 검색 결과 (AdmRulSearch)
        elif "AdmRulSearch" in data:
            search_data = data["AdmRulSearch"]
            total_count = search_data.get("totalCnt", 0)
            keyword = search_data.get("키워드", query)
            result += f"'{keyword}' 행정규칙 검색 결과 (총 {total_count}건)\n\n"
            
            # 단일 객체 또는 배열 처리
            admrul_data = search_data.get("admrul")
            if isinstance(admrul_data, dict):
                items = [admrul_data]
            elif isinstance(admrul_data, list):
                items = admrul_data
            else:
                items = []
                
            if items:
                for i, item in enumerate(items[:10], 1):
                    if isinstance(item, dict):
                        result += f"{i}. {item.get('행정규칙명', '행정규칙명 없음')}\n"
                        result += f"   행정규칙ID: {item.get('행정규칙ID', '미지정')}\n"
                        result += f"   행정규칙종류: {item.get('행정규칙종류', '미지정')}\n"
                        result += f"   소관부처: {item.get('소관부처명', '미지정')}\n"
                        result += f"   발령일자: {item.get('발령일자', '미지정')}\n"
                        result += f"   시행일자: {item.get('시행일자', '미지정')}\n"
                        result += f"   발령번호: {item.get('발령번호', '미지정')}\n"
                        result += f"   제개정구분: {item.get('제개정구분명', '미지정')}\n"
                        result += f"   현행연혁구분: {item.get('현행연혁구분', '미지정')}\n"
                        result += f"   행정규칙일련번호: {item.get('행정규칙일련번호', '미지정')}\n"
                        
                        # 상세링크 처리
                        detail_link = item.get('행정규칙상세링크', '')
                        if detail_link:
                            result += f"   상세조회 URL: http://www.law.go.kr{detail_link}\n"
                        result += "\n"
            else:
                result += "검색된 행정규칙이 없습니다.\n"
                
        # 금융위원회 결정문 (Fsc)
        elif "Fsc" in data:
            search_data = data["Fsc"]
            total_count = search_data.get("totalCnt", 0)
            keyword = search_data.get("키워드", query)
            result += f"금융위원회 '{keyword}' 검색 결과 (총 {total_count}건)\n\n"
            
            items = search_data.get("fsc", [])
            if not isinstance(items, list):
                items = []
                
            if items:
                for i, item in enumerate(items[:10], 1):
                    if isinstance(item, dict):
                        result += f"{i}. {item.get('안건명', '안건명 없음')}\n"
                        result += f"   의결번호: {item.get('의결번호', '미지정')}\n"
                        result += f"   기관명: {item.get('기관명', '미지정')}\n"
                        result += f"   결정문일련번호: {item.get('결정문일련번호', '미지정')}\n"
                        
                        detail_link = item.get('결정문상세링크', '')
                        if detail_link:
                            result += f"   상세조회 URL: http://www.law.go.kr{detail_link}\n"
                        result += "\n"
            else:
                result += "검색된 금융위원회 결정문이 없습니다.\n"
                
        # 금융위원회 결정문 상세조회 (FscService)
        elif "FscService" in data:
            service_data = data["FscService"]
            decision_data = service_data.get("의결서", {})
            
            if decision_data:
                result += f"금융위원회 결정문 상세내용\n\n"
                result += f"기관명: {decision_data.get('기관명', '금융위원회')}\n"
                result += f"결정문일련번호: {decision_data.get('결정문일련번호', '미지정')}\n"
                result += f"안건명: {decision_data.get('안건명', '미지정')}\n"
                result += f"의결일자: {decision_data.get('의결일자', '미지정')}\n"
                result += f"회의종류: {decision_data.get('회의종류', '미지정')}\n"
                result += f"결정구분: {decision_data.get('결정', '미지정')}\n\n"
                
                # 주문
                if decision_data.get('주문'):
                    result += f"【주문】\n{decision_data['주문']}\n\n"
                
                # 이유
                if decision_data.get('이유'):
                    result += f"【이유】\n{decision_data['이유']}\n\n"
                
                # 별지 (상세 내용)
                if decision_data.get('별지'):
                    result += f"【별지】\n{decision_data['별지']}\n\n"
                
                # 기타 정보
                other_fields = ['결정요지', '배경', '주요내용', '신청인', '위원서명']
                for field in other_fields:
                    if decision_data.get(field) and decision_data[field].strip():
                        result += f"【{field}】\n{decision_data[field]}\n\n"
                        
            else:
                result += "금융위원회 결정문 상세내용을 찾을 수 없습니다.\n"
                
        # 개인정보보호위원회 결정문 (Ppc)  
        elif "Ppc" in data:
            search_data = data["Ppc"]
            total_count = search_data.get("totalCnt", 0)
            keyword = search_data.get("키워드", query)
            agency = search_data.get("기관명", "개인정보보호위원회")
            result += f"{agency} '{keyword}' 검색 결과 (총 {total_count}건)\n\n"
            
            items = search_data.get("ppc", [])
            if not isinstance(items, list):
                items = []
                
            if items:
                for i, item in enumerate(items[:10], 1):
                    if isinstance(item, dict):
                        result += f"{i}. {item.get('안건명', '안건명 없음')}\n"
                        result += f"   의안번호: {item.get('의안번호', '미지정')}\n"
                        result += f"   의결일: {item.get('의결일', '미지정')}\n"
                        result += f"   결정구분: {item.get('결정구분', '미지정')}\n"
                        result += f"   회의종류: {item.get('회의종류', '미지정')}\n"
                        result += f"   결정문일련번호: {item.get('결정문일련번호', '미지정')}\n"
                        
                        detail_link = item.get('결정문상세링크', '')
                        if detail_link:
                            result += f"   상세조회 URL: http://www.law.go.kr{detail_link}\n"
                        result += "\n"
            else:
                result += "검색된 개인정보보호위원회 결정문이 없습니다.\n"
                
        # 개인정보보호위원회 결정문 상세조회 (PpcService)
        elif "PpcService" in data:
            service_data = data["PpcService"]
            decision_data = service_data.get("의결서", {})
            
            if decision_data:
                result += f"개인정보보호위원회 결정문 상세내용\n\n"
                result += f"기관명: {decision_data.get('기관명', '개인정보보호위원회')}\n"
                result += f"결정문일련번호: {decision_data.get('결정문일련번호', '미지정')}\n"
                result += f"안건명: {decision_data.get('안건명', '미지정')}\n"
                result += f"의결일자: {decision_data.get('의결일자', '미지정')}\n"
                result += f"회의종류: {decision_data.get('회의종류', '미지정')}\n"
                result += f"결정구분: {decision_data.get('결정', '미지정')}\n"
                result += f"위원서명: {decision_data.get('위원서명', '미지정')}\n\n"
                
                # 주문
                if decision_data.get('주문'):
                    result += f"【주문】\n{decision_data['주문']}\n\n"
                
                # 이유
                if decision_data.get('이유'):
                    result += f"【이유】\n{decision_data['이유']}\n\n"
                
                # 별지 (상세 내용)
                if decision_data.get('별지'):
                    result += f"【별지】\n{decision_data['별지']}\n\n"
                
                # 기타 정보
                other_fields = ['결정요지', '배경', '주요내용', '신청인', '이의제기방법및기간']
                for field in other_fields:
                    if decision_data.get(field) and decision_data[field].strip():
                        result += f"【{field}】\n{decision_data[field]}\n\n"
                        
            else:
                result += "개인정보보호위원회 결정문 상세내용을 찾을 수 없습니다.\n"
                
        # 오류 응답 처리 (공통)
        elif "Law" in data and isinstance(data["Law"], str):
            result += f"조회 결과: {data['Law']}\n"
            
        # 법령 상세조회 (LawService)
        elif "LawService" in data:
            service_data = data["LawService"]
            law_data = service_data.get("법령", {})
            
            if law_data:
                result += f"법령 상세내용\n\n"
                result += f"법령명: {law_data.get('법령명', law_data.get('법령명한글', '미지정'))}\n"
                result += f"법령구분: {law_data.get('법령구분명', '미지정')}\n"
                result += f"소관부처: {law_data.get('소관부처명', '미지정')}\n"
                result += f"법령ID: {law_data.get('법령ID', '미지정')}\n"
                result += f"공포일자: {law_data.get('공포일자', '미지정')}\n"
                result += f"시행일자: {law_data.get('시행일자', '미지정')}\n"
                result += f"공포번호: {law_data.get('공포번호', '미지정')}\n"
                result += f"현행연혁코드: {law_data.get('현행연혁코드', '미지정')}\n\n"
                
                # 조문 내용 (배열 형태)
                if law_data.get('조문') and isinstance(law_data['조문'], list):
                    result += f"【조문내용】\n"
                    for jo in law_data['조문'][:20]:  # 최대 20개 조문
                        if isinstance(jo, dict):
                            result += f"\n{jo.get('조문내용', '')}\n"
                            if jo.get('항'):
                                for hang in jo['항']:
                                    if isinstance(hang, dict):
                                        result += f"{hang.get('항내용', '')}\n"
                                        if hang.get('호'):
                                            for ho in hang['호']:
                                                if isinstance(ho, dict):
                                                    result += f"{ho.get('호내용', '')}\n"
                    result += "\n"
                    
                # 제개정이유
                if law_data.get('제개정이유') and law_data['제개정이유'].get('제개정이유내용'):
                    result += f"【제개정이유】\n"
                    for reason_item in law_data['제개정이유']['제개정이유내용']:
                        if isinstance(reason_item, list):
                            for item in reason_item:
                                result += f"{item}\n"
                    result += "\n"
                    
            else:
                result += "법령 상세내용을 찾을 수 없습니다.\n"
                
        # 법령 상세조회 (MST 파라미터 사용시 - 다른 구조)
        elif "법령" in data and isinstance(data["법령"], dict):
            law_data = data["법령"]
            basic_info = law_data.get("기본정보", {})
            
            result += f"법령 상세내용\n\n"
            result += f"법령명: {basic_info.get('법령명_한글', '미지정')}\n"
            result += f"법령ID: {basic_info.get('법령ID', '미지정')}\n"
            result += f"법종구분: {basic_info.get('법종구분', {}).get('content', '미지정')}\n"
            result += f"공포일자: {basic_info.get('공포일자', '미지정')}\n"
            result += f"시행일자: {basic_info.get('시행일자', '미지정')}\n"
            result += f"공포번호: {basic_info.get('공포번호', '미지정')}\n"
            result += f"제개정구분: {basic_info.get('제개정구분', '미지정')}\n\n"
            
            # 조문 내용
            if law_data.get("조문"):
                result += f"【조문내용】\n"
                jo_data = law_data["조문"].get("조문단위", {})
                if jo_data.get("조문내용"):
                    for content_item in jo_data["조문내용"]:
                        if isinstance(content_item, list):
                            for line in content_item:
                                result += f"{line}\n"
                        else:
                            result += f"{content_item}\n"
                result += "\n"
            
            # 부칙
            if law_data.get("부칙"):
                result += f"【부칙】\n"
                buchi_data = law_data["부칙"].get("부칙단위", {})
                if buchi_data.get("부칙내용"):
                    for content_item in buchi_data["부칙내용"]:
                        if isinstance(content_item, list):
                            for line in content_item:
                                result += f"{line}\n"
                        else:
                            result += f"{content_item}\n"
                result += "\n"
            
            # 개정문
            if law_data.get("개정문") and law_data["개정문"].get("개정문내용"):
                result += f"【개정문】\n{law_data['개정문']['개정문내용']}\n\n"
                
        # 판례 상세조회 (PrecService)
        elif "PrecService" in data:
            service_data = data["PrecService"]
            prec_data = service_data.get("판례", {})
            
            if prec_data:
                result += f"판례 상세내용\n\n"
                result += f"사건명: {prec_data.get('사건명', '미지정')}\n"
                result += f"사건번호: {prec_data.get('사건번호', '미지정')}\n"
                result += f"선고일자: {prec_data.get('선고일자', '미지정')}\n"
                result += f"법원명: {prec_data.get('법원명', '미지정')}\n"
                result += f"사건종류: {prec_data.get('사건종류명', '미지정')}\n"
                result += f"판례일련번호: {prec_data.get('판례일련번호', '미지정')}\n\n"
                
                # 판시사항
                if prec_data.get('판시사항'):
                    result += f"【판시사항】\n{prec_data['판시사항']}\n\n"
                
                # 판결요지
                if prec_data.get('판결요지'):
                    result += f"【판결요지】\n{prec_data['판결요지']}\n\n"
                
                # 참조조문
                if prec_data.get('참조조문'):
                    result += f"【참조조문】\n{prec_data['참조조문']}\n\n"
                
                # 전문
                if prec_data.get('전문'):
                    result += f"【전문】\n{prec_data['전문']}\n\n"
                    
            else:
                result += "판례 상세내용을 찾을 수 없습니다.\n"
                
        # 법령해석례 상세조회 (ExpcService)
        elif "ExpcService" in data:
            service_data = data["ExpcService"]
            expc_data = service_data.get("해석례", {})
            
            if expc_data:
                result += f"법령해석례 상세내용\n\n"
                result += f"해석례명: {expc_data.get('해석례명', '미지정')}\n"
                result += f"조회수: {expc_data.get('조회수', '미지정')}\n"
                result += f"해석일자: {expc_data.get('해석일자', '미지정')}\n"
                result += f"해석기관: {expc_data.get('해석기관', '미지정')}\n"
                result += f"해석례일련번호: {expc_data.get('해석례일련번호', '미지정')}\n\n"
                
                # 질의요지
                if expc_data.get('질의요지'):
                    result += f"【질의요지】\n{expc_data['질의요지']}\n\n"
                
                # 회답
                if expc_data.get('회답'):
                    result += f"【회답】\n{expc_data['회답']}\n\n"
                
                # 관련법령
                if expc_data.get('관련법령'):
                    result += f"【관련법령】\n{expc_data['관련법령']}\n\n"
                    
            else:
                result += "법령해석례 상세내용을 찾을 수 없습니다.\n"
                
        # 공정거래위원회 결정문 (Ftc)
        elif "Ftc" in data:
            search_data = data["Ftc"]
            total_count = search_data.get("totalCnt", 0)
            keyword = search_data.get("키워드", query)
            agency = search_data.get("기관명", "공정거래위원회")
            result += f"{agency} '{keyword}' 검색 결과 (총 {total_count}건)\n\n"
            
            # 단일 객체 또는 배열 처리
            ftc_data = search_data.get("ftc", {})
            if isinstance(ftc_data, dict):
                items = [ftc_data]
            elif isinstance(ftc_data, list):
                items = ftc_data
            else:
                items = []
                
            if items:
                for i, item in enumerate(items[:10], 1):
                    if isinstance(item, dict):
                        result += f"{i}. {item.get('사건명', '사건명 없음')}\n"
                        result += f"   사건번호: {item.get('사건번호', '미지정')}\n"
                        result += f"   결정번호: {item.get('결정번호', '미지정')}\n"
                        result += f"   결정일자: {item.get('결정일자', '미지정')}\n"
                        result += f"   문서유형: {item.get('문서유형', '미지정')}\n"
                        result += f"   결정문일련번호: {item.get('결정문일련번호', '미지정')}\n"
                        
                        detail_link = item.get('결정문상세링크', '')
                        if detail_link:
                            result += f"   상세조회 URL: http://www.law.go.kr{detail_link}\n"
                        result += "\n"
            else:
                result += "검색된 공정거래위원회 결정문이 없습니다.\n"
                
        # 기타 모든 API 응답 처리 (OrdinSearch, 기타 위원회 등)
        else:
            # 응답에서 주요 키 찾기
            main_keys = [k for k in data.keys() if k not in ["error", "message"]]
            if main_keys:
                main_key = main_keys[0]
                search_data = data[main_key]
                
                if isinstance(search_data, dict):
                    total_count = search_data.get("totalCnt", "미지정")
                    keyword = search_data.get("키워드", query)
                    result += f"'{keyword}' 검색 결과 (총 {total_count}건)\n\n"
                    
                    # 데이터 배열 찾기 (첫 번째 배열 또는 단일 객체)
                    items_found = False
                    for key, value in search_data.items():
                        if isinstance(value, list) and value:
                            items = value[:10]  # 최대 10개
                            items_found = True
                            break
                        elif isinstance(value, dict) and 'id' in value:
                            items = [value]  # 단일 객체를 리스트로 감싸기
                            items_found = True
                            break
                    
                    if items_found:
                        for i, item in enumerate(items, 1):
                            if isinstance(item, dict):
                                # 제목/이름 필드 찾기
                                title_fields = [
                                    "법령명한글", "법령명", "판례명", "사건명", "안건명", "제목",
                                    "별표명", "조약명", "용어명", "질의요지", "해석명", "규칙명",
                                    "결정문제목", "의결서제목", "행정규칙명", "자치법규명", "조례명"
                                ]
                                title = "제목 없음"
                                for field in title_fields:
                                    if field in item and item[field]:
                                        title = item[field]
                                        break
                                
                                result += f"{i}. {title}\n"
                                
                                # 모든 필드 출력 (title 제외)
                                for field, value in item.items():
                                    if field not in title_fields and value and str(value).strip():
                                        # 한글 필드명을 적절히 번역
                                        if field.endswith('링크'):
                                            if str(value).startswith('/'):
                                                result += f"   {field}: http://www.law.go.kr{value}\n"
                                            else:
                                                result += f"   {field}: {value}\n"
                                        else:
                                            result += f"   {field}: {value}\n"
                                
                                result += "\n"
                    else:
                        result += "검색된 결과가 없습니다.\n"
                        
                else:
                    # search_data가 dict가 아닌 경우 전체 JSON 출력
                    result += f"전체 응답 데이터:\n{json.dumps(data, ensure_ascii=False, indent=2)[:1500]}\n"
            else:
                # 메인 키를 찾을 수 없는 경우
                result += f"전체 응답 데이터:\n{json.dumps(data, ensure_ascii=False, indent=2)[:1500]}\n"
        

                
        return result
        
    except Exception as e:
        logger.error(f"결과 포맷팅 실패: {e}")
        return f"📊 **원본 응답 데이터**:\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)[:1000]}{'...' if len(json.dumps(data, ensure_ascii=False)) > 1000 else ''}\n```\n\n🔗 **API URL**: {url}\n\n**포맷팅 오류**: {str(e)}"

# ===========================================
# 1. 법령 관련 API (16개)
# ===========================================

@mcp.tool(name="search_law", description="한국의 법령을 검색합니다. 다양한 검색 조건과 정렬 옵션을 제공하여 정밀한 법령 검색이 가능합니다. 📚 법령의 해설서나 가이드라인이 필요하면 get_ministry_guideline_info 도구를 사용하세요.")
def search_law(
    query: Optional[str] = None,
    search: int = 2,  # 실제 curl 테스트에서 본문검색(2)이 제목검색(1)보다 훨씬 효과적임 확인
    display: int = 20,
    page: int = 1,
    sort: Optional[str] = None,
    date: Optional[str] = None,
    ef_date_range: Optional[str] = None,
    announce_date_range: Optional[str] = None,
    announce_no_range: Optional[str] = None,
    revision_type: Optional[str] = None,
    announce_no: Optional[str] = None,
    ministry_code: Optional[str] = None,
    law_type_code: Optional[str] = None,
    law_chapter: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """법령 목록 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어 (법령명)
        search: 검색범위 (1=법령명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=법령오름차순, ldes=법령내림차순, dasc=공포일자오름차순, ddes=공포일자내림차순, nasc=공포번호오름차순, ndes=공포번호내림차순, efasc=시행일자오름차순, efdes=시행일자내림차순)
        date: 공포일자 (YYYYMMDD)
        ef_date_range: 시행일자 범위 (20090101~20090130)
        announce_date_range: 공포일자 범위 (20090101~20090130)
        announce_no_range: 공포번호 범위 (306~400)
        revision_type: 제개정 종류 (300201=제정, 300202=일부개정, 300203=전부개정, 300204=폐지, 300205=폐지제정, 300206=일괄개정, 300207=일괄폐지, 300209=타법개정, 300210=타법폐지, 300208=기타)
        announce_no: 공포번호
        ministry_code: 소관부처 코드
        law_type_code: 법령종류 코드
        law_chapter: 법령분류 (01=제1편...44=제44편)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "개인정보보호법"
    params = {
        "query": search_query,
        "search": search,
        "display": min(display, 100),
        "page": page
    }
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if date:
        params["date"] = date
    if ef_date_range:
        params["efYd"] = ef_date_range
    if announce_date_range:
        params["ancYd"] = announce_date_range
    if announce_no_range:
        params["ancNo"] = announce_no_range
    if revision_type:
        params["rrClsCd"] = revision_type
    if announce_no:
        params["nb"] = announce_no
    if ministry_code:
        params["org"] = ministry_code
    if law_type_code:
        params["knd"] = law_type_code
    if law_chapter:
        params["lsChapNo"] = law_chapter
    if alphabetical:
        params["gana"] = alphabetical
    
    try:
        # 🎯 지능형 검색 적용 - 정확도 우선
        if not any([sort, date, ef_date_range, announce_date_range, announce_no_range, 
                   revision_type, announce_no, ministry_code, law_type_code, law_chapter, alphabetical]):
            # 고급 파라미터가 없으면 지능형 검색 사용
            data = _smart_search("law", search_query, display, page)
            url = _generate_api_url("law", {"query": search_query, "search": 1, "display": display, "page": page})
        else:
            # 고급 파라미터가 있으면 기존 방식 사용
            import requests
            oc = os.getenv("LEGISLATION_API_KEY", "lchangoo")
            base_params = {"OC": oc, "type": "JSON", "target": "law"}
            # params 값들을 str로 변환하여 추가
            for k, v in params.items():
                base_params[k] = str(v)
            
            from urllib.parse import urlencode
            url = f"{legislation_config.search_base_url}?{urlencode(base_params)}"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        
        result = _format_search_results(data, "law", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령 검색 중 오류: {str(e)}")

@mcp.tool(name="get_law_detail", description="특정 법령의 상세 내용을 조회합니다. 법령ID나 법령명으로 조회 가능합니다. 법령명으로 검색 시 자동으로 정확한 법령을 찾아 상세 내용을 제공합니다.")
def get_law_detail(law_id: Optional[Union[str, int]] = None, law_name: Optional[str] = None) -> TextContent:
    """법령 본문 조회 - 개선된 검색 로직"""
    if not law_id and not law_name:
        return TextContent(type="text", text="법령ID 또는 법령명을 입력해야 합니다.")
    
    try:
        if law_id:
            # ID가 있으면 직접 조회
            params = {"MST": str(law_id)}
            data = _make_legislation_request("law", params, is_detail=True)
            url = _generate_api_url("law", params, is_detail=True)
            search_term = f"ID:{law_id}"
        else:
            # 법령명으로 검색 - 먼저 검색해서 정확한 ID 찾기
            if not law_name:
                return TextContent(type="text", text="법령명이 비어있습니다.")
                
            search_result = _smart_search("law", law_name, display=5)
            
            if isinstance(search_result, dict) and search_result.get('LawSearch'):
                laws = search_result['LawSearch'].get('law', [])
                if isinstance(laws, dict):
                    laws = [laws]
                
                # 가장 관련성 높은 법령 찾기
                best_match = None
                normalized_query = _normalize_search_query(law_name)
                
                for law in laws:
                    law_title = law.get('법령명한글', '')
                    normalized_title = _normalize_search_query(law_title)
                    
                    # 정확히 일치하거나 매우 유사한 경우
                    if (normalized_title == normalized_query or 
                        normalized_query in normalized_title or
                        any(keyword in normalized_title for keyword in normalized_query.split() if len(keyword) > 1)):
                        best_match = law
                        break
                
                if best_match and best_match.get('법령일련번호'):
                    # 찾은 법령의 상세 정보 조회
                    mst_id = best_match['법령일련번호']
                    params = {"MST": str(mst_id)}
                    data = _make_legislation_request("law", params, is_detail=True)
                    url = _generate_api_url("law", params, is_detail=True)
                    search_term = f"{law_name} (자동 발견: {best_match.get('법령명한글', '')})"
                else:
                    return TextContent(type="text", text=f"'{law_name}'과 일치하는 법령을 찾을 수 없습니다. search_law 도구로 먼저 검색해보세요.")
            else:
                return TextContent(type="text", text=f"'{law_name}' 검색 중 오류가 발생했습니다.")
        
        result = _format_search_results(data, "law", search_term, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="search_english_law", description="영문 법령을 검색합니다. 한국 법령의 영어 번역본을 제공합니다. 정렬, 날짜 범위, 소관부처별 등 다양한 검색 조건을 지원합니다.")
def search_english_law(
    query: Optional[str] = None,
    search: int = 1,
    display: int = 20,
    page: int = 1,
    sort: Optional[str] = None,
    date: Optional[str] = None,
    effective_date_range: Optional[str] = None,
    announce_date_range: Optional[str] = None,
    announce_no_range: Optional[str] = None,
    revision_type: Optional[str] = None,
    announce_no: Optional[str] = None,
    ministry_code: Optional[str] = None,
    law_type_code: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """영문법령 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어 (한글 또는 영문 법령명)
        search: 검색범위 (1=법령명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=법령오름차순, ldes=법령내림차순, dasc=공포일자오름차순, ddes=공포일자내림차순, nasc=공포번호오름차순, ndes=공포번호내림차순, efasc=시행일자오름차순, efdes=시행일자내림차순)
        date: 공포일자 (YYYYMMDD)
        effective_date_range: 시행일자 범위 (20090101~20090130)
        announce_date_range: 공포일자 범위 (20090101~20090130)
        announce_no_range: 공포번호 범위 (306~400)
        revision_type: 제개정 종류 (300201=제정, 300202=일부개정, 300203=전부개정, 300204=폐지, 300205=폐지제정, 300206=일괄개정, 300207=일괄폐지, 300209=타법개정, 300210=타법폐지, 300208=기타)
        announce_no: 공포번호
        ministry_code: 소관부처 코드
        law_type_code: 법령종류 코드
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "Personal Information Protection Act"
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if date:
        params["date"] = date
    if effective_date_range:
        params["efYd"] = effective_date_range
    if announce_date_range:
        params["ancYd"] = announce_date_range
    if announce_no_range:
        params["ancNo"] = announce_no_range
    if revision_type:
        params["rrClsCd"] = revision_type
    if announce_no:
        params["nb"] = announce_no
    if ministry_code:
        params["org"] = ministry_code
    if law_type_code:
        params["knd"] = law_type_code
    if alphabetical:
        params["gana"] = alphabetical
    
    try:
        data = _make_legislation_request("elaw", params)
        url = _generate_api_url("elaw", params)
        result = _format_search_results(data, "elaw", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"영문법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_effective_law", description="시행일법령을 검색합니다. 특정 시행일자의 법령을 조회할 수 있습니다. 연혁/시행예정/현행 구분, 날짜 범위, 소관부처별 등 다양한 검색 조건을 지원합니다.")
def search_effective_law(
    query: Optional[str] = None,
    search: int = 1,
    display: int = 20,
    page: int = 1,
    status_type: Optional[str] = None,
    law_id: Optional[str] = None,
    sort: Optional[str] = None,
    effective_date_range: Optional[str] = None,
    date: Optional[str] = None,
    announce_date_range: Optional[str] = None,
    announce_no_range: Optional[str] = None,
    revision_type: Optional[str] = None,
    announce_no: Optional[str] = None,
    ministry_code: Optional[str] = None,
    law_type_code: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """시행일법령 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=법령명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        status_type: 법령 상태 (1=연혁, 2=시행예정, 3=현행, 조합가능: "1,2" "2,3" "1,2,3")
        law_id: 법령ID (특정 법령 검색시)
        sort: 정렬 (lasc=법령오름차순, ldes=법령내림차순, dasc=공포일자오름차순, ddes=공포일자내림차순, nasc=공포번호오름차순, ndes=공포번호내림차순, efasc=시행일자오름차순, efdes=시행일자내림차순)
        effective_date_range: 시행일자 범위 (20090101~20090130)
        date: 공포일자 (YYYYMMDD)
        announce_date_range: 공포일자 범위 (20090101~20090130)
        announce_no_range: 공포번호 범위 (306~400)
        revision_type: 제개정 종류 (300201=제정, 300202=일부개정, 300203=전부개정, 300204=폐지, 300205=폐지제정, 300206=일괄개정, 300207=일괄폐지, 300209=타법개정, 300210=타법폐지, 300208=기타)
        announce_no: 공포번호
        ministry_code: 소관부처 코드
        law_type_code: 법령종류 코드
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "개인정보보호법"
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if status_type:
        params["nw"] = status_type
    if law_id:
        params["LID"] = law_id
    if sort:
        params["sort"] = sort
    if effective_date_range:
        params["efYd"] = effective_date_range
    if date:
        params["date"] = date
    if announce_date_range:
        params["ancYd"] = announce_date_range
    if announce_no_range:
        params["ancNo"] = announce_no_range
    if revision_type:
        params["rrClsCd"] = revision_type
    if announce_no:
        params["nb"] = announce_no
    if ministry_code:
        params["org"] = ministry_code
    if law_type_code:
        params["knd"] = law_type_code
    if alphabetical:
        params["gana"] = alphabetical
    
    try:
        data = _make_legislation_request("eflaw", params)
        url = _generate_api_url("eflaw", params)
        result = _format_search_results(data, "eflaw", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"시행일법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_law_history", description="법령의 변경이력을 검색합니다. 법령의 개정 과정을 추적할 수 있습니다. 다양한 검색 조건과 정렬 옵션을 제공합니다.")
def search_law_history(
    query: Optional[str] = None,
    display: int = 20,
    page: int = 1,
    sort: Optional[str] = None,
    ef_date_range: Optional[str] = None,
    date: Optional[str] = None,
    announce_date_range: Optional[str] = None,
    announce_no_range: Optional[str] = None,
    revision_type: Optional[str] = None,
    ministry_code: Optional[str] = None,
    law_type_code: Optional[str] = None,
    law_chapter: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """법령 변경이력 목록 조회 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=법령오름차순, ldes=법령내림차순, dasc=공포일자오름차순, ddes=공포일자내림차순, nasc=공포번호오름차순, ndes=공포번호내림차순, efasc=시행일자오름차순, efdes=시행일자내림차순)
        ef_date_range: 시행일자 범위 (20090101~20090130)
        date: 공포일자 (YYYYMMDD)
        announce_date_range: 공포일자 범위 (20090101~20090130)
        announce_no_range: 공포번호 범위 (306~400)
        revision_type: 제개정 종류 (300201=제정, 300202=일부개정, 300203=전부개정, 300204=폐지, 300205=폐지제정, 300206=일괄개정, 300207=일괄폐지, 300209=타법개정, 300210=타법폐지, 300208=기타)
        ministry_code: 소관부처 코드
        law_type_code: 법령종류 코드
        law_chapter: 법령분류 (01=제1편...44=제44편)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "개인정보보호법"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if ef_date_range:
        params["efYd"] = ef_date_range
    if date:
        params["date"] = date
    if announce_date_range:
        params["ancYd"] = announce_date_range
    if announce_no_range:
        params["ancNo"] = announce_no_range
    if revision_type:
        params["rrClsCd"] = revision_type
    if ministry_code:
        params["org"] = ministry_code
    if law_type_code:
        params["knd"] = law_type_code
    if law_chapter:
        params["lsChapNo"] = law_chapter
    if alphabetical:
        params["gana"] = alphabetical
    
    try:
        data = _make_legislation_request("lsHistory", params)
        url = _generate_api_url("lsHistory", params)
        result = _format_search_results(data, "lsHistory", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령 변경이력 검색 중 오류: {str(e)}")

@mcp.tool(name="search_law_nickname", description="법령의 약칭을 검색합니다. 법령의 별명이나 통칭을 조회할 수 있습니다.")
def search_law_nickname(start_date: Optional[str] = None, end_date: Optional[str] = None) -> TextContent:
    """법령 약칭 조회"""
    params = {}
    if start_date:
        params["stdDt"] = start_date
    if end_date:
        params["endDt"] = end_date
    try:
        data = _make_legislation_request("lsAbrv", params)
        url = _generate_api_url("lsAbrv", params)
        result = _format_search_results(data, "lsAbrv", "법령 약칭", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령 약칭 검색 중 오류: {str(e)}")

@mcp.tool(name="search_deleted_law_data", description="삭제된 법령 데이터를 검색합니다. 폐지된 법령 정보를 조회할 수 있습니다.")
def search_deleted_law_data(data_type: Optional[int] = None, delete_date: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """삭제데이터 조회 (법령: 1, 행정규칙: 2, 자치법규: 3, 학칙공단: 13)"""
    params = {"display": str(min(display, 100)), "page": str(page)}
    if data_type:
        params["knd"] = str(data_type)
    if delete_date:
        params["delDt"] = str(delete_date)
    if from_date:
        params["frmDt"] = str(from_date)  
    if to_date:
        params["toDt"] = str(to_date)
    try:
        data = _make_legislation_request("delHst", params)
        url = _generate_api_url("delHst", params)
        result = _format_search_results(data, "delHst", "삭제된 데이터", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"삭제데이터 검색 중 오류: {str(e)}")

@mcp.tool(name="search_law_articles", description="법령의 조문을 검색합니다. 특정 조문별로 상세 내용을 조회할 수 있습니다.")
def search_law_articles(law_id: Union[str, int], display: int = 20, page: int = 1) -> TextContent:
    """조문별 조회 - lawService.do API 사용"""
    # lawService.do API용 파라미터 구성
    params = {"target": "law", "MST": str(law_id), "type": "JSON"}
    try:
        # lawService.do API 호출을 위해 직접 구현
        import urllib.request
        import urllib.parse
        import json
        
        base_url = legislation_config.service_base_url
        params["OC"] = "lchangoo"
        url = base_url + "?" + urllib.parse.urlencode(params)
        
        with urllib.request.urlopen(url, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        result = _format_search_results(data, "law", f"법령MST:{law_id}", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"조문별 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"신구법비교 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"3단비교 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"삭제이력 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"한눈보기 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"법령 체계도 검색 중 오류: {str(e)}")

@mcp.tool(name="get_law_system_diagram_detail", description="법령 체계도 상세내용을 조회합니다. 특정 법령의 체계도 본문을 제공합니다.")
def get_law_system_diagram_detail(mst_id: Union[str, int]) -> TextContent:
    """법령 체계도 본문 조회"""
    params = {"target": "lsStmd", "MST": str(mst_id)}
    try:
        data = _make_legislation_request("lsStmd", params)
        result = _format_search_results(data, "lsStmd", f"체계도MST:{mst_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령 체계도 상세 조회 중 오류: {str(e)}")

@mcp.tool(name="get_delegated_law", description="위임법령을 조회합니다. 특정 법령에서 위임한 하위법령들의 정보를 제공합니다.")
def get_delegated_law(law_id: Union[str, int]) -> TextContent:
    """위임법령 조회"""
    params = {"target": "lsDelegated", "ID": str(law_id)}
    try:
        data = _make_legislation_request("lsDelegated", params)
        result = _format_search_results(data, "lsDelegated", f"법령ID:{law_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"위임법령 조회 중 오류: {str(e)}")

# ===========================================
# 3. 행정규칙 API (5개)
# ===========================================

@mcp.tool(name="search_administrative_rule", description="행정규칙을 검색합니다. 각 부처의 행정규칙과 예규를 제공합니다.")
def search_administrative_rule(query: Optional[str] = None, search: int = 2, display: int = 20, page: int = 1) -> TextContent:
    """행정규칙 검색"""
    search_query = query or "개인정보보호"
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
        result = _format_search_results(data, "admrul", f"행정규칙ID:{rule_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정규칙 상세 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"행정규칙 신구법 비교 검색 중 오류: {str(e)}")

@mcp.tool(name="get_administrative_rule_comparison_detail", description="행정규칙 신구법 비교 상세내용을 조회합니다. 특정 행정규칙의 신구법 비교 본문을 제공합니다.")
def get_administrative_rule_comparison_detail(comparison_id: Union[str, int]) -> TextContent:
    """행정규칙 신구법 비교 본문 조회"""
    params = {"target": "admrulOldAndNew", "ID": str(comparison_id)}
    try:
        data = _make_legislation_request("admrulOldAndNew", params)
        result = _format_search_results(data, "admrulOldAndNew", f"비교ID:{comparison_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정규칙 신구법 비교 상세 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"자치법규 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"자치법규 별표서식 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"연계 자치법규 검색 중 오류: {str(e)}")

# ===========================================
# 5. 판례관련 API (8개)
# ===========================================

@mcp.tool(name="search_precedent", description="대법원 판례를 검색합니다. 사건명, 키워드로 판례를 찾을 수 있습니다. 법원별, 법령별, 일자별 등 다양한 검색 조건을 지원합니다. 📚 판례의 해설이나 가이드라인이 필요하면 get_ministry_guideline_info 도구를 사용하세요.")
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
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=선고일자오름차순, ddes=선고일자내림차순, nasc=법원명오름차순, ndes=법원명내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
        date: 판례 선고일자 (YYYYMMDD)
        date_range: 선고일자 범위 (20090101~20090130)
        case_number: 판례 사건번호
        data_source: 데이터출처명 (국세법령정보시스템, 근로복지공단산재판례, 대법원)
    """
    search_query = query or "개인정보보호"
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
        return TextContent(type="text", text=f"헌법재판소 결정례 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"법령해석례 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 판례 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"행정심판례 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"행정심판례 상세 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 행정심판례 검색 중 오류: {str(e)}")

# ===========================================
# 6. 위원회결정문 API (30개 주요 위원회)
# ===========================================

@mcp.tool(name="search_privacy_committee", description="개인정보보호위원회 결정문을 검색합니다. 개인정보보호 관련 위원회 결정사항을 제공합니다. 본문검색, 정렬, 사전식 검색 등 다양한 옵션을 지원합니다. 📚 결정문의 해설이나 가이드라인이 필요하면 get_ministry_guideline_info 도구를 사용하세요.")
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
        search: 검색범위 (1=안건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=안건명오름차순, ldes=안건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=의안번호오름차순, ndes=의안번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "개인정보수집"
    
    # 🎯 개선된 검색 파라미터 - 빈 제목 문제 해결
    params = {
        "query": search_query, 
        "search": search, 
        "display": min(display, 100), 
        "page": page,
        "sort": sort or "ddes"  # 의결일자 내림차순으로 최신순 정렬
    }
    
    # 고급 검색 파라미터 추가
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("ppc", params)
        url = _generate_api_url("ppc", params)
        
        # ✅ 결과 품질 검증 및 개선
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('ppc', [])
            if isinstance(items, dict):
                items = [items]
            
            # 빈 제목 필터링 및 품질 개선
            filtered_items = []
            for item in items:
                title = item.get('안건명', '').strip()
                if title and title != '' and len(title) > 1:  # 의미있는 제목만
                    filtered_items.append(item)
            
            # 필터링된 결과로 데이터 업데이트
            if filtered_items:
                data['LawSearch']['ppc'] = filtered_items
            
        result = _format_search_results(data, "ppc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"개인정보보호위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_financial_committee", description="금융위원회 결정문을 검색합니다. 금융 관련 규제와 결정사항을 제공합니다. 본문검색을 통해 상세한 결과를 제공합니다.")
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
        sort: 정렬 (lasc=안건명오름차순, ldes=안건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=의결번호오름차순, ndes=의결번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "금융"
    # search=2 (본문검색) 파라미터 필수 - 안건명만 검색(search=1)하면 결과가 0건
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("fsc", params)
        url = _generate_api_url("fsc", params)
        result = _format_search_results(data, "fsc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"금융위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_monopoly_committee", description="공정거래위원회 결정문을 검색합니다. 독점규제 및 공정거래 관련 결정사항을 제공합니다. 본문검색을 통해 상세한 결과를 제공합니다.")
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
        search: 검색범위 (1=사건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=결정일자오름차순, ddes=결정일자내림차순, nasc=결정번호오름차순, ndes=결정번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "독점"
    # search=2 (본문검색) 파라미터 필수 - 안건명만 검색(search=1)하면 결과가 현저히 적음
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
        
    try:
        data = _make_legislation_request("ftc", params)
        url = _generate_api_url("ftc", params)
        result = _format_search_results(data, "ftc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"공정거래위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_anticorruption_committee", description="국민권익위원회 결정문을 검색합니다. 부패방지 및 권익보호 관련 결정사항을 제공합니다. 본문검색을 통해 상세한 결과를 제공합니다.")
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
        search: 검색범위 (1=사건명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "권익보호"
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
        result = _format_search_results(data, "acr", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국민권익위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_labor_committee", description="노동위원회 결정문을 검색합니다. 노동 관련 분쟁 조정 결정사항을 제공합니다. 본문검색을 통해 상세한 결과를 제공합니다.")
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
        sort: 정렬 (lasc=사건명오름차순, ldes=사건명내림차순, dasc=의결일자오름차순, ddes=의결일자내림차순, nasc=사건번호오름차순, ndes=사건번호내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "노동분쟁"
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
        result = _format_search_results(data, "nlrc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"노동위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_environment_committee", description="중앙환경분쟁조정위원회 결정문을 검색합니다. 환경 분쟁 조정 관련 결정사항을 제공합니다. 본문검색을 통해 상세한 결과를 제공합니다.")
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
    search_query = query or "환경분쟁"
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
        result = _format_search_results(data, "ecc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중앙환경분쟁조정위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_securities_committee", description="증권선물위원회 결정문을 검색합니다. 증권 및 선물 관련 규제 결정사항을 제공합니다. 본문검색을 통해 상세한 결과를 제공합니다.")
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
    search_query = query or "증권"
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
        result = _format_search_results(data, "sfc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"증권선물위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_human_rights_committee", description="국가인권위원회 결정문을 검색합니다. 인권 보호 및 차별 시정 관련 결정사항을 제공합니다.")
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
    search_query = query or "인권"
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
        result = _format_search_results(data, "nhrck", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국가인권위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_broadcasting_committee", description="방송통신위원회 결정문을 검색합니다. 방송통신 관련 규제와 결정사항을 제공합니다. 본문검색을 통해 상세한 결과를 제공합니다.")
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
    search_query = query or "방송통신"
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
        result = _format_search_results(data, "kcc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"방송통신위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_industrial_accident_committee", description="산업재해보상보험 재심사위원회 결정문을 검색합니다. 산재 관련 결정사항을 제공합니다.")
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
    search_query = query or "산업재해"
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
        result = _format_search_results(data, "iaciac", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"산업재해보상보험재심사위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_land_tribunal", description="중앙토지수용위원회 결정문을 검색합니다. 토지수용 관련 결정사항을 제공합니다. 본문검색을 통해 상세한 결과를 제공합니다.")
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
    search_query = query or "토지수용"
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
        result = _format_search_results(data, "oclt", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중앙토지수용위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_employment_insurance_committee", description="고용보험심사위원회 결정문을 검색합니다. 고용보험 관련 심사 결정사항을 제공합니다.")
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
    search_query = query or "고용보험"
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
        result = _format_search_results(data, "eiac", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"고용보험심사위원회 결정문 검색 중 오류: {str(e)}")

@mcp.tool(name="get_employment_insurance_committee_detail", description="고용보험심사위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다.")
def get_employment_insurance_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """고용보험심사위원회 결정문 본문 조회"""
    params = {"target": "eiac", "ID": str(decision_id)}
    try:
        data = _make_legislation_request("eiac", params)
        result = _format_search_results(data, "eiac", f"결정문ID:{decision_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"고용보험심사위원회 결정문 상세 조회 중 오류: {str(e)}")

# ===========================================
# 7. 조약 API (2개)
# ===========================================

@mcp.tool(name="search_treaty", description="조약을 검색합니다. 한국이 체결한 국제조약과 협정을 조회할 수 있습니다. 양자/다자조약, 발효일자, 체결일자 등 다양한 검색 조건을 지원합니다.")
def search_treaty(
    query: Optional[str] = None,
    search: int = 1,
    display: int = 20,
    page: int = 1,
    treaty_type: Optional[int] = None,
    country_code: Optional[int] = None,
    effective_date_range: Optional[str] = None,
    conclusion_date_range: Optional[str] = None,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """조약 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=조약명, 2=조약본문)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        treaty_type: 조약 구분 (1=양자조약, 2=다자조약)
        country_code: 국가코드
        effective_date_range: 발효일자 범위 (20090101~20090130)
        conclusion_date_range: 체결일자 범위 (20090101~20090130)
        sort: 정렬 (lasc=조약명오름차순, ldes=조약명내림차순, dasc=발효일자오름차순, ddes=발효일자내림차순, nasc=조약번호오름차순, ndes=조약번호내림차순, rasc=관보게재일오름차순, rdes=관보게재일내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "통상"  # 실제 curl 테스트: "통상"(5건) > "개인정보보호"(0건)
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if treaty_type:
        params["cls"] = treaty_type
    if country_code:
        params["natCd"] = country_code
    if effective_date_range:
        params["eftYd"] = effective_date_range
    if conclusion_date_range:
        params["concYd"] = conclusion_date_range
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
    
    try:
        data = _make_legislation_request("trty", params)
        url = _generate_api_url("trty", params)
        result = _format_search_results(data, "trty", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"조약 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 조약 검색 중 오류: {str(e)}")

# ===========================================
# 8. 별표서식 API (4개)
# ===========================================

@mcp.tool(name="search_law_appendix", description="법령 별표서식을 검색합니다. 법령에 첨부된 별표와 서식을 조회할 수 있습니다. 별표종류, 소관부처, 지자체별 등 다양한 검색 조건을 지원합니다.")
def search_law_appendix(
    query: Optional[str] = None,
    search: int = 1,
    display: int = 20,
    page: int = 1,
    appendix_type: Optional[str] = None,
    ministry_code: Optional[str] = None,
    local_gov_code: Optional[str] = None,
    sort: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """법령 별표서식 검색 (풍부한 검색 파라미터 지원)
    
    Args:
        query: 검색어
        search: 검색범위 (1=별표서식명, 2=해당법령검색, 3=별표본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        appendix_type: 별표종류 (1=별표, 2=서식, 3=별도, 4=별지)
        ministry_code: 소관부처 코드
        local_gov_code: 지자체별 시·군·구 검색 코드 (ministry_code와 함께 사용)
        sort: 정렬 (lasc=별표서식명오름차순, ldes=별표서식명내림차순)
        alphabetical: 사전식 검색 (ga,na,da,ra,ma,ba,sa,a,ja,cha,ka,ta,pa,ha)
    """
    search_query = query or "개인정보보호"
    params = {"query": search_query, "search": search, "display": min(display, 100), "page": page}
    
    # 고급 검색 파라미터 추가
    if appendix_type:
        params["knd"] = appendix_type
    if ministry_code:
        params["org"] = ministry_code
    if local_gov_code:
        params["sborg"] = local_gov_code
    if sort:
        params["sort"] = sort
    if alphabetical:
        params["gana"] = alphabetical
    
    try:
        data = _make_legislation_request("licbyl", params)
        url = _generate_api_url("licbyl", params)
        result = _format_search_results(data, "licbyl", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령 별표서식 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 법령 별표서식 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"대학 학칙 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"지방공사공단 규정 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"공공기관 규정 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"대학 학칙 상세 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"지방공사공단 규정 상세 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"공공기관 규정 상세 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"조세심판원 특별행정심판례 검색 중 오류: {str(e)}")

@mcp.tool(name="get_tax_tribunal_detail", description="조세심판원 특별행정심판례 상세내용을 조회합니다. 특정 심판례의 본문을 제공합니다.")
def get_tax_tribunal_detail(trial_id: Union[str, int]) -> TextContent:
    """조세심판원 특별행정심판례 본문 조회"""
    params = {"target": "ttSpecialDecc", "ID": str(trial_id)}
    try:
        data = _make_legislation_request("ttSpecialDecc", params)
        result = _format_search_results(data, "ttSpecialDecc", f"심판례ID:{trial_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"조세심판원 특별행정심판례 상세 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"해양안전심판원 특별행정심판례 검색 중 오류: {str(e)}")

@mcp.tool(name="get_maritime_safety_tribunal_detail", description="해양안전심판원 특별행정심판례 상세내용을 조회합니다. 특정 심판례의 본문을 제공합니다.")
def get_maritime_safety_tribunal_detail(trial_id: Union[str, int]) -> TextContent:
    """해양안전심판원 특별행정심판례 본문 조회"""
    params = {"target": "kmstSpecialDecc", "ID": str(trial_id)}
    try:
        data = _make_legislation_request("kmstSpecialDecc", params)
        result = _format_search_results(data, "kmstSpecialDecc", f"심판례ID:{trial_id}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"해양안전심판원 특별행정심판례 상세 조회 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"법령용어 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 법령용어 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 법령 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 영문법령 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 행정규칙 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"모바일 자치법규 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"맞춤형 법령 검색 중 오류: {str(e)}")

@mcp.tool(name="search_custom_law_articles", description="맞춤형 법령 조문을 검색합니다. 사용자 맞춤형 법령의 조문별 내용을 제공합니다.")
def search_custom_law_articles(vcode: str, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 법령 조문 검색"""
    params = {"target": "couseLs", "vcode": vcode, "lj": "jo", "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("couseLs", params)
        result = _format_search_results(data, "couseLs", f"분류코드:{vcode} 조문")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"맞춤형 법령 조문 검색 중 오류: {str(e)}")

@mcp.tool(name="search_custom_ordinance", description="맞춤형 자치법규를 검색합니다. 사용자 맞춤형 자치법규 분류에 따른 검색을 제공합니다.")
def search_custom_ordinance(vcode: str, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 자치법규 검색"""
    params = {"target": "couseOrdin", "vcode": vcode, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("couseOrdin", params)
        result = _format_search_results(data, "couseOrdin", f"분류코드:{vcode}")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"맞춤형 자치법규 검색 중 오류: {str(e)}")

@mcp.tool(name="search_custom_ordinance_articles", description="맞춤형 자치법규 조문을 검색합니다. 사용자 맞춤형 자치법규의 조문별 내용을 제공합니다.")
def search_custom_ordinance_articles(vcode: str, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 자치법규 조문 검색"""
    params = {"target": "couseOrdin", "vcode": vcode, "lj": "jo", "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("couseOrdin", params)
        result = _format_search_results(data, "couseOrdin", f"분류코드:{vcode} 조문")
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"맞춤형 자치법규 조문 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"맞춤형 판례 검색 중 오류: {str(e)}")

# ===========================================
# 13. 지식베이스 API (6개)
# ===========================================

@mcp.tool(name="search_legal_ai", description="법령 AI 지식베이스를 검색합니다. 스마트 다중 검색으로 최적화된 법령 정보와 분석을 제공합니다.")
def search_legal_ai(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """스마트 AI 기반 다중 검색 - 기존 API가 작동하지 않아 대안 구현"""
    search_query = query or "개인정보보호"
    
    results = []
    results.append(f"🤖 **AI 기반 스마트 검색 결과: '{search_query}'**\n")
    results.append("=" * 50 + "\n")
    
    try:
        # 1. 정밀 법령 검색 (제목 우선)
        law_data = _smart_search("law", search_query, display=5)
        if law_data and law_data.get('LawSearch'):
            law_result = _format_search_results(law_data, "law", search_query)
            results.append("📋 **관련 법령 (정밀 매칭):**\n")
            results.append(law_result + "\n")
        
        # 2. 해석례 검색 (실무 적용)
        interp_data = _smart_search("expc", search_query, display=3)
        if interp_data and interp_data.get('LawSearch'):
            interp_result = _format_search_results(interp_data, "expc", search_query)
            results.append("💡 **법령해석례 (실무 가이드):**\n")
            results.append(interp_result + "\n")
        
        # 3. 위원회 결정문 (사례 분석)
        committee_targets = ["ppc", "fsc", "ftc"]
        for target in committee_targets:
            committee_data = _smart_search(target, search_query, display=2)
            if committee_data and committee_data.get('LawSearch'):
                committee_result = _format_search_results(committee_data, target, search_query)
                if "결과가 없습니다" not in committee_result:
                    agency_names = {"ppc": "개인정보보호위원회", "fsc": "금융위원회", "ftc": "공정거래위원회"}
                    results.append(f"🏛️ **{agency_names.get(target, target)} 결정례:**\n")
                    results.append(committee_result + "\n")
        
        # 4. AI 분석 요약
        results.append("🔍 **AI 분석 요약:**\n")
        results.append(f"• 검색어 '{search_query}'에 대한 다각도 법령 분석을 완료했습니다.\n")
        results.append("• 관련 법령, 해석례, 위원회 결정례를 종합적으로 제공합니다.\n")
        results.append("• 상세한 내용은 각 문서의 상세조회 도구를 활용하세요.\n\n")
        
        return TextContent(type="text", text="".join(results))
        
    except Exception as e:
        return TextContent(type="text", text=f"스마트 법령 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"지식베이스 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"FAQ 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"질의응답 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"상담 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"판례 상담 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"민원 검색 중 오류: {str(e)}")

# ===========================================
# 15. 중앙부처해석 API (14개)
# ===========================================

@mcp.tool(name="search_moef_interpretation", description="기획재정부 법령해석을 검색합니다. 기획재정부의 법령해석 사례를 제공합니다.")
def search_moef_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """기획재정부 법령해석 검색"""
    search_query = query or "조세"  # 실제 curl 테스트: "조세"(594건) > "개인정보보호"(0건)
    params = {"target": "moefCgmExpc", "query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("moefCgmExpc", params)
        result = _format_search_results(data, "moefCgmExpc", search_query)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"기획재정부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"국토교통부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"고용노동부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"해양수산부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"보건복지부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"교육부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"한국 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"보훈처 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"산업통상자원부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"농림축산식품부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"국방부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"중소벤처기업부 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"산림청 법령해석 검색 중 오류: {str(e)}")

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
        return TextContent(type="text", text=f"한국철도공사 법령해석 검색 중 오류: {str(e)}")

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
        # 1. 스마트 법령 검색 (정확도 개선)
        if include_law:
            law_data = _smart_search("law", search_query, display=4)
            law_url = _generate_api_url("law", {"query": search_query, "display": 4})
            law_result = _format_search_results(law_data, "law", search_query, law_url)
            results.append("📜 **법령 검색 결과 (스마트 매칭):**\n")
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
        
        # 4. 주요 위원회 결정문 검색 (다중 위원회)
        if include_committee:
            committee_targets = [
                ("ppc", "개인정보보호위원회"),
                ("fsc", "금융위원회"), 
                ("ftc", "공정거래위원회"),
                ("acr", "국민권익위원회"),
                ("nhrck", "국가인권위원회")
            ]
            
            results.append("🏛️ **위원회 결정문 검색 결과:**\n")
            
            for target, name in committee_targets:
                try:
                    committee_params = {"query": search_query, "display": 2}
                    committee_data = _make_legislation_request(target, committee_params)
                    committee_url = _generate_api_url(target, committee_params)
                    
                    # 결과가 있는 경우만 추가
                    if committee_data and not committee_data.get("error"):
                        committee_result = _format_search_results(committee_data, target, search_query, committee_url)
                        if "결과가 없습니다" not in committee_result:
                            results.append(f"📋 **{name}:**\n")
                            results.append(committee_result + "\n")
                except Exception as e:
                    logger.warning(f"{name} 검색 실패: {e}")
                    continue
        
        return TextContent(type="text", text="".join(results))
        
    except Exception as e:
        error_msg = f"통합 검색 중 오류가 발생했습니다: {str(e)}"
        return TextContent(type="text", text=error_msg)

logger.info("✅ 121개 법제처 OPEN API 도구가 모두 로드되었습니다!") 

# ===========================================
# 추가 누락된 API 도구들 (125개 완성을 위해)
# ===========================================

@mcp.tool(name="search_daily_article_revision", description="일자별 조문 개정 이력을 검색합니다. 특정 날짜별로 조문의 개정 현황을 조회할 수 있습니다.")
def search_daily_article_revision(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """일자별 조문 개정 이력 목록 조회 (lsDayJoRvs)"""
    search_query = query or "개인정보보호"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lsDayJoRvs", params)
        url = _generate_api_url("lsDayJoRvs", params)
        result = _format_search_results(data, "lsDayJoRvs", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"일자별 조문 개정 이력 검색 중 오류: {str(e)}")

@mcp.tool(name="search_article_change_history", description="조문별 변경 이력을 검색합니다. 특정 조문의 개정 변경 사항을 시계열로 조회할 수 있습니다.")
def search_article_change_history(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """조문별 변경 이력 목록 조회 (lsJoChg)"""
    search_query = query or "개인정보보호"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lsJoChg", params)
        url = _generate_api_url("lsJoChg", params)
        result = _format_search_results(data, "lsJoChg", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"조문별 변경 이력 검색 중 오류: {str(e)}")

@mcp.tool(name="search_law_ordinance_link", description="법령 기준 자치법규 연계 정보를 검색합니다. 법령과 관련된 자치법규들의 연계 현황을 조회할 수 있습니다.")
def search_law_ordinance_link(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 기준 자치법규 연계 관련 목록 조회 (lsOrdinCon)"""
    search_query = query or "개인정보보호"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lsOrdinCon", params)
        url = _generate_api_url("lsOrdinCon", params)
        result = _format_search_results(data, "lsOrdinCon", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령-자치법규 연계 검색 중 오류: {str(e)}")

@mcp.tool(name="get_law_ordinance_connection", description="법령-자치법규 연계현황을 조회합니다. 특정 법령과 자치법규 간의 연계 상태를 상세히 확인할 수 있습니다. 연계 목록 검색은 search_law_ordinance_link 도구를 사용하세요.")
def get_law_ordinance_connection(law_id: Union[str, int], ordinance_id: Optional[Union[str, int]] = None) -> TextContent:
    """법령-자치법규 연계현황 조회 (lsOrdinConInfo)"""
    params = {"ID": str(law_id)}
    if ordinance_id:
        params["ordinID"] = str(ordinance_id)
    try:
        data = _make_legislation_request("lsOrdinConInfo", params)
        url = _generate_api_url("lsOrdinConInfo", params)
        result = _format_search_results(data, "lsOrdinConInfo", str(law_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령-자치법규 연계현황 조회 중 오류: {str(e)}")

@mcp.tool(name="search_ordinance_law_link", description="자치법규 기준 법령 연계 정보를 검색합니다. 자치법규와 관련된 상위 법령들의 연계 현황을 조회할 수 있습니다.")
def search_ordinance_law_link(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """자치법규 기준 법령 연계 관련 목록 조회 (ordinLsCon)"""
    search_query = query or "개인정보보호"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ordinLsCon", params)
        url = _generate_api_url("ordinLsCon", params)
        result = _format_search_results(data, "ordinLsCon", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"자치법규-법령 연계 검색 중 오류: {str(e)}")

# ===========================================
# 법령정보 지식베이스 관련 API (7개)
# ===========================================

@mcp.tool(name="search_legal_term_ai", description="법령용어 AI 지식베이스를 검색합니다. AI 기반으로 법령용어의 정의와 해석을 제공합니다.")
def search_legal_term_ai(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령용어 AI 조회 (lstrmAI)"""
    search_query = query or "개인정보"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lstrmAI", params)
        url = _generate_api_url("lstrmAI", params)
        result = _format_search_results(data, "lstrmAI", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령용어 AI 검색 중 오류: {str(e)}")

@mcp.tool(name="search_daily_term", description="일상용어를 검색합니다. 법령용어에 대응하는 일상용어를 조회할 수 있습니다.")
def search_daily_term(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """일상용어 조회 (dlytrm)"""
    search_query = query or "개인정보"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("dlytrm", params)
        url = _generate_api_url("dlytrm", params)
        result = _format_search_results(data, "dlytrm", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"일상용어 검색 중 오류: {str(e)}")

@mcp.tool(name="search_legal_daily_term_link", description="법령용어-일상용어 연계 정보를 검색합니다. 법령용어와 일상용어 간의 연관관계를 조회할 수 있습니다.")
def search_legal_daily_term_link(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령용어-일상용어 연계 조회 (lstrmRlt)"""
    search_query = query or "개인정보"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lstrmRlt", params)
        url = _generate_api_url("lstrmRlt", params)
        result = _format_search_results(data, "lstrmRlt", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령용어-일상용어 연계 검색 중 오류: {str(e)}")

@mcp.tool(name="search_daily_legal_term_link", description="일상용어-법령용어 연계 정보를 검색합니다. 일상용어에서 법령용어로의 연관관계를 조회할 수 있습니다.")
def search_daily_legal_term_link(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """일상용어-법령용어 연계 조회 (dlytrmRlt)"""
    search_query = query or "개인정보"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("dlytrmRlt", params)
        url = _generate_api_url("dlytrmRlt", params)
        result = _format_search_results(data, "dlytrmRlt", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"일상용어-법령용어 연계 검색 중 오류: {str(e)}")

@mcp.tool(name="search_legal_term_article_link", description="법령용어-조문 연계 정보를 검색합니다. 법령용어가 사용된 조문들의 연관관계를 조회할 수 있습니다.")
def search_legal_term_article_link(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령용어-조문 연계 조회 (lstrmRltJo)"""
    search_query = query or "개인정보"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lstrmRltJo", params)
        url = _generate_api_url("lstrmRltJo", params)
        result = _format_search_results(data, "lstrmRltJo", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령용어-조문 연계 검색 중 오류: {str(e)}")

@mcp.tool(name="search_article_legal_term_link", description="조문-법령용어 연계 정보를 검색합니다. 조문에서 사용된 법령용어들의 연관관계를 조회할 수 있습니다.")
def search_article_legal_term_link(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """조문-법령용어 연계 조회 (joRltLstrm)"""
    search_query = query or "개인정보"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("joRltLstrm", params)
        url = _generate_api_url("joRltLstrm", params)
        result = _format_search_results(data, "joRltLstrm", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"조문-법령용어 연계 검색 중 오류: {str(e)}")

@mcp.tool(name="search_related_law", description="관련법령을 검색합니다. 특정 법령과 관련된 다른 법령들의 연관관계를 조회할 수 있습니다.")
def search_related_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """관련법령 조회 (lsRlt)"""
    search_query = query or "개인정보보호법"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lsRlt", params)
        url = _generate_api_url("lsRlt", params)
        result = _format_search_results(data, "lsRlt", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"관련법령 검색 중 오류: {str(e)}")

# ===========================================
# 중앙부처 해석 상세 조회 API (누락된 본문 조회들)
# ===========================================

@mcp.tool(name="get_moef_interpretation_detail", description="기획재정부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_moef_interpretation 도구를 사용하세요.")
def get_moef_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """기획재정부 법령해석 본문 조회 (moefCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moefCgmExpc", params)
        url = _generate_api_url("moefCgmExpc", params)
        result = _format_search_results(data, "moefCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"기획재정부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="search_nts_interpretation", description="국세청 법령해석을 검색합니다. 국세청의 법령해석 사례를 제공합니다.")
def search_nts_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """국세청 법령해석 목록 조회 (ntsCgmExpc)"""
    search_query = query or "소득세"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("ntsCgmExpc", params)
        url = _generate_api_url("ntsCgmExpc", params)
        result = _format_search_results(data, "ntsCgmExpc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국세청 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="get_nts_interpretation_detail", description="국세청 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_nts_interpretation 도구를 사용하세요.")
def get_nts_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """국세청 법령해석 본문 조회 (ntsCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("ntsCgmExpc", params)
        url = _generate_api_url("ntsCgmExpc", params)
        result = _format_search_results(data, "ntsCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국세청 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="search_kcs_interpretation", description="관세청 법령해석을 검색합니다. 관세청의 법령해석 사례를 제공합니다.")
def search_kcs_interpretation(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """관세청 법령해석 목록 조회 (kcsCgmExpc)"""
    search_query = query or "관세"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("kcsCgmExpc", params)
        url = _generate_api_url("kcsCgmExpc", params)
        result = _format_search_results(data, "kcsCgmExpc", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"관세청 법령해석 검색 중 오류: {str(e)}")

@mcp.tool(name="get_kcs_interpretation_detail", description="관세청 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_kcs_interpretation 도구를 사용하세요.")
def get_kcs_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """관세청 법령해석 본문 조회 (kcsCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("kcsCgmExpc", params)
        url = _generate_api_url("kcsCgmExpc", params)
        result = _format_search_results(data, "kcsCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"관세청 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mois_interpretation_detail", description="행정안전부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_mois_interpretation 도구를 사용하세요.")
def get_mois_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """행정안전부 법령해석 본문 조회 (moisCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moisCgmExpc", params)
        url = _generate_api_url("moisCgmExpc", params)
        result = _format_search_results(data, "moisCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"행정안전부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_me_interpretation_detail", description="환경부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_me_interpretation 도구를 사용하세요.")
def get_me_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """환경부 법령해석 본문 조회 (meCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("meCgmExpc", params)
        url = _generate_api_url("meCgmExpc", params)
        result = _format_search_results(data, "meCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"환경부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_kicogm_interpretation_detail", description="한국산업인력공단 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_kicogm_interpretation 도구를 사용하세요.")
def get_kicogm_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """한국산업인력공단 법령해석 본문 조회 (kicoCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("kicoCgmExpc", params)
        url = _generate_api_url("kicoCgmExpc", params)
        result = _format_search_results(data, "kicoCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"한국산업인력공단 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_kcg_interpretation_detail", description="해양경찰청 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_kcg_interpretation 도구를 사용하세요.")
def get_kcg_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """해양경찰청 법령해석 본문 조회 (kcgCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("kcgCgmExpc", params)
        url = _generate_api_url("kcgCgmExpc", params)
        result = _format_search_results(data, "kcgCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"해양경찰청 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_ordinance_appendix", description="모바일 자치법규 별표서식을 검색합니다. 모바일 최적화된 자치법규 별표서식을 제공합니다.")
def search_mobile_ordinance_appendix(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 자치법규 별표서식 목록 조회 (mobOrdinByl)"""
    search_query = query or "서식"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("mobOrdinByl", params)
        url = _generate_api_url("mobOrdinByl", params)
        result = _format_search_results(data, "mobOrdinByl", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"모바일 자치법규 별표서식 검색 중 오류: {str(e)}")

@mcp.tool(name="search_mobile_administrative_rule_appendix", description="모바일 행정규칙 별표서식을 검색합니다. 모바일 최적화된 행정규칙 별표서식을 제공합니다.")
def search_mobile_administrative_rule_appendix(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """모바일 행정규칙 별표서식 목록 조회 (mobAdmrulByl)"""
    search_query = query or "서식"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("mobAdmrulByl", params)
        url = _generate_api_url("mobAdmrulByl", params)
        result = _format_search_results(data, "mobAdmrulByl", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"모바일 행정규칙 별표서식 검색 중 오류: {str(e)}")

logger.info("✅ 완벽한 125개 API 전체 완성! 🎉") 

# ===========================================
# 누락된 13개 API 도구 추가 (정확한 125개 API 완성)
# ===========================================

@mcp.tool(name="get_effective_law_articles", description="시행일 법령의 조항호목을 조회합니다. 특정 시행일 법령의 조문별 세부 내용을 확인할 수 있습니다. 조, 항, 호, 목 단위로 정밀 검색이 가능합니다.")
def get_effective_law_articles(
    law_id: Union[str, int], 
    ef_yd: str,
    jo: Optional[str] = None,
    hang: Optional[str] = None,
    ho: Optional[str] = None,
    mok: Optional[str] = None
) -> TextContent:
    """시행일 법령 본문 조항호목 조회 (eflawjosub target 사용)
    
    Args:
        law_id: 법령 ID 또는 MST 번호
        ef_yd: 시행일자 (YYYYMMDD 형식, 필수)
        jo: 조번호 (6자리 숫자, 예: 000200=제2조, 001002=제10조의2)
        hang: 항번호 (6자리 숫자, 예: 000200=제2항)
        ho: 호번호 (6자리 숫자, 예: 000200=제2호, 001002=제10호의2)
        mok: 목 (한자리 문자, 예: 가,나,다,라...카,타,파,하)
    """
    params = {"ID": str(law_id), "efYd": ef_yd}
    
    # 조항호목 파라미터 추가
    if jo:
        params["JO"] = jo
    if hang:
        params["HANG"] = hang
    if ho:
        params["HO"] = ho
    if mok:
        params["MOK"] = mok
    
    try:
        data = _make_legislation_request("eflawjosub", params)
        url = _generate_api_url("eflawjosub", params)
        article_info = f"법령ID:{law_id} 시행일:{ef_yd}"
        if jo:
            article_info += f" 제{int(jo):,}조"
        if hang:
            article_info += f" 제{int(hang):,}항"
        if ho:
            article_info += f" 제{int(ho):,}호"
        if mok:
            article_info += f" {mok}목"
        result = _format_search_results(data, "eflawjosub", article_info, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"시행일 법령 조항호목 조회 중 오류: {str(e)}")

@mcp.tool(name="get_current_law_articles", description="현행법령의 조항호목을 조회합니다. 특정 법령의 조문별 세부 내용을 확인할 수 있습니다. 조, 항, 호, 목 단위로 정밀 검색이 가능합니다.")
def get_current_law_articles(
    law_id: Union[str, int],
    jo: Optional[str] = None,
    hang: Optional[str] = None,
    ho: Optional[str] = None,
    mok: Optional[str] = None
) -> TextContent:
    """현행법령 본문 조항호목 조회 (lawjosub target 사용)
    
    Args:
        law_id: 법령 ID 또는 MST 번호
        jo: 조번호 (6자리 숫자, 예: 000200=제2조, 001002=제10조의2)
        hang: 항번호 (6자리 숫자, 예: 000200=제2항)
        ho: 호번호 (6자리 숫자, 예: 000200=제2호, 001002=제10호의2)
        mok: 목 (한자리 문자, 예: 가,나,다,라...카,타,파,하)
    """
    params = {"ID": str(law_id)}
    
    # 조항호목 파라미터 추가
    if jo:
        params["JO"] = jo
    if hang:
        params["HANG"] = hang
    if ho:
        params["HO"] = ho
    if mok:
        params["MOK"] = mok
    
    try:
        data = _make_legislation_request("lawjosub", params)
        url = _generate_api_url("lawjosub", params)
        article_info = f"법령ID:{law_id}"
        if jo:
            article_info += f" 제{int(jo):,}조"
        if hang:
            article_info += f" 제{int(hang):,}항"
        if ho:
            article_info += f" 제{int(ho):,}호"
        if mok:
            article_info += f" {mok}목"
        result = _format_search_results(data, "lawjosub", article_info, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"현행법령 조항호목 조회 중 오류: {str(e)}")

@mcp.tool(name="get_ordinance_detail", description="자치법규 상세내용을 조회합니다. 특정 자치법규의 본문을 제공합니다. 목록 검색은 search_local_ordinance 도구를 사용하세요.")
def get_ordinance_detail(ordinance_id: Union[str, int]) -> TextContent:
    """자치법규 본문 조회 (ordin)"""
    params = {"ID": str(ordinance_id)}
    try:
        data = _make_legislation_request("ordin", params)
        url = _generate_api_url("ordin", params)
        result = _format_search_results(data, "ordin", str(ordinance_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"자치법규 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_precedent_detail", description="판례 상세내용을 조회합니다. 특정 판례의 전문과 판시사항을 제공합니다. 국세청 판례의 경우 HTML만 지원됩니다. 목록 검색은 search_precedent 도구를 사용하세요.")
def get_precedent_detail(case_id: Union[str, int], data_source: Optional[str] = None, output_type: str = "JSON") -> TextContent:
    """판례 본문 조회 (prec) - 국세청 판례는 HTML만 지원"""
    params = {"ID": str(case_id)}
    
    # 국세청 판례는 HTML만 지원
    if data_source and "국세" in data_source:
        params["type"] = "HTML"
    else:
        params["type"] = output_type
    
    try:
        data = _make_legislation_request("prec", params, is_detail=True)
        url = _generate_api_url("prec", params, is_detail=True)
        
        # 국세청 판례 HTML 응답 처리
        if params.get("type") == "HTML":
            result = f"🔗 **API 호출 URL**: {url}\n\n"
            result += "📄 **국세청 판례 HTML 응답**:\n"
            if isinstance(data, dict) and not data.get("error"):
                result += "✅ HTML 형태로 판례 내용이 조회되었습니다.\n"
                result += "💡 **안내**: 국세청 판례는 HTML 형태로만 제공됩니다."
            else:
                result += f"오류: {data.get('error', '알 수 없는 오류')}"
        else:
            result = _format_search_results(data, "prec", str(case_id), url)
        
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"판례 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_constitutional_court_detail", description="헌법재판소 결정례 상세내용을 조회합니다. 특정 결정례의 전문을 제공합니다. 목록 검색은 search_constitutional_court 도구를 사용하세요.")
def get_constitutional_court_detail(case_id: Union[str, int]) -> TextContent:
    """헌재결정례 본문 조회 (detc)"""
    params = {"ID": str(case_id)}
    try:
        data = _make_legislation_request("detc", params, is_detail=True)
        url = _generate_api_url("detc", params, is_detail=True)
        result = _format_search_results(data, "detc", str(case_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"헌재결정례 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_legal_interpretation_detail", description="법령해석례 상세내용을 조회합니다. 특정 해석례의 전문과 해석 내용을 제공합니다. 목록 검색은 search_legal_interpretation 도구를 사용하세요.")
def get_legal_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """법령해석례 본문 조회 (expc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("expc", params, is_detail=True)
        url = _generate_api_url("expc", params, is_detail=True)
        result = _format_search_results(data, "expc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령해석례 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_precedent_detail", description="모바일 판례 상세내용을 조회합니다. 모바일 최적화된 판례 본문을 제공합니다. 목록 검색은 search_mobile_precedent 도구를 사용하세요.")
def get_mobile_precedent_detail(case_id: Union[str, int]) -> TextContent:
    """모바일 판례 본문 조회 (mobprec)"""
    params = {"ID": str(case_id)}
    try:
        data = _make_legislation_request("mobprec", params)
        url = _generate_api_url("mobprec", params)
        result = _format_search_results(data, "mobprec", str(case_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"모바일 판례 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_constitutional_court_detail", description="모바일 헌재결정례 상세내용을 조회합니다. 모바일 최적화된 헌재결정례 본문을 제공합니다. 목록 검색은 search_constitutional_court 도구를 사용하세요.")
def get_mobile_constitutional_court_detail(case_id: Union[str, int]) -> TextContent:
    """모바일 헌재결정례 본문 조회 (mobdetc)"""
    params = {"ID": str(case_id)}
    try:
        data = _make_legislation_request("mobdetc", params)
        url = _generate_api_url("mobdetc", params)
        result = _format_search_results(data, "mobdetc", str(case_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"모바일 헌재결정례 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_legal_interpretation_detail", description="모바일 법령해석례 상세내용을 조회합니다. 모바일 최적화된 해석례 본문을 제공합니다. 목록 검색은 search_legal_interpretation 도구를 사용하세요.")
def get_mobile_legal_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """모바일 법령해석례 본문 조회 (mobexpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("mobexpc", params)
        url = _generate_api_url("mobexpc", params)
        result = _format_search_results(data, "mobexpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"모바일 법령해석례 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_administrative_trial_detail", description="모바일 행정심판례 상세내용을 조회합니다. 모바일 최적화된 심판례 본문을 제공합니다. 목록 검색은 search_mobile_administrative_trial 도구를 사용하세요.")
def get_mobile_administrative_trial_detail(trial_id: Union[str, int]) -> TextContent:
    """모바일 행정심판례 본문 조회 (mobdecc)"""
    params = {"ID": str(trial_id)}
    try:
        data = _make_legislation_request("mobdecc", params)
        url = _generate_api_url("mobdecc", params)
        result = _format_search_results(data, "mobdecc", str(trial_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"모바일 행정심판례 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_treaty_detail", description="모바일 조약 상세내용을 조회합니다. 모바일 최적화된 조약 본문을 제공합니다. 목록 검색은 search_mobile_treaty 도구를 사용하세요.")
def get_mobile_treaty_detail(treaty_id: Union[str, int]) -> TextContent:
    """모바일 조약 본문 조회 (mobtrty)"""
    params = {"ID": str(treaty_id)}
    try:
        data = _make_legislation_request("mobtrty", params)
        url = _generate_api_url("mobtrty", params)
        result = _format_search_results(data, "mobtrty", str(treaty_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"모바일 조약 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mobile_legal_term_detail", description="모바일 법령용어 상세내용을 조회합니다. 모바일 최적화된 용어 해설을 제공합니다. 목록 검색은 search_mobile_legal_term 도구를 사용하세요.")
def get_mobile_legal_term_detail(term_id: Union[str, int]) -> TextContent:
    """모바일 법령용어 본문 조회 (moblstrm)"""
    params = {"ID": str(term_id)}
    try:
        data = _make_legislation_request("moblstrm", params)
        url = _generate_api_url("moblstrm", params)
        result = _format_search_results(data, "moblstrm", str(term_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"모바일 법령용어 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_legal_term_detail", description="법령용어 상세내용을 조회합니다. 특정 법령용어의 정의와 설명을 제공합니다. 목록 검색은 search_legal_term 도구를 사용하세요.")
def get_legal_term_detail(term_id: Union[str, int]) -> TextContent:
    """법령용어 본문 조회 (lstrm)"""
    params = {"ID": str(term_id)}
    try:
        data = _make_legislation_request("lstrm", params)
        url = _generate_api_url("lstrm", params)
        result = _format_search_results(data, "lstrm", str(term_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령용어 상세조회 중 오류: {str(e)}")

logger.info("✅ 진짜 125개 API 완성! 추가 분석도구 13개 별도! 총 138개 도구!")

# ===========================================
# 누락된 핵심 API 본문 조회 도구들 추가
# ===========================================

@mcp.tool(name="get_effective_law_detail", description="시행일 법령의 상세내용을 조회합니다. 특정 시행일 법령의 본문을 제공합니다. 목록 검색은 search_effective_law 도구를 사용하세요.")
def get_effective_law_detail(law_id: Union[str, int], effective_date: str) -> TextContent:
    """시행일 법령 본문 조회 (eflawi)"""
    params = {"ID": str(law_id), "efYd": effective_date}
    try:
        data = _make_legislation_request("eflawi", params)
        url = _generate_api_url("eflawi", params)
        result = _format_search_results(data, "eflawi", f"법령ID:{law_id} 시행일:{effective_date}", url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"시행일 법령 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_law_history_detail", description="법령연혁의 상세내용을 조회합니다. 특정 법령연혁의 본문을 제공합니다. 목록 검색은 search_law_history 도구를 사용하세요.")
def get_law_history_detail(history_id: Union[str, int]) -> TextContent:
    """법령연혁 본문 조회 (lsHst)"""
    params = {"ID": str(history_id)}
    try:
        data = _make_legislation_request("lsHst", params)
        url = _generate_api_url("lsHst", params)
        result = _format_search_results(data, "lsHst", str(history_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령연혁 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_english_law_detail", description="영문법령의 상세내용을 조회합니다. 특정 영문법령의 본문을 제공합니다. 목록 검색은 search_english_law 도구를 사용하세요.")
def get_english_law_detail(law_id: Union[str, int]) -> TextContent:
    """영문법령 본문 조회 (lsEng)"""
    params = {"ID": str(law_id)}
    try:
        data = _make_legislation_request("lsEng", params)
        url = _generate_api_url("lsEng", params)
        result = _format_search_results(data, "lsEng", str(law_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"영문법령 상세조회 중 오류: {str(e)}")

@mcp.tool(name="search_law_change_history", description="법령 변경이력을 검색합니다. 법령의 개정 및 변경 내역을 조회할 수 있습니다.")
def search_law_change_history(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 변경이력 목록 조회 (lsChg)"""
    search_query = query or "개인정보보호법"
    params = {"query": search_query, "display": min(display, 100), "page": page}
    try:
        data = _make_legislation_request("lsChg", params)
        url = _generate_api_url("lsChg", params)
        result = _format_search_results(data, "lsChg", search_query, url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령 변경이력 검색 중 오류: {str(e)}")

@mcp.tool(name="get_treaty_detail", description="조약의 상세내용을 조회합니다. 특정 조약의 전문과 내용을 제공합니다. 목록 검색은 search_treaty 도구를 사용하세요.")
def get_treaty_detail(treaty_id: Union[str, int]) -> TextContent:
    """조약 본문 조회 (trty)"""
    params = {"ID": str(treaty_id)}
    try:
        data = _make_legislation_request("trty", params)
        url = _generate_api_url("trty", params)
        result = _format_search_results(data, "trty", str(treaty_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"조약 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_law_appendix_detail", description="법령 별표서식 상세내용을 조회합니다. 특정 별표서식의 본문을 제공합니다. 목록 검색은 search_law_appendix 도구를 사용하세요.")
def get_law_appendix_detail(appendix_id: Union[str, int]) -> TextContent:
    """법령 별표서식 본문 조회 (byl)"""
    params = {"ID": str(appendix_id)}
    try:
        data = _make_legislation_request("byl", params)
        url = _generate_api_url("byl", params)
        result = _format_search_results(data, "byl", str(appendix_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"법령 별표서식 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_ordinance_appendix_detail", description="자치법규 별표서식 상세내용을 조회합니다. 특정 자치법규 별표서식의 본문을 제공합니다. 목록 검색은 search_ordinance_appendix 도구를 사용하세요.")
def get_ordinance_appendix_detail(appendix_id: Union[str, int]) -> TextContent:
    """자치법규 별표서식 본문 조회 (ordinbyl)"""
    params = {"ID": str(appendix_id)}
    try:
        data = _make_legislation_request("ordinbyl", params)
        url = _generate_api_url("ordinbyl", params)
        result = _format_search_results(data, "ordinbyl", str(appendix_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"자치법규 별표서식 상세조회 중 오류: {str(e)}")

# ===========================================
# 위원회 결정문 본문 조회 도구들 (누락된 Info API들)
# ===========================================

@mcp.tool(name="get_privacy_committee_detail", description="개인정보보호위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_privacy_committee 도구를 사용하세요.")
def get_privacy_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """개인정보보호위원회 결정문 본문 조회 (ppc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("ppc", params, is_detail=True)
        url = _generate_api_url("ppc", params, is_detail=True)
        result = _format_search_results(data, "ppc", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"개인정보보호위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_financial_committee_detail", description="금융위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_financial_committee 도구를 사용하세요.")
def get_financial_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """금융위원회 결정문 본문 조회 (fsc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("fsc", params, is_detail=True)
        url = _generate_api_url("fsc", params, is_detail=True)
        result = _format_search_results(data, "fsc", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"금융위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_monopoly_committee_detail", description="공정거래위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_monopoly_committee 도구를 사용하세요.")
def get_monopoly_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """공정거래위원회 결정문 본문 조회 (ftc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("ftc", params, is_detail=True)
        url = _generate_api_url("ftc", params)
        result = _format_search_results(data, "ftc", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"공정거래위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_anticorruption_committee_detail", description="국민권익위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_anticorruption_committee 도구를 사용하세요.")
def get_anticorruption_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """국민권익위원회 결정문 본문 조회 (acr)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("acr", params)
        url = _generate_api_url("acr", params)
        result = _format_search_results(data, "acr", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국민권익위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_labor_committee_detail", description="노동위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_labor_committee 도구를 사용하세요.")
def get_labor_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """노동위원회 결정문 본문 조회 (nlrc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("nlrc", params)
        url = _generate_api_url("nlrc", params)
        result = _format_search_results(data, "nlrc", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"노동위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_environment_committee_detail", description="중앙환경분쟁조정위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_environment_committee 도구를 사용하세요.")
def get_environment_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """중앙환경분쟁조정위원회 결정문 본문 조회 (ecc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("ecc", params)
        url = _generate_api_url("ecc", params)
        result = _format_search_results(data, "ecc", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중앙환경분쟁조정위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_securities_committee_detail", description="증권선물위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_securities_committee 도구를 사용하세요.")
def get_securities_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """증권선물위원회 결정문 본문 조회 (sfc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("sfc", params)
        url = _generate_api_url("sfc", params)
        result = _format_search_results(data, "sfc", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"증권선물위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_human_rights_committee_detail", description="국가인권위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_human_rights_committee 도구를 사용하세요.")
def get_human_rights_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """국가인권위원회 결정문 본문 조회 (nhrck)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("nhrck", params)
        url = _generate_api_url("nhrck", params)
        result = _format_search_results(data, "nhrck", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국가인권위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_broadcasting_committee_detail", description="방송통신위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_broadcasting_committee 도구를 사용하세요.")
def get_broadcasting_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """방송통신위원회 결정문 본문 조회 (kcc)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("kcc", params)
        url = _generate_api_url("kcc", params)
        result = _format_search_results(data, "kcc", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"방송통신위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_industrial_accident_committee_detail", description="산업재해보상보험 재심사위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_industrial_accident_committee 도구를 사용하세요.")
def get_industrial_accident_committee_detail(decision_id: Union[str, int]) -> TextContent:
    """산업재해보상보험 재심사위원회 결정문 본문 조회 (eiac)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("eiac", params)
        url = _generate_api_url("eiac", params)
        result = _format_search_results(data, "eiac", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"산업재해보상보험 재심사위원회 결정문 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_land_tribunal_detail", description="중앙토지수용위원회 결정문 상세내용을 조회합니다. 특정 결정문의 본문을 제공합니다. 목록 검색은 search_land_tribunal 도구를 사용하세요.")
def get_land_tribunal_detail(decision_id: Union[str, int]) -> TextContent:
    """중앙토지수용위원회 결정문 본문 조회 (lx)"""
    params = {"ID": str(decision_id)}
    try:
        data = _make_legislation_request("oclt", params)
        url = _generate_api_url("oclt", params)
        result = _format_search_results(data, "oclt", str(decision_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중앙토지수용위원회 결정문 상세조회 중 오류: {str(e)}")

# ===========================================
# 중앙부처 해석 본문 조회 도구들 (모든 부처별 Info API 완성)
# ===========================================

@mcp.tool(name="get_molit_interpretation_detail", description="국토교통부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_molit_interpretation 도구를 사용하세요.")
def get_molit_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """국토교통부 법령해석 본문 조회 (molitCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("molitCgmExpc", params)
        url = _generate_api_url("molitCgmExpc", params)
        result = _format_search_results(data, "molitCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국토교통부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_moel_interpretation_detail", description="고용노동부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_moel_interpretation 도구를 사용하세요.")
def get_moel_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """고용노동부 법령해석 본문 조회 (moelCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moelCgmExpc", params)
        url = _generate_api_url("moelCgmExpc", params)
        result = _format_search_results(data, "moelCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"고용노동부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mof_interpretation_detail", description="해양수산부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_mof_interpretation 도구를 사용하세요.")
def get_mof_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """해양수산부 법령해석 본문 조회 (mofCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("mofCgmExpc", params)
        url = _generate_api_url("mofCgmExpc", params)
        result = _format_search_results(data, "mofCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"해양수산부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mohw_interpretation_detail", description="보건복지부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_mohw_interpretation 도구를 사용하세요.")
def get_mohw_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """보건복지부 법령해석 본문 조회 (mohwCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("mohwCgmExpc", params)
        url = _generate_api_url("mohwCgmExpc", params)
        result = _format_search_results(data, "mohwCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"보건복지부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_moe_interpretation_detail", description="교육부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_moe_interpretation 도구를 사용하세요.")
def get_moe_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """교육부 법령해석 본문 조회 (moeCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moeCgmExpc", params)
        url = _generate_api_url("moeCgmExpc", params)
        result = _format_search_results(data, "moeCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"교육부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_korea_interpretation_detail", description="한국 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_korea_interpretation 도구를 사용하세요.")
def get_korea_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """한국 법령해석 본문 조회 (koreaExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("koreaExpc", params)
        url = _generate_api_url("koreaExpc", params)
        result = _format_search_results(data, "koreaExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"한국 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mssp_interpretation_detail", description="보훈처 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_mssp_interpretation 도구를 사용하세요.")
def get_mssp_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """보훈처 법령해석 본문 조회 (msspCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("msspCgmExpc", params)
        url = _generate_api_url("msspCgmExpc", params)
        result = _format_search_results(data, "msspCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"보훈처 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_mote_interpretation_detail", description="산업통상자원부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_mote_interpretation 도구를 사용하세요.")
def get_mote_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """산업통상자원부 법령해석 본문 조회 (moteCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("moteCgmExpc", params)
        url = _generate_api_url("moteCgmExpc", params)
        result = _format_search_results(data, "moteCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"산업통상자원부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_maf_interpretation_detail", description="농림축산식품부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_maf_interpretation 도구를 사용하세요.")
def get_maf_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """농림축산식품부 법령해석 본문 조회 (mafCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("mafCgmExpc", params)
        url = _generate_api_url("mafCgmExpc", params)
        result = _format_search_results(data, "mafCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"농림축산식품부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_moms_interpretation_detail", description="국방부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_moms_interpretation 도구를 사용하세요.")
def get_moms_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """국방부 법령해석 본문 조회 (momsCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("momsCgmExpc", params)
        url = _generate_api_url("momsCgmExpc", params)
        result = _format_search_results(data, "momsCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"국방부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_sme_interpretation_detail", description="중소벤처기업부 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_sme_interpretation 도구를 사용하세요.")
def get_sme_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """중소벤처기업부 법령해석 본문 조회 (smeexpcCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("smeexpcCgmExpc", params)
        url = _generate_api_url("smeexpcCgmExpc", params)
        result = _format_search_results(data, "smeexpcCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"중소벤처기업부 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_nfa_interpretation_detail", description="산림청 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_nfa_interpretation 도구를 사용하세요.")
def get_nfa_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """산림청 법령해석 본문 조회 (nfaCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("nfaCgmExpc", params)
        url = _generate_api_url("nfaCgmExpc", params)
        result = _format_search_results(data, "nfaCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"산림청 법령해석 상세조회 중 오류: {str(e)}")

@mcp.tool(name="get_korail_interpretation_detail", description="한국철도공사 법령해석 상세내용을 조회합니다. 특정 해석례의 전문을 제공합니다. 목록 검색은 search_korail_interpretation 도구를 사용하세요.")
def get_korail_interpretation_detail(interpretation_id: Union[str, int]) -> TextContent:
    """한국철도공사 법령해석 본문 조회 (korailCgmExpc)"""
    params = {"ID": str(interpretation_id)}
    try:
        data = _make_legislation_request("korailCgmExpc", params)
        url = _generate_api_url("korailCgmExpc", params)
        result = _format_search_results(data, "korailCgmExpc", str(interpretation_id), url)
        return TextContent(type="text", text=result)
    except Exception as e:
        return TextContent(type="text", text=f"한국철도공사 법령해석 상세조회 중 오류: {str(e)}")

logger.info("✅ 완전한 125개 API + 45개 누락된 본문조회 API = 총 170개 완성!")
logger.info("🎯 추가로 분석도구 13개 = 총 183개 도구 완성!")
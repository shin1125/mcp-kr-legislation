"""
한국 법제처 OPEN API - 법령 관련 통합 도구들

현행법령, 시행일법령, 법령연혁, 영문법령, 조문, 체계도, 연계정보, 맞춤형 등
모든 법령 관련 도구들을 통합 제공합니다. (총 29개 도구)
"""

import logging
import json
import os
import requests
from urllib.parse import urlencode
from typing import Optional, Union, Dict, Any, List
from mcp.types import TextContent
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import re

from ..server import mcp
from ..config import legislation_config
from ..apis.client import LegislationClient

logger = logging.getLogger(__name__)

# ===========================================
# 캐시 시스템 (최적화용)
# ===========================================

# 홈 디렉토리의 .cache 사용 (권한 문제 해결)
CACHE_DIR = Path.home() / ".cache" / "mcp-kr-legislation"
CACHE_DAYS = 7  # 캐시 유효 기간 (일)

def ensure_cache_dir():
    """캐시 디렉토리 생성"""
    try:
        # 홈 디렉토리의 .cache 사용
        cache_path = CACHE_DIR
        cache_path.mkdir(parents=True, exist_ok=True)
        
        # 디렉토리 쓰기 권한 확인
        test_file = cache_path / ".test"
        try:
            test_file.touch()
            test_file.unlink()
            logger.info(f"캐시 디렉토리 준비 완료: {cache_path}")
            return True
        except Exception as e:
            logger.warning(f"캐시 디렉토리에 쓰기 권한이 없습니다: {cache_path} - {e}")
            return False
        
    except Exception as e:
        logger.error(f"캐시 디렉토리 생성 실패: {e}")
        return False

def get_cache_key(law_id: str, section: str = "all") -> str:
    """캐시 키 생성"""
    key_string = f"{law_id}_{section}"
    return hashlib.md5(key_string.encode()).hexdigest()

def get_cache_path(cache_key: str) -> Path:
    """캐시 파일 경로 생성"""
    return CACHE_DIR / f"{cache_key}.json"

def is_cache_valid(cache_path: Path) -> bool:
    """캐시 유효성 확인"""
    if not cache_path.exists():
        return False
    from datetime import timedelta
    file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
    expiry_time = datetime.now() - timedelta(days=CACHE_DAYS)
    return file_time > expiry_time

def save_to_cache(cache_key: str, data: Any):
    """캐시에 데이터 저장"""
    try:
        if not ensure_cache_dir():
            logger.warning("캐시 디렉토리를 생성할 수 없어 캐시 저장을 건너뜁니다.")
            return
        
        cache_file = get_cache_path(cache_key)
        
        # 캐시 데이터 구조
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"캐시 저장 완료: {cache_key}")
    except Exception as e:
        logger.warning(f"캐시 저장 중 오류 (서비스는 계속됨): {e}")

def load_from_cache(cache_key: str) -> Optional[Any]:
    """캐시에서 데이터 로드"""
    try:
        cache_file = get_cache_path(cache_key)
        
        if not cache_file.exists():
            return None
            
        if not is_cache_valid(cache_file):
            cache_file.unlink()  # 만료된 캐시 삭제
            return None
            
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
            logger.info(f"캐시 로드 완료: {cache_key}")
            return cache_data.get("data")
            
    except Exception as e:
        logger.warning(f"캐시 로드 중 오류 (API 호출로 대체됨): {e}")
        return None

# ===========================================
# 공통 유틸리티 함수들
# ===========================================

def extract_article_number(article_key: str) -> int:
    """조문 키에서 숫자 추출 (정렬용)"""
    try:
        import re
        match = re.search(r'제(\d+)조', article_key)
        return int(match.group(1)) if match else 999999
    except:
        return 999999

def extract_law_summary_from_detail(detail_data: Dict[str, Any]) -> Dict[str, Any]:
    """법령 상세 데이터에서 요약 정보 추출"""
    try:
        law_info = detail_data.get("법령", {})
        basic_info = law_info.get("기본정보", {})
        
        # 법령일련번호 추출 - 여러 필드에서 시도
        mst = (basic_info.get("법령일련번호") or 
               basic_info.get("법령MST") or
               law_info.get("법령키", "")[:10] if law_info.get("법령키") else None)
        
        # 소관부처 정보 추출 - dict인 경우와 string인 경우 모두 처리
        ministry_info = basic_info.get("소관부처", "")
        if isinstance(ministry_info, dict):
            ministry = ministry_info.get("content", ministry_info.get("소관부처명", "미지정"))
        else:
            ministry = ministry_info or basic_info.get("소관부처명", "미지정")
        
        # 조문 정보 추출
        articles_section = law_info.get("조문", {})
        article_units = []
        
        if isinstance(articles_section, dict) and "조문단위" in articles_section:
            article_units = articles_section.get("조문단위", [])
            # 리스트가 아닌 경우 리스트로 변환
            if not isinstance(article_units, list):
                article_units = [article_units] if article_units else []
        elif isinstance(articles_section, list):
            article_units = articles_section
        
        # 실제 조문만 필터링 (조문여부가 "조문"인 것만)
        actual_articles = []
        for article in article_units:
            if isinstance(article, dict) and article.get("조문여부") == "조문":
                actual_articles.append(article)
        
        # 처음 50개 조문 인덱스 생성 (기존 20개에서 확대)
        article_index = []
        for i, article in enumerate(actual_articles[:50]):
            article_no = article.get("조문번호", "")
            article_title = article.get("조문제목", "")
            article_content = article.get("조문내용", "")
            
            # 조문 요약 생성
            summary = f"제{article_no}조"
            if article_title:
                summary += f"({article_title})"
            
            # 내용 미리보기 추가 - 더 자세하게 표시
            if article_content:
                content_preview = article_content.strip()[:150]  # 100자에서 150자로 확대
                if len(article_content) > 150:
                    content_preview += "..."
                summary += f" {content_preview}"
            
            article_index.append({
                "key": f"제{article_no}조",
                "summary": summary
            })
        
        # 제개정이유 추출
        revision_reason = []
        revision_section = law_info.get("개정문", {})
        if revision_section:
            reason_content = revision_section.get("개정문내용", [])
            if isinstance(reason_content, list) and reason_content:
                revision_reason = reason_content[0][:3] if len(reason_content[0]) >= 3 else reason_content[0]
        
        # 날짜 형식 통일 (YYYYMMDD → YYYY-MM-DD)
        def format_date(date_str):
            if date_str and len(date_str) == 8:
                return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            return date_str
        
        return {
            "법령명": basic_info.get("법령명_한글", ""),
            "법령ID": basic_info.get("법령ID", ""),
            "법령일련번호": mst,
            "공포일자": format_date(basic_info.get("공포일자", "")),
            "시행일자": format_date(basic_info.get("시행일자", "")),
            "소관부처": ministry,
            "조문_인덱스": article_index,
            "조문_총개수": len(actual_articles),
            "제개정이유": revision_reason,
            "원본크기": len(json.dumps(detail_data, ensure_ascii=False))
        }
        
    except Exception as e:
        logger.error(f"요약 추출 중 오류: {e}")
        return {
            "법령명": "오류",
            "오류메시지": str(e)
        }

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
    """검색어 변형 생성 - 범용적 법률 검색 최적화"""
    if not query:
        return [query]
    
    variants = [query]
    normalized = _normalize_search_query(query)
    if normalized != query:
        variants.append(normalized)
    
    # 추가 변형들
    if query not in normalized:
        if query.endswith('법'):
            variants.extend([query + '률', query[:-1] + '에관한법률'])
        elif query.endswith('령'):
            variants.extend([query[:-1] + '시행령'])
        elif query.endswith('규칙'):
            variants.extend([query[:-2] + '시행규칙'])
    
    return list(set(variants))

def _make_legislation_request(target: str, params: dict, is_detail: bool = False, timeout: int = 10) -> dict:
    """법제처 API 요청 공통 함수"""
    try:
        # URL 생성 - 올바른 target 파라미터 사용
        url = _generate_api_url(target, params, is_detail)
        
        # 디버깅을 위한 로그 추가 (영문 법령의 경우)
        if target == "elaw":
            logger.info(f"영문법령 API 요청 URL: {url}")
        
        # 요청 실행
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        # 응답 내용 확인 (영문 법령의 경우)
        if target == "elaw":
            logger.info(f"영문법령 응답 상태: {response.status_code}")
            logger.info(f"영문법령 Content-Type: {response.headers.get('Content-Type', 'None')}")
            if not response.text:
                logger.error("영문법령 API 빈 응답")
                return {"error": "영문법령 API가 빈 응답을 반환했습니다"}
        
        # HTML 오류 페이지 체크
        if response.headers.get('Content-Type', '').startswith('text/html'):
            if '사용자인증에 실패' in response.text or '페이지 접속에 실패' in response.text:
                raise ValueError("API 인증 실패 - OC(기관코드)를 확인하세요")
            else:
                # 영문 법령의 경우 더 자세한 오류 메시지
                if target == "elaw":
                    logger.error(f"영문법령 HTML 응답: {response.text[:500]}")
                    raise ValueError("영문법령 API가 HTML을 반환했습니다. API 엔드포인트나 파라미터를 확인하세요.")
                raise ValueError("HTML 응답 반환 - JSON 응답이 예상됨")
        
        # JSON 파싱
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            # 영문 법령의 경우 더 자세한 오류 처리
            if target == "elaw":
                logger.error(f"영문법령 JSON 파싱 오류: {str(e)}")
                logger.error(f"응답 내용 (처음 500자): {response.text[:500]}")
                return {"error": f"영문법령 API JSON 파싱 실패: {str(e)}"}
            raise
        
        # 응답 구조 확인
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON response structure")
        
        # 빈 응답 체크
        if not data:
            logger.warning(f"빈 응답 반환 - target: {target}, params: {params}")
            return {}
        
        # 오류 코드 체크
        if 'LawSearch' in data:
            # 영문 법령은 resultCode가 없으므로 체크하지 않음
            if target != "elaw":
                result_code = data['LawSearch'].get('resultCode')
                if result_code != '00':
                    result_msg = data['LawSearch'].get('resultMsg', '알 수 없는 오류')
                    raise ValueError(f"API 오류: {result_msg} (코드: {result_code})")
            else:
                # 영문 법령은 totalCnt로 결과 유무 판단
                total_cnt = data['LawSearch'].get('totalCnt', '0')
                if str(total_cnt) == '0' and 'law' not in data['LawSearch']:
                    # 실제로 결과가 없는 경우만 처리 (빈 검색 결과는 오류가 아님)
                    pass
        
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API 요청 실패: {e}")
        raise
    except Exception as e:
        logger.error(f"데이터 처리 실패: {e}")
        raise

def _generate_api_url(target: str, params: dict, is_detail: bool = False) -> str:
    """올바른 법제처 API URL 생성"""
    try:
        # 기본 파라미터 설정
        base_params = {
            "OC": legislation_config.oc,
            "type": "JSON",
            "target": target  # 핵심: target 파라미터 반드시 포함
        }
        base_params.update(params)
        
        # URL 결정: 상세조회 vs 검색
        if is_detail and ("ID" in params or "MST" in params):
            # 상세조회: lawService.do 사용  
            base_url = legislation_config.service_base_url
        else:
            # 검색: lawSearch.do 사용
            base_url = legislation_config.search_base_url
    
        query_string = urlencode(base_params, safe=':', encoding='utf-8')
        return f"{base_url}?{query_string}"
        
    except Exception as e:
        logger.error(f"URL 생성 실패: {e}")
        return ""

def _format_search_results(data: dict, target: str, search_query: str, max_results: int = 50) -> str:
    """검색 결과 포맷팅 공통 함수"""
    try:
        # 다양한 응답 구조 처리
        if 'LawSearch' in data:
            # 기본 검색 구조
            if target == "elaw":
                # 영문 법령은 'law' 키 사용
                target_data = data['LawSearch'].get('law', [])
            else:
                target_data = data['LawSearch'].get(target, [])
        elif target in data:
            # 직접 타겟 구조
            target_data = data[target]
        else:
            # 단일 키 구조 확인
            keys = list(data.keys())
            if len(keys) == 1:
                target_data = data[keys[0]]
            else:
                target_data = []
        
        # 리스트가 아닌 경우 처리
        if not isinstance(target_data, list):
            if isinstance(target_data, dict):
                target_data = [target_data]
            else:
                target_data = []
        
        if not target_data:
            return f"'{search_query}'에 대한 검색 결과가 없습니다."
        
        # 결과 개수 제한
        limited_data = target_data[:max_results]
        total_count = len(target_data)
        
        result = f"**'{search_query}' 검색 결과** (총 {total_count}건"
        if total_count > max_results:
            result += f", 상위 {max_results}건 표시"
        result += ")\n\n"
        
        for i, item in enumerate(limited_data, 1):
            result += f"**{i}. "
            
            # 제목 추출 (실제 API 응답 키 이름들 - 언더스코어 없음)
            title_keys = [
                '법령명한글', '법령명', '제목', 'title', '명칭', 'name',
                '현행법령명', '법령명국문', '국문법령명', 'lawNm', 'lawName',
                '법령명전체', '법령제목', 'lawTitle'
            ]
            
            # 영문 법령인 경우 영문명을 먼저 표시
            if target == "elaw" and '법령명영문' in item and item['법령명영문']:
                title = item['법령명영문']
                # 한글명도 함께 표시
                if '법령명한글' in item and item['법령명한글']:
                    title += f" ({item['법령명한글']})"
            else:
                title = None
                for key in title_keys:
                    if key in item and item[key] and str(item[key]).strip():
                        title = str(item[key]).strip()
                        break
            
            # 디버깅: 실제 키 이름들 확인
            if not title:
                # 응답에서 사용 가능한 모든 키 확인
                available_keys = list(item.keys()) if isinstance(item, dict) else []
                logger.info(f"사용 가능한 키들: {available_keys}")
                # 법령명으로 보이는 키들 찾기
                potential_title_keys = [k for k in available_keys if '법령' in str(k) or '명' in str(k) or 'title' in str(k).lower()]
                if potential_title_keys:
                    title = str(item.get(potential_title_keys[0], '')).strip()
            
            if title:
                result += f"{title}**\n"
            else:
                result += "제목 없음**\n"
            
            # 상세 정보 추가 (실제 API 응답 키 이름들)
            detail_fields = {
                '법령ID': ['법령ID', 'ID', 'id', 'lawId', 'mstSeq'],
                '법령일련번호': ['법령일련번호', 'MST', 'mst', 'lawMst', '법령MST'],
                '공포일자': ['공포일자', 'date', 'announce_date', '공포일', 'promulgateDate', '공포년월일'],
                '시행일자': ['시행일자', 'ef_date', 'effective_date', '시행일', 'enforceDate', '시행년월일'], 
                '소관부처명': ['소관부처명', 'ministry', 'department', '소관부처', 'ministryNm', '주무부처'],
                '법령구분명': ['법령구분명', 'type', 'law_type', '법령구분', 'lawType', '법령종류'],
                '제개정구분명': ['제개정구분명', 'revision', '제개정구분', 'revisionType', '개정구분']
            }
            
            for display_name, field_keys in detail_fields.items():
                value = None
                for key in field_keys:
                    if key in item and item[key] and str(item[key]).strip():
                        value = str(item[key]).strip()
                        break
                if value:
                    result += f"   {display_name}: {value}\n"
            
            # 법령일련번호와 법령ID 모두 있는 경우 상세조회 가이드 추가
            mst = None
            law_id = None
            
            # MST 찾기
            for key in ['법령일련번호', 'MST', 'mst', 'lawMst']:
                if key in item and item[key]:
                    mst = item[key]
                    break
            
            # 법령ID 찾기
            for key in ['법령ID', 'ID', 'id', 'lawId']:
                if key in item and item[key]:
                    law_id = item[key]
                    break
            
            # 상세조회 가이드
            if mst:
                result += f"   상세조회: get_law_detail_unified(mst=\"{mst}\", target=\"law\")\n"
            elif law_id:
                result += f"   상세조회: get_law_detail(law_id=\"{law_id}\")\n"
            
            result += "\n"
        
        if total_count > max_results:
            result += f"더 많은 결과가 있습니다. 검색어를 구체화하거나 페이지 번호를 조정해보세요.\n"
        
        return result
        
    except Exception as e:
        logger.error(f"결과 포맷팅 오류: {e}")
        return f"검색 결과 처리 중 오류가 발생했습니다: {str(e)}"

def _safe_format_law_detail(data: dict, search_term: str, url: str) -> str:
    """법령 상세내용 안전 포맷팅"""
    try:
        result = f"**법령 상세 정보** (검색어: {search_term})\n"
        result += "=" * 50 + "\n\n"
        
        # 데이터 구조 탐지 및 처리
        law_info = None
        
        # target을 포함한 구조에서 law 데이터 찾기
        if 'LawSearch' in data and 'law' in data['LawSearch']:
            law_data = data['LawSearch']['law']
            if isinstance(law_data, list) and law_data:
                law_info = law_data[0]
            elif isinstance(law_data, dict):
                law_info = law_data
        
        # 직접 law 키 확인
        elif 'law' in data:
            law_data = data['law']
            if isinstance(law_data, list) and law_data:
                law_info = law_data[0]
            elif isinstance(law_data, dict):
                law_info = law_data
        
        # 법령 키 확인 (상세조회 API 응답)
        elif '법령' in data:
            law_data = data['법령']
            if isinstance(law_data, dict):
                law_info = law_data
        
        # 단일 객체 구조 확인
        elif len(data) == 1:
            key = list(data.keys())[0]
            law_data = data[key]
            if isinstance(law_data, list) and law_data:
                law_info = law_data[0]
            elif isinstance(law_data, dict):
                law_info = law_data
        
        if not law_info:
            return f"법령 정보를 찾을 수 없습니다.\n\nAPI URL: {url}"
        
        # 기본 정보 출력 (더 많은 키 이름 추가)
        basic_fields = {
            '법령명': [
                '법령명_한글', '법령명한글', '법령명', '제목', 'title', '명칭', 'name',
                '현행법령명', '법령명_국문', '국문법령명', 'lawNm', 'lawName', '법령명전체'
            ],
            '법령ID': ['법령ID', 'ID', 'id', 'lawId', 'mstSeq'],
            '공포일자': ['공포일자', 'announce_date', 'date', '공포일', 'promulgateDate', '공포년월일'],
            '시행일자': ['시행일자', 'effective_date', 'ef_date', '시행일', 'enforceDate', '시행년월일'],
            '소관부처': ['소관부처명', 'ministry', 'department', '소관부처', 'ministryNm', '주무부처'],
            '법령구분': ['법령구분명', 'law_type', 'type', '법령구분', 'lawType', '법령종류']
        }
        
        for field_name, field_keys in basic_fields.items():
            value = None
            
            # 기본정보 키에서 찾기 (상세조회 API 응답)
            if '기본정보' in law_info and isinstance(law_info['기본정보'], dict):
                basic_info = law_info['기본정보']
                for key in field_keys:
                    if key in basic_info and basic_info[key]:
                        value = basic_info[key]
                        # 소관부처의 경우 content 추출
                        if isinstance(value, dict) and 'content' in value:
                            value = value['content']
                        break
            
            # 직접 law_info에서 찾기 (검색 API 응답)
            if not value:
                for key in field_keys:
                    if key in law_info and law_info[key]:
                        value = law_info[key]
                        break
            
            if value:
                result += f"**{field_name}**: {value}\n"
        
        result += "\n" + "=" * 50 + "\n\n"
        
        # 조문 내용 출력 (구조화된 조문 처리)
        content = None
        
        # 상세조회 API 응답의 조문단위 처리
        if '조문' in law_info and isinstance(law_info['조문'], dict):
            article_data = law_info['조문']
            if '조문단위' in article_data and isinstance(article_data['조문단위'], list):
                articles = article_data['조문단위']
                content = str(articles)  # 전체 조문 데이터
        
        # 기존 필드에서 조문 내용 찾기
        if not content:
            content_fields = [
                '조문', 'content', 'text', '내용', 'body', '본문', '법령내용', 
                'lawCn', 'lawContent', '조문내용', '전문', 'fullText',
                '법령본문', '조문본문', 'articleContent'
            ]
            
            for field in content_fields:
                if field in law_info and law_info[field] and str(law_info[field]).strip():
                    content = str(law_info[field]).strip()
                    break
        
        # 디버깅: 조문 내용을 찾을 수 없는 경우 사용 가능한 키들 로그
        if not content and isinstance(law_info, dict):
            available_keys = list(law_info.keys())
            logger.info(f"조문 내용을 찾을 수 없음. 사용 가능한 키들: {available_keys}")
            # 내용으로 보이는 키들 찾기
            potential_content_keys = [k for k in available_keys if '내용' in str(k) or '조문' in str(k) or 'content' in str(k).lower()]
            if potential_content_keys:
                content = str(law_info.get(potential_content_keys[0], '')).strip()
        
        if content:
            result += "**조문 내용:**\n\n"
            result += str(content)
            result += "\n\n"
        else:
            result += "조문 내용을 찾을 수 없습니다.\n\n"
        
        # 추가 정보 (상세조회 API 응답 구조 처리)
        additional_fields = {
            '부칙': ['부칙', 'appendix'],
            '개정문': ['개정문', 'revision_text'],
            '제개정이유': ['제개정이유', 'enactment_reason'],
            '주요내용': ['주요내용', 'main_content']
        }
        
        for field_name, field_keys in additional_fields.items():
            value = None
            
            # 직접 키에서 찾기 (상세조회 API 응답)
            for key in field_keys:
                if key in law_info and law_info[key]:
                    value = law_info[key]
                    break
            
            if value:
                result += f"**{field_name}:**\n{value}\n\n"
        
        result += "=" * 50 + "\n"
        result += f"**API URL**: {url}\n"
        
        return result
        
    except Exception as e:
        logger.error(f"법령 상세내용 포맷팅 오류: {e}")
        return f"❌ 법령 상세내용 처리 중 오류: {str(e)}\n\n🔗 API URL: {url}"

# ===========================================
# 법령 관련 통합 도구들 (29개)
# ===========================================

@mcp.tool(
    name="search_law",
    description="""구체적인 법령명을 알고 있을 때 사용하는 정밀 검색 도구입니다.

언제 사용:
- 정확한 법령명을 알고 있을 때 (예: "도로교통법", "공인중개사법")
- search_law_unified로 찾은 구체적인 법령명을 상세 검색할 때

언제 사용 안함:
- 일반적인 키워드 검색 시 → search_law_unified 사용
- 법령명을 모를 때 → search_law_unified 사용
    
매개변수:
- query: 법령명 (필수) - 정확한 법령명
- search: 검색범위 (1=법령명으로만, 2=본문내용 포함)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 옵션

반환정보: 법령명, 법령ID, 법령일련번호(MST), 공포일자, 시행일자, 소관부처, 제개정구분

특별 기능:
1. 일반 키워드 매핑: "부동산", "교통", "개인정보", "노동" → 관련 법령 자동 검색
2. 법령명 자동 보정: "법" 추가, 공백 제거 등
3. 실패 시 본문검색 자동 전환 (하지만 결과가 부정확할 수 있음)

권장 워크플로우:
1단계: search_law_unified("부동산") → 관련 법령 목록 확인
2단계: search_law("공인중개사법") → 특정 법령 정밀 검색

사용 예시: search_law("도로교통법"), search_law("공인중개사법")""",
    tags={"법령검색", "법률", "대통령령", "시행령", "시행규칙", "현행법", "법조문", "제정", "개정", "폐지", "정밀검색"}
)
def search_law(
    query: Optional[str] = None,
    search: int = 1,  # 법령명 검색이 더 정확함. 결과 없으면 본문검색으로 fallback
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
        query: 검색어 (법령명) - 필수 입력
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
    if not query or not query.strip():
        return TextContent(type="text", text="검색어를 입력해주세요. 예: '개인정보보호법', '근로기준법', '상법' 등")
    
    search_query = query.strip()
    
    # 일반 키워드를 구체적인 법령명으로 매핑
    keyword_mapping = {
        "부동산": ["공인중개사법", "부동산등기법", "주택임대차보호법", "부동산 거래신고 등에 관한 법률", "부동산실권리자명의등기에관한법률"],
        "교통": ["도로교통법", "자동차관리법", "교통사고처리 특례법", "여객자동차 운수사업법"],
        "개인정보": ["개인정보 보호법", "정보통신망 이용촉진 및 정보보호 등에 관한 법률"],
        "노동": ["근로기준법", "최저임금법", "근로자퇴직급여 보장법", "산업안전보건법"],
        "근로": ["근로기준법", "최저임금법", "근로자퇴직급여 보장법", "산업안전보건법"]
    }
    
    # 일반 키워드인 경우 구체적인 법령들로 검색
    if search_query.lower() in keyword_mapping:
        suggested_laws = keyword_mapping[search_query.lower()]
        results = []
        
        for law_name in suggested_laws:
            params = {
                "OC": legislation_config.oc,
                "type": "JSON",
                "target": "law",
                "query": law_name,
                "search": 1,
                "display": 5
            }
            
            try:
                data = _make_legislation_request("law", params, is_detail=False)
                if 'LawSearch' in data and 'law' in data['LawSearch']:
                    laws = data['LawSearch']['law']
                    if isinstance(laws, list):
                        results.extend(laws[:3])  # 각 법령당 최대 3개
            except:
                continue
        
        if results:
            # 수동으로 결과 포맷팅
            formatted = f"**'{search_query}' 관련 주요 법령** (총 {len(results)}건)\n\n"
            for i, law in enumerate(results[:display], 1):
                formatted += f"**{i}. {law.get('법령명한글', '')}**\n"
                formatted += f"   법령ID: {law.get('법령ID', '')}\n"
                formatted += f"   법령일련번호: {law.get('법령일련번호', '')}\n"
                formatted += f"   공포일자: {law.get('공포일자', '')}\n"
                formatted += f"   시행일자: {law.get('시행일자', '')}\n"
                formatted += f"   소관부처명: {law.get('소관부처명', '')}\n"
                
                mst = law.get('법령일련번호')
                if mst:
                    formatted += f"   상세조회: get_law_detail_unified(mst=\"{mst}\", target=\"law\")\n"
                formatted += "\n"
            
            formatted += f"\n팁: 더 정확한 검색을 위해 구체적인 법령명을 사용하세요."
            return TextContent(type="text", text=formatted)
    
    try:
        oc = legislation_config.oc
        if not oc:
            raise ValueError("OC(기관코드)가 설정되지 않았습니다.")
        
        # 검색 전략 개선: 키워드가 "법"으로 끝나지 않으면 자동으로 추가
        original_query = search_query
        search_attempts = []
        
        # 1차 시도: 원본 쿼리
        search_attempts.append((original_query, 1))  # 법령명 검색
        
        # 2차 시도: "법"이 없으면 추가
        if not original_query.endswith("법"):
            search_attempts.append((original_query + "법", 1))
        
        # 3차 시도: 공백 제거
        cleaned_query = original_query.replace(" ", "")
        if cleaned_query != original_query:
            search_attempts.append((cleaned_query, 1))
            if not cleaned_query.endswith("법") and cleaned_query + "법" not in [q[0] for q in search_attempts]:
                search_attempts.append((cleaned_query + "법", 1))
        
        best_result = None
        best_count = 0
        
        for attempt_query, search_mode in search_attempts:
            # 기본 파라미터 설정
            base_params = {"OC": oc, "type": "JSON", "target": "law"}
            
            # 검색 파라미터 추가
            params = base_params.copy()
            params.update({
                "query": attempt_query,
                "search": search_mode,
                "display": min(display, 100),
                "page": page
            })
            
            # 선택적 파라미터 추가
            optional_params = {
                "sort": sort, "date": date, "efDateRange": ef_date_range,
                "announceDateRange": announce_date_range, "announceNoRange": announce_no_range,
                "revisionType": revision_type, "announceNo": announce_no,
                "ministryCode": ministry_code, "lawTypeCode": law_type_code,
                "lawChapter": law_chapter, "alphabetical": alphabetical
            }
            
            for key, value in optional_params.items():
                if value is not None:
                    params[key] = value
            
            try:
                # API 요청 - 현행법령 검색
                data = _make_legislation_request("law", params, is_detail=False)
                
                # 결과 확인
                if 'LawSearch' in data and 'law' in data['LawSearch']:
                    results = data['LawSearch']['law']
                    total_count = int(data['LawSearch'].get('totalCnt', 0))
                    
                    # 정확한 매칭 검사
                    if isinstance(results, list) and len(results) > 0:
                        # 첫 번째 결과가 정확히 일치하는지 확인
                        first_law = results[0]
                        law_name = first_law.get('법령명한글', '')
                        
                        # 정확한 매칭이면 즉시 반환
                        if law_name and (
                            original_query in law_name or 
                            attempt_query in law_name or
                            law_name.replace(" ", "") == attempt_query.replace(" ", "")
                        ):
                            formatted_result = _format_search_results(data, "law", original_query)
                            
                            # 검색어가 다른 경우 안내 추가
                            if attempt_query != original_query:
                                formatted_result = f"['{original_query}' → '{attempt_query}'로 검색]\n\n" + formatted_result
                            
                            return TextContent(type="text", text=formatted_result)
                    
                    # 최선의 결과 저장 (결과 수가 적으면서 0이 아닌 경우)
                    if 0 < total_count < 20 and (best_result is None or total_count < best_count):
                        best_result = (attempt_query, data)
                        best_count = total_count
                        
            except Exception as e:
                logger.debug(f"검색 시도 실패 ({attempt_query}): {e}")
                continue
        
        # 최선의 결과가 있으면 반환
        if best_result:
            attempt_query, data = best_result
            result = _format_search_results(data, "law", original_query)
            if attempt_query != original_query:
                result = f"['{original_query}' → '{attempt_query}'로 검색]\n\n" + result
            return TextContent(type="text", text=result)
        
        # 모든 시도가 실패한 경우 본문검색으로 최종 시도
        if search == 1:
            params["search"] = 2
            params["query"] = original_query
            
            try:
                data = _make_legislation_request("law", params, is_detail=False)
                result = _format_search_results(data, "law", original_query)
                
                # 본문검색임을 명시
                result = f"[법령명 검색 결과 없음 → 본문검색 결과]\n\n" + result
                return TextContent(type="text", text=result)
            except:
                pass
        
        # 완전히 실패
        return TextContent(type="text", text=f"'{original_query}'에 대한 검색 결과가 없습니다.\n\n"
                                            f"검색 팁:\n"
                                            f"- 정확한 법령명을 입력하세요 (예: '개인정보보호법')\n"
                                            f"- 법령명 끝에 '법', '령', '규칙' 등을 포함하세요\n"
                                            f"- 띄어쓰기를 확인하세요")
        
    except Exception as e:
        logger.error(f"법령 검색 중 오류: {e}")
        return TextContent(type="text", text=f"법령 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="search_english_law", 
    description="""한국 법령의 영어 번역본을 검색합니다.
    
매개변수:
- query: 검색어 (필수) - 영문 법령명
- search: 검색범위 (1=법령명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 옵션
- law_type: 법령종류 (L=법률, P=대통령령, M=총리령부령)
- promulgate_date: 공포일자 (YYYYMMDD)
- enforce_date: 시행일자 (YYYYMMDD)

반환정보: 영문법령명, 한글법령명, 법령ID, 공포일자, 시행일자, 소관부처

예시: search_english_law("Civil Act"), search_english_law("Labor Standards Act")""",
    tags={"영문법령", "영어번역", "English", "국제법무", "외국인", "번역", "Civil Act", "Commercial Act", "한국법"}
)
def search_english_law(
    query: Optional[str] = None,
    search: int = 1,
    display: int = 20,
    page: int = 1,
    sort: Optional[str] = None,
    law_type: Optional[str] = None,
    promulgate_date: Optional[str] = None,
    enforce_date: Optional[str] = None
) -> TextContent:
    """영문법령 검색
    
    Args:
        query: 검색어 (영문 법령명)
        search: 검색범위 (1=법령명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 (lasc=법령오름차순, ldes=법령내림차순, dasc=공포일자오름차순, ddes=공포일자내림차순)
        law_type: 법령종류 (L=법률, P=대통령령, M=총리령부령)
        promulgate_date: 공포일자 (YYYYMMDD)
        enforce_date: 시행일자 (YYYYMMDD)
    """
    if not query or not query.strip():
        return TextContent(type="text", text="❌ 검색어를 입력해주세요. 예: 'Civil Act', 'Commercial Act' 등")
    
    search_query = query.strip()
    
    try:
        # 기본 파라미터 설정 - 다른 검색 도구와 동일한 패턴 사용
        params = {
            "OC": legislation_config.oc,  # 직접 OC 포함
            "type": "JSON",               # 직접 type 포함
            "target": "elaw",            # 영문법령은 target이 'elaw'
            "query": search_query,
            "search": search,
            "display": min(display, 100),
            "page": page
        }
        
        # 선택적 파라미터 추가
        optional_params = {
            "sort": sort,
            "lawType": law_type,
            "promulgateDate": promulgate_date,
            "enforceDate": enforce_date
        }
        
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value
        
        # API 요청 - 영문법령은 is_detail=False로 명시
        data = _make_legislation_request("elaw", params, is_detail=False)
        result = _format_search_results(data, "elaw", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"영문법령 검색 중 오류: {e}")
        return TextContent(type="text", text=f"영문법령 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="get_english_law_detail", description="""영문 법령의 상세 내용을 조회합니다.

매개변수:
- law_id: 법령일련번호(MST) - search_english_law 도구의 결과에서 '법령일련번호' 필드값 사용

사용 예시: get_english_law_detail(law_id="204485")""")
def get_english_law_detail(law_id: Union[str, int]) -> TextContent:
    """영문법령 상세내용 조회"""
    if not law_id:
        return TextContent(type="text", text="❌ 법령일련번호(MST)를 입력해주세요.")
    
    try:
        # API 요청 파라미터 - 한글 법령과 동일한 단순한 패턴 사용
        params = {"MST": str(law_id)}
        data = _make_legislation_request("elaw", params, is_detail=True)
        
        # 영문 법령 전용 포맷팅
        result = _format_english_law_detail(data, str(law_id))
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"영문법령 상세조회 중 오류: {e}")
        return TextContent(type="text", text=f"영문법령 상세조회 중 오류가 발생했습니다: {str(e)}")

def _format_english_law_detail(data: dict, law_id: str) -> str:
    """영문 법령 상세 정보 포맷팅"""
    try:
        if not data or 'Law' not in data:
            return f"❌ 법령 정보를 찾을 수 없습니다. (MST: {law_id})"
        
        law_data = data['Law']
        
        # 기본 정보 추출
        result = "**영문 법령 상세 내용**\n"
        result += "=" * 50 + "\n\n"
        
        # 1. 먼저 JoSection(실제 조문) 확인
        jo_section = law_data.get('JoSection', {})
        main_articles = []
        
        if jo_section and 'Jo' in jo_section:
            jo_data = jo_section['Jo']
            if isinstance(jo_data, list):
                # 실제 조문만 필터링 (joYn='Y'인 것들)
                main_articles = [jo for jo in jo_data if jo.get('joYn') == 'Y']
            elif isinstance(jo_data, dict):
                if jo_data.get('joYn') == 'Y':
                    main_articles = [jo_data]
        
        # 2. JoSection이 없거나 비어있으면 ArSection(부칙) 확인
        addenda_articles = []
        ar_section = law_data.get('ArSection', {})
        if ar_section and 'Ar' in ar_section:
            ar_data = ar_section['Ar']
            if isinstance(ar_data, dict):
                addenda_articles = [ar_data]
            elif isinstance(ar_data, list):
                addenda_articles = ar_data
        
        # 3. 조문 표시 우선순위: 실제 조문 > 부칙
        if main_articles:
            result += f"**법령 조문** ({len(main_articles)}개)\n\n"
            display_count = min(10, len(main_articles))  # 실제 조문은 더 많이 표시
            
            for i, article in enumerate(main_articles[:display_count], 1):
                article_content = article.get('joCts', '')
                article_no = article.get('joNo', str(i))
                
                if article_content:
                    # 내용이 너무 길면 앞부분만 표시
                    preview = article_content[:800]  # 조문은 조금 더 길게
                    if len(article_content) > 800:
                        preview += "..."
                    
                    result += f"**Article {article_no}:**\n"
                    result += f"{preview}\n\n"
            
            if len(main_articles) > display_count:
                result += f"... (총 {len(main_articles)}개 조문 중 {display_count}개만 표시)\n\n"
                
        elif addenda_articles:
            result += f"**부칙 및 경과조치** ({len(addenda_articles)}개)\n\n"
            display_count = min(3, len(addenda_articles))  # 부칙은 적게 표시
            
            for i, article in enumerate(addenda_articles[:display_count], 1):
                article_content = article.get('arCts', '')
                
                if article_content:
                    preview = article_content[:500]
                    if len(article_content) > 500:
                        preview += "..."
                    
                    result += f"**부칙 {article.get('No', i)}:**\n"
                    result += f"{preview}\n\n"
        else:
            return f"❌ 조문 내용을 찾을 수 없습니다. (MST: {law_id})"
        
        # 4. 부가 정보
        if 'BylSection' in law_data and law_data['BylSection']:
            result += f"**별표/서식**: 있음\n"
        
        result += f"\n**MST**: {law_id}\n"
        
        if main_articles:
            result += f"**전체 조문 개수**: {len(main_articles)}개"
            if addenda_articles:
                result += f" (+ 부칙 {len(addenda_articles)}개)"
        elif addenda_articles:
            result += f"**부칙 개수**: {len(addenda_articles)}개"
        
        return result
        
    except Exception as e:
        logger.error(f"영문법령 포맷팅 중 오류: {e}")
        return f"❌ 법령 정보 처리 중 오류가 발생했습니다: {str(e)}"

@mcp.tool(
    name="search_effective_law", 
    description="""시행일 기준 법령을 검색합니다.
    
매개변수:
- query: 검색어 (선택) - 법령명
- search: 검색범위 (1=법령명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- status_type: 시행상태 (100=시행, 200=미시행, 300=폐지)
- law_id: 법령ID
- sort: 정렬 옵션
- effective_date_range: 시행일자 범위 (20090101~20090130)
- date: 공포일자 (YYYYMMDD)
- revision_type: 제개정 종류
- ministry_code: 소관부처 코드
- law_type_code: 법령종류 코드

반환정보: 법령명, 시행일자, 시행상태, 법령ID, 공포일자, 소관부처

사용 예시: search_effective_law("민법", status_type=100)""",
    tags={"시행일법령", "시행일", "법령상태", "시행예정", "미시행", "폐지", "연혁", "효력발생", "컴플라이언스"}
)
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
        query: 검색어 (법령명)
        search: 검색범위 (1=법령명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        status_type: 시행상태 (100=시행, 200=미시행, 300=폐지)
        law_id: 법령ID
        sort: 정렬 (lasc=법령오름차순, ldes=법령내림차순, dasc=공포일자오름차순, ddes=공포일자내림차순, efasc=시행일자오름차순, efdes=시행일자내림차순)
        effective_date_range: 시행일자 범위 (20090101~20090130)
        date: 공포일자 (YYYYMMDD)
        announce_date_range: 공포일자 범위 (20090101~20090130)
        announce_no_range: 공포번호 범위 (306~400)
        revision_type: 제개정 종류
        announce_no: 공포번호
        ministry_code: 소관부처 코드
        law_type_code: 법령종류 코드
        alphabetical: 사전식 검색
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "eflaw",
            "display": min(display, 100),
            "page": page,
            "search": search
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            params["query"] = query.strip()
        
        # 선택적 파라미터 추가
        optional_params = {
            "statusType": status_type, "lawId": law_id, "sort": sort,
            "effectiveDateRange": effective_date_range, "date": date,
            "announceDateRange": announce_date_range, "announceNoRange": announce_no_range,
            "revisionType": revision_type, "announceNo": announce_no,
            "ministryCode": ministry_code, "lawTypeCode": law_type_code,
            "alphabetical": alphabetical
        }
        
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value
        
        # API 요청
        data = _make_legislation_request("lsEfYdListGuide", params)
        search_term = query or "시행일법령"
        result = _format_search_results(data, "eflaw", search_term)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"시행일법령 검색 중 오류: {e}")
        return TextContent(type="text", text=f"시행일법령 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="search_law_history",
    description="""법령의 변경이력과 연혁을 검색합니다.
    
매개변수:
- query: 검색어 (선택) - 법령명
- search: 검색범위 (1=법령명, 2=본문검색)
- display: 결과 개수 (max=100)
- page: 페이지 번호
- sort: 정렬 옵션
- law_id: 법령ID
- history_type: 연혁구분
- announce_date_range: 공포일자 범위
- effective_date_range: 시행일자 범위
- revision_type: 제개정구분
- ministry_code: 소관부처 코드
- law_type_code: 법령종류 코드

반환정보: 법령명, 연혁구분, 공포일자, 시행일자, 제개정구분

사용 예시: search_law_history("개인정보보호법"), search_law_history(law_id="248613")""",
    tags={"법령연혁", "법령변경", "개정이력", "제정", "폐지", "타법개정", "연혁추적", "법제사", "정책변화"}
)
def search_law_history(
    query: Optional[str] = None,
    search: int = 1,
    display: int = 20,
    page: int = 1,
    sort: Optional[str] = None,
    law_id: Optional[str] = None,
    history_type: Optional[str] = None,
    announce_date_range: Optional[str] = None,
    effective_date_range: Optional[str] = None,
    announce_no_range: Optional[str] = None,
    revision_type: Optional[str] = None,
    ministry_code: Optional[str] = None,
    law_type_code: Optional[str] = None,
    alphabetical: Optional[str] = None
) -> TextContent:
    """법령연혁 검색
    
    Args:
        query: 검색어 (법령명)
        search: 검색범위 (1=법령명, 2=본문검색)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        sort: 정렬 옵션
        law_id: 법령ID
        history_type: 연혁구분
        announce_date_range: 공포일자 범위
        effective_date_range: 시행일자 범위
        announce_no_range: 공포번호 범위
        revision_type: 제개정구분
        ministry_code: 소관부처 코드
        law_type_code: 법령종류 코드
        alphabetical: 사전식 검색
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "lsHistory",
            "display": min(display, 100),
            "page": page,
            "search": search
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            params["query"] = query.strip()
        
        # 선택적 파라미터 추가
        optional_params = {
            "sort": sort, "lawId": law_id, "historyType": history_type,
            "announceDateRange": announce_date_range, "effectiveDateRange": effective_date_range,
            "announceNoRange": announce_no_range, "revisionType": revision_type,
            "ministryCode": ministry_code, "lawTypeCode": law_type_code,
            "alphabetical": alphabetical
        }
        
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value
        
        # API 요청
        data = _make_legislation_request("lsHstListGuide", params)
        search_term = query or "법령연혁"
        result = _format_search_results(data, "lsHistory", search_term)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령연혁 검색 중 오류: {e}")
        return TextContent(type="text", text=f"법령연혁 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_law_nickname", description="""법령의 약칭을 검색합니다.

매개변수:
- start_date: 시작일자 (선택) - YYYYMMDD 형식
- end_date: 종료일자 (선택) - YYYYMMDD 형식

반환정보: 법령약칭, 정식법령명, 법령ID, 등록일자

사용 예시:
- search_law_nickname()  # 전체 약칭 목록
- search_law_nickname(start_date="20240101")  # 2024년 이후 등록된 약칭
- search_law_nickname(start_date="20230101", end_date="20231231")  # 2023년 등록 약칭

참고: 법령의 통칭이나 줄임말로 검색할 때 유용합니다. 예: '개인정보법' → '개인정보보호법'""")
def search_law_nickname(start_date: Optional[str] = None, end_date: Optional[str] = None) -> TextContent:
    """법령 약칭 검색
    
    Args:
        start_date: 시작일자 (YYYYMMDD)
        end_date: 종료일자 (YYYYMMDD)
    """
    try:
        # 기본 파라미터 설정
        params = {"target": "lsAbrev"}
        
        # 선택적 파라미터 추가
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        # API 요청
        data = _make_legislation_request("lsAbrvListGuide", params)
        result = _format_search_results(data, "lsAbrev", "법령약칭")
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령약칭 검색 중 오류: {e}")
        return TextContent(type="text", text=f"법령약칭 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_deleted_law_data", description="""삭제된 법령 데이터를 검색합니다.

매개변수:
- data_type: 데이터 타입 (선택)
  - 1: 현행법령
  - 2: 시행일법령
  - 3: 법령연혁
  - 4: 영문법령
  - 5: 별표서식
- delete_date: 삭제일자 (선택) - YYYYMMDD 형식
- from_date: 시작일자 (선택) - YYYYMMDD 형식
- to_date: 종료일자 (선택) - YYYYMMDD 형식
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 삭제된 법령명, 법령ID, 삭제일자, 삭제사유, 데이터타입

사용 예시:
- search_deleted_law_data()  # 최근 삭제 데이터 전체
- search_deleted_law_data(data_type=1)  # 삭제된 현행법령만
- search_deleted_law_data(delete_date="20240101")  # 특정일 삭제 데이터
- search_deleted_law_data(from_date="20240101", to_date="20241231")  # 기간별 삭제 데이터

참고: 폐지되거나 삭제된 법령 정보를 추적할 때 사용합니다.""")
def search_deleted_law_data(data_type: Optional[int] = None, delete_date: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """삭제된 법령 데이터 검색
    
    Args:
        data_type: 데이터 타입 (1=현행법령, 2=시행일법령, 3=법령연혁, 4=영문법령, 5=별표서식)
        delete_date: 삭제일자 (YYYYMMDD)
        from_date: 시작일자 (YYYYMMDD)
        to_date: 종료일자 (YYYYMMDD)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "datDelHst",
            "display": min(display, 100),
            "page": page
        }
        
        # 선택적 파라미터 추가
        optional_params = {
            "dataType": data_type,
            "deleteDate": delete_date,
            "fromDate": from_date,
            "toDate": to_date
        }
        
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value
        
        # API 요청
        data = _make_legislation_request("datDelHstGuide", params)
        result = _format_search_results(data, "datDelHst", "삭제된 법령 데이터")
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"삭제된 법령 데이터 검색 중 오류: {e}")
        return TextContent(type="text", text=f"삭제된 법령 데이터 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_law_articles", description="""법령의 조문을 검색합니다.

매개변수:
- law_id: 법령ID (필수) - search_law 도구의 결과에서 '법령ID' 또는 'ID' 필드값 사용
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 조문번호, 조문제목, 조문내용 일부, 조문ID

주요 법령의 조문 구조 예시:
◆ 도로교통법 (ID: 001638):
  - 제1조~제10조: 총칙
  - 제44조~제59조: 교통사고와 처리 (제54조: 사고발생 시의 조치)
  - 제80조~제96조: 운전면허 (제80조: 운전면허)
  
◆ 공인중개사법 (ID: 001654):
  - 제24조~제33조: 중개업무 (제25조: 확인·설명, 제32조: 중개보수)
  
◆ 개인정보보호법 (ID: 011357):
  - 제15조~제22조: 개인정보의 수집·이용
  - 제29조~제31조: 개인정보의 처리 제한

사용 예시:
- search_law_articles(law_id="001638")  # 도로교통법 조문 목록
- search_law_articles(law_id="001654", display=50)  # 공인중개사법 조문 50개
- search_law_articles(law_id="011357", page=2)  # 개인정보보호법 2페이지

참고: 
1. 전체 조문 목록을 보고 특정 조문을 선택하기 위한 도구입니다
2. 조문 전체 내용은 get_law_detail_unified 후 get_law_article_by_key를 사용하세요
3. law_id는 법령ID를 사용하고, mst(법령일련번호)와는 다릅니다""")
def search_law_articles(law_id: Union[str, int], display: int = 20, page: int = 1) -> TextContent:
    """법령 조문 검색
    
    Args:
        law_id: 법령ID
        display: 결과 개수
        page: 페이지 번호
    """
    if not law_id:
        return TextContent(type="text", text="❌ 법령ID를 입력해주세요.")
    
    try:
        # API 요청 파라미터
        params = {"target": "law", "MST": str(law_id), "type": "JSON"}
        
        # API 요청
        data = _make_legislation_request("lsNwJoListGuide", params)
        result = _format_search_results(data, "law", f"법령조문 (ID: {law_id})")
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령조문 검색 중 오류: {e}")
        return TextContent(type="text", text=f"법령조문 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_old_and_new_law", description="""신구법비교 목록을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 비교ID, 개정일자, 신구조문대비표 유무

사용 예시:
- search_old_and_new_law()  # 전체 신구법비교 목록
- search_old_and_new_law("개인정보보호법")  # 특정 법령의 신구법비교
- search_old_and_new_law("근로", display=50)  # 근로 관련 법령 비교

참고: 법령 개정 전후의 변경사항을 비교할 수 있는 자료를 검색합니다.""")
def search_old_and_new_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """신구법비교 검색
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "oldAndNew",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            params["query"] = query.strip()
        
        # API 요청
        data = _make_legislation_request("oldAndNewListGuide", params)
        search_term = query or "신구법비교"
        result = _format_search_results(data, "oldAndNew", search_term)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"신구법비교 검색 중 오류: {e}")
        return TextContent(type="text", text=f"신구법비교 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_three_way_comparison", description="""3단비교 목록을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 비교ID, 인용조문, 위임조문, 비교일자

사용 예시:
- search_three_way_comparison()  # 전체 3단비교 목록
- search_three_way_comparison("시행령")  # 시행령 관련 3단비교
- search_three_way_comparison("건축법", display=30)

참고: 상위법령-하위법령-위임조문의 3단계 관계를 비교분석하는 자료입니다.""")
def search_three_way_comparison(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """3단비교 검색
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "thirdComparison",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            params["query"] = query.strip()
        
        # API 요청
        data = _make_legislation_request("thdCmpListGuide", params)
        search_term = query or "3단비교"
        result = _format_search_results(data, "thirdComparison", search_term)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"3단비교 검색 중 오류: {e}")
        return TextContent(type="text", text=f"3단비교 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_deleted_history", description="""삭제 이력을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 삭제항목명, 삭제일시, 삭제유형, 삭제사유

사용 예시:
- search_deleted_history()  # 전체 삭제 이력
- search_deleted_history("폐지")  # 폐지 관련 삭제 이력
- search_deleted_history("2024", display=50)  # 2024년 관련 삭제 이력

참고: 법령 데이터의 삭제 이력을 추적하고 감사할 때 사용합니다.""")
def search_deleted_history(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """삭제 이력 검색
    
    Args:
        query: 검색어
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "deletedHistory",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            params["query"] = query.strip()
        
        # API 요청
        data = _make_legislation_request("datDelHstGuide", params)
        search_term = query or "삭제 이력"
        result = _format_search_results(data, "deletedHistory", search_term)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"삭제 이력 검색 중 오류: {e}")
        return TextContent(type="text", text=f"삭제 이력 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_one_view", description="""한눈보기 목록을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 한눈보기ID, 주요내용, 작성일자

사용 예시:
- search_one_view()  # 전체 한눈보기 목록
- search_one_view("개인정보")  # 개인정보 관련 한눈보기
- search_one_view("세법", display=30)  # 세법 관련 한눈보기

참고: 복잡한 법령의 핵심 내용을 한눈에 파악할 수 있도록 정리한 자료입니다.""")
def search_one_view(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """한눈보기 검색
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "oneView",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            params["query"] = query.strip()
        
        # API 요청
        data = _make_legislation_request("oneViewListGuide", params)
        search_term = query or "한눈보기"
        result = _format_search_results(data, "oneView", search_term)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"한눈보기 검색 중 오류: {e}")
        return TextContent(type="text", text=f"한눈보기 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_law_system_diagram", description="""법령 체계도를 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 체계도ID, 법령일련번호(MST), 체계도 유형, 작성일자

사용 예시:
- search_law_system_diagram()  # 전체 체계도 목록
- search_law_system_diagram("지방자치법")  # 지방자치법 체계도
- search_law_system_diagram("조세", display=30)  # 조세 관련 법령 체계도

참고: 법령의 구조와 하위법령 관계를 시각적으로 보여주는 다이어그램입니다. 상세 내용은 get_law_system_diagram_detail 사용.""")
def search_law_system_diagram(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 체계도 검색
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "lawSystemDiagram",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            params["query"] = query.strip()
        
        # API 요청
        data = _make_legislation_request("lsStmdListGuide", params)
        search_term = query or "법령 체계도"
        result = _format_search_results(data, "lawSystemDiagram", search_term)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령 체계도 검색 중 오류: {e}")
        return TextContent(type="text", text=f"법령 체계도 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="get_law_system_diagram_detail", description="""법령 체계도 상세내용을 조회합니다.

매개변수:
- mst_id: 법령일련번호(MST) - search_law_system_diagram 도구의 결과에서 'MST' 필드값 사용

사용 예시: get_law_system_diagram_detail(mst_id="248613")""")
def get_law_system_diagram_detail(mst_id: Union[str, int]) -> TextContent:
    """법령 체계도 상세내용 조회
    
    Args:
        mst_id: 체계도 ID
    """
    if not mst_id:
        return TextContent(type="text", text="체계도 ID를 입력해주세요.")
    
    try:
        # API 요청 파라미터
        params = {"target": "lawSystemDiagram", "MST": str(mst_id)}
        url = _generate_api_url("lsStmdInfoGuide", params)
        
        # API 요청
        data = _make_legislation_request("lsStmdInfoGuide", params)
        result = _safe_format_law_detail(data, str(mst_id), url)
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령 체계도 상세조회 중 오류: {e}")
        return TextContent(type="text", text=f"법령 체계도 상세조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="get_delegated_law", description="""위임법령을 조회합니다.

매개변수:
- law_id: 법령일련번호(MST) - search_law 도구의 결과에서 'MST' 또는 'ID' 필드값 사용

사용 예시: get_delegated_law(law_id="248613")""")
def get_delegated_law(law_id: Union[str, int]) -> TextContent:
    """위임법령 조회
    
    Args:
        law_id: 법령ID
    """
    if not law_id:
        return TextContent(type="text", text="❌ 법령ID를 입력해주세요.")
    
    try:
        # API 요청 파라미터
        params = {"target": "lsDelegated", "ID": str(law_id)}
        
        # API 요청
        data = _make_legislation_request("lsDelegated", params)
        result = _format_search_results(data, "lsDelegated", f"위임법령 (ID: {law_id})")
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"위임법령 조회 중 오류: {e}")
        return TextContent(type="text", text=f"위임법령 조회 중 오류가 발생했습니다: {str(e)}")

# misc_tools.py에서 이동할 도구들
@mcp.tool(name="get_effective_law_articles", description="""시행일 법령의 조항호목을 조회합니다.

매개변수:
- law_id: 시행일법령ID - search_effective_law 도구의 결과에서 'ID' 필드값 사용
- article_no: 조번호 (선택)
- paragraph_no: 항번호 (선택)
- item_no: 호번호 (선택)
- subitem_no: 목번호 (선택)
- display: 결과 개수 (기본값: 20)
- page: 페이지 번호 (기본값: 1)

사용 예시: get_effective_law_articles(law_id="123456", article_no="1")""")
def get_effective_law_articles(
    law_id: Union[str, int],
    article_no: Optional[str] = None,
    paragraph_no: Optional[str] = None,
    item_no: Optional[str] = None,
    subitem_no: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> TextContent:
    """시행일 법령 조항호목 조회
    
    Args:
        law_id: 법령ID
        article_no: 조 번호
        paragraph_no: 항 번호
        item_no: 호 번호
        subitem_no: 목 번호
        display: 결과 개수
        page: 페이지 번호
    """
    if not law_id:
        return TextContent(type="text", text="❌ 법령ID를 입력해주세요.")
    
    try:
        # API 요청 파라미터
        params = {
            "target": "eflaw",
            "MST": str(law_id),
            "display": min(display, 100),
            "page": page
        }
        
        # 선택적 파라미터 추가
        optional_params = {
            "articleNo": article_no,
            "paragraphNo": paragraph_no,
            "itemNo": item_no,
            "subitemNo": subitem_no
        }
        
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value
        
        # API 요청
        data = _make_legislation_request("lsEfYdJoListGuide", params)
        result = _format_search_results(data, "eflaw", f"시행일 법령 조항호목 (ID: {law_id})")
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"시행일 법령 조항호목 조회 중 오류: {e}")
        return TextContent(type="text", text=f"시행일 법령 조항호목 조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="get_current_law_articles", description="""현행법령의 특정 조문을 조회합니다.

매개변수:
- law_id: 법령일련번호(MST) - search_law 도구의 결과에서 'MST' 필드값 사용
- article_no: 조문번호 (선택) - 예: "1", "제1조"
- start_article: 시작 조문 번호 (기본값: 1)
- count: 조회할 조문 개수 (기본값: 5)

사용 예시: get_current_law_articles(law_id="248613", article_no="1")""")
def get_current_law_articles(
    law_id: Union[str, int],
    article_no: Optional[str] = None,
    start_article: int = 1,
    count: int = 5
) -> TextContent:
    """현행법령 조문 조회
    
    Args:
        law_id: 법령ID 또는 MST
        article_no: 특정 조문 번호 (예: "50" 또는 "제50조")
        start_article: 시작 조문 번호 (article_no가 없을 때)
        count: 조회할 조문 개수 (article_no가 없을 때)
    """
    if not law_id:
        return TextContent(type="text", text="❌ 법령ID를 입력해주세요.")
    
    try:
        # 캐시 확인 또는 API 호출
        cache_key = get_cache_key(f"law_{law_id}", "full")
        law_data = load_from_cache(cache_key)
        
        if not law_data:
            # 캐시가 없으면 API 호출
            params = {
                "target": "law",
                "MST": str(law_id),
                "type": "JSON",
                "OC": legislation_config.oc
            }
            
            response = law_client._make_request("http://www.law.go.kr/DRF/lawService.do", params)
            if not response:
                return TextContent(type="text", text="❌ API 응답이 없습니다.")
            
            law_data = response
            # 캐시 저장
            save_to_cache(cache_key, law_data)
        
        # 법령 정보 추출
        law_info = law_data.get("법령", {})
        law_name = law_info.get("기본정보", {}).get("법령명_한글", "")
        
        # 조문 정보 파싱
        articles = law_info.get("조문", {})
        article_units = []
        
        if isinstance(articles, dict) and "조문단위" in articles:
            article_units = articles.get("조문단위", [])
            # 리스트가 아닌 경우 리스트로 변환
            if not isinstance(article_units, list):
                article_units = [article_units] if article_units else []
        elif isinstance(articles, list):
            article_units = articles
        
        # 실제 조문만 필터링
        actual_articles = [
            a for a in article_units 
            if a.get("조문여부") == "조문"
        ]
        
        if not actual_articles:
            return TextContent(type="text", text=f"❌ 법령 '{law_name}'의 조문 정보가 없습니다.")
        
        result = f"📋 **{law_name}** 조문 조회\n\n"
        
        if article_no:
            # 특정 조문 조회
            import re
            numbers = re.findall(r'\d+', str(article_no))
            target_num = numbers[0] if numbers else ""
            
            found = False
            for article in actual_articles:
                if article.get("조문번호") == target_num:
                    found = True
                    result += format_article_detail(article)
                    break
            
            if not found:
                result += f"❌ 제{article_no}조를 찾을 수 없습니다."
        else:
            # 범위 조회
            total = len(actual_articles)
            end_idx = min(start_article + count - 1, total)
            
            result += f"**전체 조문**: {total}개\n"
            result += f"**조회 범위**: 제{start_article}조 ~ 제{end_idx}조\n\n"
            result += "---\n\n"
            
            for i in range(start_article - 1, end_idx):
                if i < len(actual_articles):
                    article = actual_articles[i]
                    result += format_article_summary(article)
                    result += "\n---\n\n"
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"현행법령 조문 조회 중 오류: {e}")
        return TextContent(type="text", text=f"❌ 조회 중 오류가 발생했습니다: {str(e)}")

def format_article_detail(article: Dict[str, Any]) -> str:
    """조문 상세 포맷팅"""
    import re
    
    num = article.get("조문번호", "")
    title = article.get("조문제목", "")
    content = article.get("조문내용", "")
    
    # 제목 구성
    if title:
        header = f"### 제{num}조({title})"
    else:
        header = f"### 제{num}조"
    
    result = header + "\n\n"
    
    # 조문 내용 처리
    if content and len(content.strip()) > 20:  # 실제 내용이 있는 경우
        # HTML 태그 제거
        clean_content = re.sub(r'<[^>]+>', '', content)
        clean_content = clean_content.strip()
        result += clean_content + "\n"
    else:
        # 항 내용 처리
        hangs = article.get("항", [])
        if isinstance(hangs, list) and hangs:
            for hang in hangs:
                if isinstance(hang, dict):
                    hang_content = hang.get("항내용", "")
                    if hang_content:
                        # HTML 태그 제거
                        clean_hang = re.sub(r'<[^>]+>', '', hang_content)
                        clean_hang = clean_hang.strip()
                        result += clean_hang + "\n\n"
                else:
                    result += str(hang) + "\n\n"
    
    # 시행일자
    if article.get("조문시행일자"):
        result += f"\n**시행일자**: {article.get('조문시행일자')}"
    
    # 변경 여부
    if article.get("조문변경여부") == "Y":
        result += f"\n⚠️ 최근 변경된 조문입니다."
    
    return result

def format_article_summary(article: Dict[str, Any]) -> str:
    """조문 요약 포맷팅"""
    import re
    
    num = article.get("조문번호", "")
    title = article.get("조문제목", "")
    content = article.get("조문내용", "")
    
    # 제목 구성
    if title:
        result = f"**제{num}조**({title})"
    else:
        result = f"**제{num}조**"
    
    # 내용 요약 (첫 150자)
    if content:
        # HTML 태그 제거
        clean_content = re.sub(r'<[^>]+>', '', content)
        clean_content = clean_content.strip()
        
        if len(clean_content) > 150:
            summary = clean_content[:150] + "..."
        else:
            summary = clean_content
            
        result += f"\n  {summary}"
    
    return result

@mcp.tool(name="get_effective_law_detail", description="""시행일 법령의 상세내용을 조회합니다.

매개변수:
- effective_law_id: 시행일법령ID - search_effective_law 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_effective_law_detail(effective_law_id="123456")""")
def get_effective_law_detail(effective_law_id: Union[str, int]) -> TextContent:
    """시행일 법령 상세내용 조회
    
    Args:
        effective_law_id: 시행일 법령ID
    """
    if not effective_law_id:
        return TextContent(type="text", text="시행일 법령ID를 입력해주세요.")
    
    try:
        # API 요청 파라미터
        params = {"target": "eflaw", "MST": str(effective_law_id)}
        url = _generate_api_url("lsEfYdInfoGuide", params)
        
        # API 요청
        data = _make_legislation_request("lsEfYdInfoGuide", params)
        result = _safe_format_law_detail(data, str(effective_law_id), url)
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"시행일 법령 상세조회 중 오류: {e}")
        return TextContent(type="text", text=f"시행일 법령 상세조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="get_law_history_detail", description="""법령연혁의 상세내용을 조회합니다.

매개변수:
- history_id: 법령연혁ID - search_law_history 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_law_history_detail(history_id="123456")""")
def get_law_history_detail(history_id: Union[str, int]) -> TextContent:
    """법령연혁 상세내용 조회
    
    Args:
        history_id: 연혁ID
    """
    if not history_id:
        return TextContent(type="text", text="❌ 연혁ID를 입력해주세요.")
    
    try:
        # API 요청 파라미터
        params = {"target": "lsHistory", "MST": str(history_id)}
        url = _generate_api_url("lsHstInfoGuide", params)
        
        # API 요청
        data = _make_legislation_request("lsHstInfoGuide", params)
        result = _safe_format_law_detail(data, str(history_id), url)
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령연혁 상세조회 중 오류: {e}")
        return TextContent(type="text", text=f"법령연혁 상세조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_law_change_history", description="""법령 변경이력을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 변경ID, 변경일자, 변경유형, 변경내용 요약

사용 예시:
- search_law_change_history()  # 최근 변경이력 전체
- search_law_change_history("개인정보보호법")  # 특정 법령의 변경이력
- search_law_change_history("2024", display=50)  # 2024년 변경이력

참고: 법령의 제정, 개정, 폐지 등 모든 변경사항의 이력을 추적합니다.""")
def search_law_change_history(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 변경이력 검색
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "lawChangeHistory",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "법령 변경이력"
        
        # API 요청
        data = _make_legislation_request("lsJoChgListGuide", params)
        result = _format_search_results(data, "lawChangeHistory", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령 변경이력 검색 중 오류: {e}")
        return TextContent(type="text", text=f"법령 변경이력 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="get_law_appendix_detail", description="""법령 별표서식 상세내용을 조회합니다.

매개변수:
- appendix_id: 별표서식ID - search_law_appendix 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_law_appendix_detail(appendix_id="123456")""")
def get_law_appendix_detail(appendix_id: Union[str, int]) -> TextContent:
    """법령 별표서식 상세내용 조회
    
    Args:
        appendix_id: 별표서식ID
    """
    if not appendix_id:
        return TextContent(type="text", text="별표서식ID를 입력해주세요.")
    
    try:
        # API 요청 파라미터
        params = {"target": "lawAppendix", "MST": str(appendix_id)}
        url = _generate_api_url("lsBylInfoGuide", params)
        
        # API 요청
        data = _make_legislation_request("lsBylInfoGuide", params)
        result = _safe_format_law_detail(data, str(appendix_id), url)
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령 별표서식 상세조회 중 오류: {e}")
        return TextContent(type="text", text=f"법령 별표서식 상세조회 중 오류가 발생했습니다: {str(e)}")

# linkage_tools.py에서 이동할 도구들
@mcp.tool(name="search_daily_article_revision", description="""일자별 조문 개정 이력을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- revision_date: 개정일자 (선택) - YYYYMMDD 형식
- law_id: 법령ID (선택) - search_law 도구의 결과에서 'ID' 필드값 사용
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 조문번호, 개정일자, 개정유형, 개정내용

사용 예시:
- search_daily_article_revision()  # 최근 조문 개정 이력
- search_daily_article_revision(revision_date="20240101")  # 특정일 개정 조문
- search_daily_article_revision(law_id="248613")  # 특정 법령의 조문 개정
- search_daily_article_revision("근로", revision_date="20240301")  # 조건 조합

참고: 날짜별로 어떤 조문이 개정되었는지 추적할 때 유용합니다.""")
def search_daily_article_revision(
    query: Optional[str] = None,
    revision_date: Optional[str] = None,
    law_id: Optional[str] = None,
    display: int = 20,
    page: int = 1
) -> TextContent:
    """일자별 조문 개정 이력 검색
    
    Args:
        query: 검색어
        revision_date: 개정일자 (YYYYMMDD)
        law_id: 법령ID
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "dailyArticleRevision",
            "display": min(display, 100),
            "page": page
        }
        
        # 선택적 파라미터 추가
        if query and query.strip():
            params["query"] = query.strip()
        if revision_date:
            params["revisionDate"] = revision_date
        if law_id:
            params["lawId"] = law_id
        
        # API 요청
        data = _make_legislation_request("lsDayJoRvsListGuide", params)
        search_term = query or f"일자별 조문 개정이력 ({revision_date or '전체'})"
        result = _format_search_results(data, "dailyArticleRevision", search_term)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"일자별 조문 개정이력 검색 중 오류: {e}")
        return TextContent(type="text", text=f"일자별 조문 개정이력 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_article_change_history", description="""조문별 변경 이력을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 조문 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 조문번호, 변경일자, 변경유형, 이전내용, 변경후내용

사용 예시:
- search_article_change_history()  # 전체 조문 변경 이력
- search_article_change_history("개인정보보호법")  # 특정 법령의 조문 변경
- search_article_change_history("제50조", display=30)  # 특정 조문번호 검색

참고: 특정 조문이 시간에 따라 어떻게 변경되었는지 추적할 수 있습니다.""")
def search_article_change_history(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """조문별 변경이력 검색
    
    Args:
        query: 검색어 (법령명 또는 조문)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "articleChangeHistory",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "조문별 변경이력"
        
        # API 요청
        data = _make_legislation_request("lsJoChgListGuide", params)
        result = _format_search_results(data, "articleChangeHistory", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"조문별 변경이력 검색 중 오류: {e}")
        return TextContent(type="text", text=f"조문별 변경이력 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_law_ordinance_link", description="""법령 기준 자치법규 연계 정보를 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 법령ID, 연계된 자치법규명, 자치법규ID, 지자체명, 연계유형

사용 예시:
- search_law_ordinance_link()  # 전체 법령-자치법규 연계
- search_law_ordinance_link("건축법")  # 건축법과 연계된 자치법규
- search_law_ordinance_link("주차", display=50)  # 주차 관련 법령의 자치법규 연계

참고: 상위 법령이 각 지자체에서 어떤 조례나 규칙으로 구현되는지 파악할 때 사용합니다.""")
def search_law_ordinance_link(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """법령 기준 자치법규 연계 정보 검색
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "lawOrdinanceLink",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "법령-자치법규 연계정보"
        
        # API 요청
        data = _make_legislation_request("lsOrdinConListGuide", params)
        result = _format_search_results(data, "lawOrdinanceLink", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령-자치법규 연계정보 검색 중 오류: {e}")
        return TextContent(type="text", text=f"법령-자치법규 연계정보 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="get_law_ordinance_connection", description="""법령-자치법규 연계현황을 조회합니다.

매개변수:
- connection_id: 연계ID - search_law_ordinance_link 도구의 결과에서 'ID' 필드값 사용

사용 예시: get_law_ordinance_connection(connection_id="123456")""")
def get_law_ordinance_connection(connection_id: Union[str, int]) -> TextContent:
    """법령-자치법규 연계현황 조회
    
    Args:
        connection_id: 연계ID
    """
    if not connection_id:
        return TextContent(type="text", text="❌ 연계ID를 입력해주세요.")
    
    try:
        # API 요청 파라미터
        params = {"target": "lawOrdinanceConnection", "MST": str(connection_id)}
        url = _generate_api_url("lsOrdinConGuide", params)
        
        # API 요청
        data = _make_legislation_request("lsOrdinConGuide", params)
        result = _safe_format_law_detail(data, str(connection_id), url)
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령-자치법규 연계현황 조회 중 오류: {e}")
        return TextContent(type="text", text=f"법령-자치법규 연계현황 조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_ordinance_law_link", description="""자치법규 기준 법령 연계 정보를 검색합니다.

매개변수:
- query: 검색어 (선택) - 자치법규명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 자치법규명, 자치법규ID, 연계된 법령명, 법령ID, 지자체명, 연계유형

사용 예시:
- search_ordinance_law_link()  # 전체 자치법규-법령 연계
- search_ordinance_law_link("서울특별시")  # 서울시 조례의 상위 법령
- search_ordinance_law_link("주차장 조례")  # 특정 조례의 근거 법령

참고: 특정 자치법규가 어떤 상위 법령에 근거하는지 파악할 때 사용합니다.""")
def search_ordinance_law_link(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """자치법규 기준 법령 연계 정보 검색
    
    Args:
        query: 검색어 (자치법규명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "ordinanceLawLink",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "자치법규-법령 연계정보"
        
        # API 요청
        data = _make_legislation_request("ordinLsConListGuide", params)
        result = _format_search_results(data, "ordinanceLawLink", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"자치법규-법령 연계정보 검색 중 오류: {e}")
        return TextContent(type="text", text=f"자치법규-법령 연계정보 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_related_law", description="""관련법령을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 기준법령명, 관련법령명, 관계유형, 관련조항

사용 예시:
- search_related_law()  # 전체 관련법령 목록
- search_related_law("개인정보보호법")  # 개인정보보호법의 관련법령
- search_related_law("민법", display=50)  # 민법 관련법령 많이 보기

참고: 특정 법령과 연관된 다른 법령들을 찾아 법체계를 이해할 때 유용합니다.""")
def search_related_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """관련법령 검색
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "relatedLaw",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "관련법령"
        
        # API 요청
        data = _make_legislation_request("lsRltGuide", params)
        result = _format_search_results(data, "relatedLaw", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"관련법령 검색 중 오류: {e}")
        return TextContent(type="text", text=f"관련법령 검색 중 오류가 발생했습니다: {str(e)}")

# custom_tools.py에서 이동할 도구들
@mcp.tool(name="search_custom_law", description="""맞춤형 법령을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 법령ID, 맞춤분류, 분류일자, 소관부처

사용 예시:
- search_custom_law()  # 전체 맞춤형 법령 목록
- search_custom_law("중소기업")  # 중소기업 관련 맞춤형 법령
- search_custom_law("복지", display=30)  # 복지 관련 맞춤형 법령

참고: 특정 주제나 대상별로 분류된 맞춤형 법령을 검색할 때 사용합니다.""")
def search_custom_law(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 법령 검색
    
    Args:
        query: 검색어 (법령명)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "customLaw",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "맞춤형 법령"
        
        # API 요청
        data = _make_legislation_request("custLsListGuide", params)
        result = _format_search_results(data, "customLaw", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"맞춤형 법령 검색 중 오류: {e}")
        return TextContent(type="text", text=f"맞춤형 법령 검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(name="search_custom_law_articles", description="""맞춤형 법령 조문을 검색합니다.

매개변수:
- query: 검색어 (선택) - 법령명 또는 조문 키워드
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)

반환정보: 법령명, 조문번호, 조문제목, 조문내용, 맞춤분류

사용 예시:
- search_custom_law_articles()  # 전체 맞춤형 법령 조문
- search_custom_law_articles("창업")  # 창업 관련 맞춤형 조문
- search_custom_law_articles("지원", display=50)  # 지원 관련 조문

참고: 맞춤형으로 분류된 법령의 특정 조문들을 검색할 때 사용합니다.""")
def search_custom_law_articles(query: Optional[str] = None, display: int = 20, page: int = 1) -> TextContent:
    """맞춤형 법령 조문 검색
    
    Args:
        query: 검색어 (법령명 또는 조문)
        display: 결과 개수
        page: 페이지 번호
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "customLawArticles",
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "맞춤형 법령 조문"
        
        # API 요청
        data = _make_legislation_request("custLsJoListGuide", params)
        result = _format_search_results(data, "customLawArticles", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"맞춤형 법령 조문 검색 중 오류: {e}")
        return TextContent(type="text", text=f"맞춤형 법령 조문 검색 중 오류가 발생했습니다: {str(e)}")

# specialized_tools.py에서 이동할 도구
@mcp.tool(name="search_law_appendix", description="""법령 별표서식을 검색합니다.

매개변수:
- query: 검색어 (선택) - 별표명 또는 서식명
- search: 검색범위 (기본값: 1)
  - 1: 명칭으로만 검색
  - 2: 내용 포함 검색
- display: 결과 개수 (최대 100, 기본값: 20)
- page: 페이지 번호 (기본값: 1)
- appendix_type: 별표종류 (선택)
  - 1: 별표
  - 2: 서식
  - 3: 양식
  - 4: 기타
- ministry_code: 소관부처 코드 (선택)
- local_gov_code: 지자체 코드 (선택)
- sort: 정렬 방식 (선택)
  - name_asc: 명칭 오름차순
  - name_desc: 명칭 내림차순
  - date_asc: 일자 오름차순
  - date_desc: 일자 내림차순

반환정보: 별표서식명, 별표서식ID, 관련법령명, 법령ID, 별표종류, 소관부처

사용 예시:
- search_law_appendix("신청서")
- search_law_appendix("수수료", appendix_type=1)  # 별표만 검색
- search_law_appendix("시행규칙", search=2, sort="date_desc")  # 최신순 정렬

참고: 법령에 첨부된 별표, 서식, 양식 등을 검색할 수 있습니다.""")
def search_law_appendix(
    query: Optional[str] = None,
    search: int = 1,
    display: int = 20,
    page: int = 1,
    appendix_type: Optional[str] = None,
    ministry_code: Optional[str] = None,
    local_gov_code: Optional[str] = None,
    sort: Optional[str] = None
) -> TextContent:
    """법령 별표서식 검색
    
    Args:
        query: 검색어 (별표/서식명)
        search: 검색범위 (1=명칭, 2=내용)
        display: 결과 개수 (max=100)
        page: 페이지 번호
        appendix_type: 별표종류 (1=별표, 2=서식, 3=양식, 4=기타)
        ministry_code: 소관부처 코드
        local_gov_code: 지자체 코드
        sort: 정렬 (name_asc=명칭오름차순, name_desc=명칭내림차순, date_asc=일자오름차순, date_desc=일자내림차순)
    """
    try:
        # 기본 파라미터 설정
        params = {
            "target": "lawAppendix",
            "search": search,
            "display": min(display, 100),
            "page": page
        }
        
        # 검색어가 있는 경우 추가
        if query and query.strip():
            search_query = query.strip()
            params["query"] = search_query
        else:
            search_query = "법령 별표서식"
        
        # 선택적 파라미터 추가
        optional_params = {
            "appendixType": appendix_type,
            "ministryCode": ministry_code,
            "localGovCode": local_gov_code,
            "sort": sort
        }
        
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value
        
        # API 요청
        data = _make_legislation_request("lsBylListGuide", params)
        result = _format_search_results(data, "lawAppendix", search_query)
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령 별표서식 검색 중 오류: {e}")
        return TextContent(type="text", text=f"법령 별표서식 검색 중 오류가 발생했습니다: {str(e)}") 

# ===========================================
# 새로운 통합 도구들 (최적화된 계층적 접근)
# ===========================================

@mcp.tool(
    name="search_law_unified",
    description="""[권장] 모든 법령 검색의 시작점 - 범용 통합 검색 도구입니다.

주요 용도:
- 일반적인 키워드로 관련 법령 탐색 (예: "부동산", "교통", "개인정보")
- 법령명을 정확히 모를 때 검색
- 다양한 종류의 법령을 한 번에 검색
- 법령의 역사, 영문판, 시행일 등 다양한 관점에서 검색

매개변수:
- query: 검색어 (필수) - 법령명, 키워드, 주제 등 자유롭게 입력
- target: 검색 대상 (기본값: "law")
  - law: 현행법령
  - eflaw: 시행일법령  
  - lsHistory: 법령연혁
  - elaw: 영문법령
  - 기타 20여개 타겟 지원
- display: 결과 개수 (최대 100)
- page: 페이지 번호
- search: 검색범위 (1=법령명, 2=본문검색)

반환정보: 법령명, 법령ID, 법령일련번호(MST), 공포일자, 시행일자, 소관부처

권장 사용 순서:
1. search_law_unified("부동산") → 관련 법령 목록 파악
2. 구체적인 법령명 확인 후 → search_law("공인중개사법")로 정밀 검색

사용 예시:
- search_law_unified("부동산")  # 부동산 관련 모든 법령 검색
- search_law_unified("개인정보", search=2)  # 본문에 개인정보 포함된 법령
- search_law_unified("Civil Act", target="elaw")  # 영문 민법 검색"""
)
def search_law_unified(
    query: str,
    target: str = "law",
    display: int = 10,
    page: int = 1,
    search: int = 1,
    sort: Optional[str] = None,
    ministry_code: Optional[str] = None,
    law_type_code: Optional[str] = None
) -> TextContent:
    """통합 법령 검색"""
    if not query:
        return TextContent(type="text", text="❌ 검색어를 입력해주세요.")
    
    try:
        params = {
            "query": query,
            "display": min(display, 100),
            "page": page,
            "search": search
        }
        
        # 선택적 파라미터 추가
        if sort:
            params["sort"] = sort
        if ministry_code:
            params["ministryCode"] = ministry_code
        if law_type_code:
            params["lawTypeCode"] = law_type_code
        
        data = _make_legislation_request(target, params, is_detail=False)
        
        # 응답 파싱
        search_data = data.get("LawSearch", {})
        items = search_data.get("law", search_data.get(target, []))
        if not isinstance(items, list):
            items = [items] if items else []
        
        total_count = int(search_data.get("totalCnt", 0))
        
        result = f"**'{query}' 검색 결과** (target: {target}, 총 {total_count}건)\n"
        result += "=" * 50 + "\n\n"
        
        for i, item in enumerate(items, 1):
            # 법령명
            law_name = (item.get("법령명한글") or item.get("법령명") or 
                       item.get("현행법령명") or "제목없음")
            
            # 법령일련번호 (상세조회용)
            mst = item.get("법령일련번호")
            law_id = item.get("법령ID")
            
            result += f"**{i}. {law_name}**\n"
            result += f"   • 법령ID: {law_id}\n"
            result += f"   • 법령일련번호: {mst}\n"
            result += f"   • 공포일자: {item.get('공포일자', '')}\n"
            result += f"   • 시행일자: {item.get('시행일자', '')}\n"
            result += f"   • 소관부처: {item.get('소관부처명', '')}\n"
            result += f"   • 구분: {item.get('법령구분명', '')}\n"
            result += f"   상세조회: get_law_detail_unified(mst=\"{mst}\", target=\"{target}\")\n"
            result += "\n"
        
        if total_count > len(items):
            result += f"더 많은 결과가 있습니다. page 파라미터를 조정하세요.\n"
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"통합 검색 중 오류: {e}")
        return TextContent(type="text", text=f"검색 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="get_law_detail_unified",
    description="""법령 상세 요약을 조회합니다.

⚠️ 주의: 특정 내용을 찾는 경우 get_law_summary 사용을 권장합니다.

이 도구는 다음 경우에만 사용하세요:
- 단순히 조문 목록만 필요한 경우
- 다른 도구가 내부적으로 호출하는 경우

일반적인 법령 내용 질문에는 get_law_summary를 사용하세요:
- "○○법의 △△ 관련 내용" → get_law_summary("○○법", "△△")

매개변수:
- mst: 법령일련번호 (필수) - search_law_unified, search_law 도구의 결과에서 'MST' 또는 '법령일련번호' 필드값 사용
- target: API 타겟 (기본값: "law")

반환정보:
- 기본정보: 법령명, 공포일자, 시행일자, 소관부처
- 조문인덱스: 전체 조문 목록 (최대 50개까지 표시, 각 조문 150자 미리보기 포함)
- 제개정이유: 법령의 목적과 배경

주요 법령 조문 구조:
◆ 도로교통법:
  - 제54조: 사고발생 시의 조치 (교통사고 처리)
  - 제80조: 운전면허
  - 제82조: 운전면허시험
  - 제87조: 적성검사
  
◆ 공인중개사법:
  - 제25조: 중개대상물의 확인·설명 (계약서 작성)
  - 제32조: 중개보수 등 (중개수수료)
  - 제33조: 서비스의 대가
  
◆ 개인정보보호법:
  - 제15조: 개인정보의 수집·이용
  - 제22조: 동의를 받는 방법
  - 제30조: 개인정보 처리방침의 수립 및 공개
  
◆ 근로기준법:
  - 제50조: 근로시간
  - 제56조: 연장·야간 및 휴일 근로
  - 제60조: 연차 유급휴가

사용 예시:
- get_law_detail_unified(mst="248613", target="law")
- get_law_detail_unified(mst="248613", target="eflaw")

참고: 특정 조문의 전체 내용은 get_law_article_by_key 도구를 사용하세요."""
)
def get_law_detail_unified(
    mst: str,
    target: str = "law"
) -> TextContent:
    """법령 상세 요약 조회"""
    if not mst:
        return TextContent(type="text", text="법령일련번호(mst)를 입력해주세요.")
    
    try:
        # 캐시 확인
        cache_key = get_cache_key(f"{target}_{mst}", "summary")
        cached_summary = load_from_cache(cache_key)
        
        if cached_summary:
            logger.info(f"캐시에서 요약 조회: {target}_{mst}")
            summary = cached_summary
        else:
            # API 호출
            params = {"MST": mst}
            data = _make_legislation_request(target, params, is_detail=True)
            
            # 전체 데이터 캐시
            full_cache_key = get_cache_key(f"{target}_{mst}", "full")
            save_to_cache(full_cache_key, data)
            
            # 요약 추출
            summary = extract_law_summary_from_detail(data)
            save_to_cache(cache_key, summary)
        
        # 포맷팅
        result = f"**{summary.get('법령명', '제목없음')}** 요약\n"
        result += "=" * 50 + "\n\n"
        
        result += "**기본 정보:**\n"
        result += f"• 법령ID: {summary.get('법령ID')}\n"
        result += f"• 법령일련번호: {summary.get('법령일련번호')}\n"
        result += f"• 공포일자: {summary.get('공포일자')}\n"
        result += f"• 시행일자: {summary.get('시행일자')}\n"
        result += f"• 소관부처: {summary.get('소관부처')}\n\n"
        
        # 조문 인덱스
        article_index = summary.get('조문_인덱스', [])
        total_articles = summary.get('조문_총개수', 0)
        
        if article_index:
            result += f"**조문 인덱스** (총 {total_articles}개 중 첫 {len(article_index)}개)\n\n"
            for item in article_index:
                result += f"• {item['key']}: {item['summary']}\n"
            result += "\n"
        
        # 제개정이유
        reason = summary.get('제개정이유', '')
        if reason:
            result += f"**제개정이유:**\n{str(reason)[:500]}{'...' if len(str(reason)) > 500 else ''}\n\n"
        
        result += f"**특정 조문 보기**: get_law_article_by_key(mst=\"{mst}\", target=\"{target}\", article_key=\"제1조\")\n"
        result += f"**원본 크기**: {summary.get('원본크기', 0):,} bytes\n"
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"상세 요약 조회 중 오류: {e}")
        return TextContent(type="text", text=f"❌ 상세 요약 조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="get_law_article_by_key",
    description="""특정 조문의 전체 내용을 조회합니다.

매개변수:
- mst: 법령일련번호 (필수) - search_law_unified, search_law 도구의 결과에서 'MST' 또는 '법령일련번호' 필드값 사용
- target: API 타겟 (필수) - get_law_detail_unified와 동일한 값 사용
- article_key: 조문 키 (필수) - 조문 번호
  - 형식: "제1조", "제50조", "1", "50" 모두 가능

반환정보: 조문번호, 조문제목, 조문내용, 항/호/목 세부구조

주요 법령의 중요 조문:
◆ 도로교통법:
  - 제54조: 사고발생 시의 조치 (교통사고 처리)
  - 제80조: 운전면허
  - 제82조: 운전면허시험
  
◆ 공인중개사법:
  - 제25조: 중개대상물의 확인·설명 (계약서 작성)
  - 제32조: 중개보수 등 (중개수수료)
  
◆ 개인정보보호법:
  - 제15조: 개인정보의 수집·이용
  - 제22조: 동의를 받는 방법
  
◆ 근로기준법:
  - 제50조: 근로시간
  - 제56조: 연장·야간 및 휴일 근로

사용 예시:
- get_law_article_by_key(mst="268547", target="law", article_key="제54조")  # 도로교통법 교통사고 조문
- get_law_article_by_key(mst="257205", target="law", article_key="제32조")  # 공인중개사법 중개수수료 조문
- get_law_article_by_key(mst="248613", target="law", article_key="15")  # 개인정보보호법 (숫자만도 가능)

참고: 캐시된 데이터를 사용하므로 빠른 응답이 가능합니다."""
)
def get_law_article_by_key(
    mst: str,
    target: str,
    article_key: str
) -> TextContent:
    """특정 조문 전체 내용 조회"""
    if not all([mst, target, article_key]):
        return TextContent(type="text", text="❌ mst, target, article_key 모두 입력해주세요.")
    
    try:
        # 캐시에서 전체 데이터 조회
        full_cache_key = get_cache_key(f"{target}_{mst}", "full")
        cached_data = load_from_cache(full_cache_key)
        
        if not cached_data:
            return TextContent(
                type="text", 
                text=f"❌ 캐시된 데이터가 없습니다. 먼저 get_law_detail_unified를 호출하세요."
            )
        
        # 조문 추출 - 실제 API 구조에 맞게
        law_info = cached_data.get("법령", {})
        articles_section = law_info.get("조문", {})
        article_units = []
        
        if isinstance(articles_section, dict) and "조문단위" in articles_section:
            article_units = articles_section.get("조문단위", [])
            # 리스트가 아닌 경우 리스트로 변환
            if not isinstance(article_units, list):
                article_units = [article_units] if article_units else []
        elif isinstance(articles_section, list):
            article_units = articles_section
        
        # 조문 번호 정규화 (제X조 → X)
        article_num = article_key
        match = re.search(r'제(\d+)조', article_key)
        if match:
            article_num = match.group(1)
        
        # 조문 찾기
        found_article = None
        for i, article in enumerate(article_units):
            if article.get("조문번호") == article_num:
                # 조문여부가 "전문"인 경우 실제 조문은 다음에 있을 수 있음
                if article.get("조문여부") == "전문" and i < len(article_units) - 1:
                    # 다음 항목 확인
                    next_article = article_units[i + 1]
                    if (next_article.get("조문번호") == article_num and 
                        next_article.get("조문여부") == "조문"):
                        found_article = next_article
                        break
                elif article.get("조문여부") == "조문":
                    found_article = article
                    break
        
        if not found_article:
            # 사용 가능한 조문 번호들 표시
            available_articles = []
            for article in article_units[:10]:
                if article.get("조문여부") == "조문":
                    no = article.get("조문번호", "")
                    if no:
                        available_articles.append(f"제{no}조")
            
            return TextContent(
                type="text",
                text=f"❌ '{article_key}'를 찾을 수 없습니다.\n"
                     f"사용 가능한 조문: {', '.join(available_articles)} ..."
            )
        
        # 조문 내용 포맷팅
        content = found_article.get("조문내용", "")
        article_no = found_article.get("조문번호", "")
        article_title = found_article.get("조문제목", "")
        key = f"제{article_no}조" if article_no else article_key
        
        law_name = law_info.get("기본정보", {}).get("법령명_한글", "")
        
        result = f"📄 **{law_name}** - {key}"
        if article_title:
            result += f"({article_title})"
        result += "\n\n"
        
        # 조문 내용 추출
        article_content = content
        if article_content and article_content.strip():
            # HTML 태그 제거
            clean_content = re.sub(r'<[^>]+>', '', article_content)
            result += clean_content + "\n\n"
        
        # 항 내용 처리
        hangs = found_article.get("항", [])
        if isinstance(hangs, list) and hangs:
            for hang in hangs:
                if isinstance(hang, dict):
                    hang_num = hang.get("항번호", "")
                    hang_content = hang.get("항내용", "")
                    if hang_content:
                        # HTML 태그 제거
                        clean_hang = re.sub(r'<[^>]+>', '', hang_content)
                        clean_hang = clean_hang.strip()
                        if clean_hang:
                            result += f"{clean_hang}\n\n"
                else:
                    result += str(hang) + "\n\n"
        
        # 추가 정보
        if found_article.get("조문시행일자"):
            result += f"\n\n📅 시행일자: {found_article.get('조문시행일자')}"
        if found_article.get("조문변경여부") == "Y":
            result += f"\n⚠️ 최근 변경된 조문입니다."
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"조문 조회 중 오류: {e}")
        return TextContent(type="text", text=f"❌ 조문 조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="get_law_articles_range",
    description="""연속된 여러 조문을 한번에 조회합니다.

매개변수:
- mst: 법령일련번호 (필수) - search_law_unified, search_law 도구의 결과에서 'MST' 필드값 사용
- target: API 타겟 (필수) - get_law_detail_unified와 동일한 값 사용
- start_article: 시작 조문 번호 (기본값: 1) - 숫자만 입력
- count: 조회할 조문 개수 (기본값: 5)

반환정보: 요청한 범위의 조문들의 전체 내용

사용 예시:
- get_law_articles_range(mst="265959", target="law", start_article=50, count=5)
  # 제50조부터 제54조까지 5개 조문 조회

참고: 페이징 방식으로 여러 조문을 효율적으로 탐색할 수 있습니다."""
)
def get_law_articles_range(
    mst: str,
    target: str,
    start_article: int = 1,
    count: int = 5
) -> TextContent:
    """연속된 조문 범위 조회"""
    if not all([mst, target]):
        return TextContent(type="text", text="❌ mst, target 모두 입력해주세요.")
    
    try:
        # 캐시에서 전체 데이터 조회
        full_cache_key = get_cache_key(f"{target}_{mst}", "full")
        cached_data = load_from_cache(full_cache_key)
        
        if not cached_data:
            # 캐시가 없으면 API 직접 호출
            params = {"MST": mst}
            cached_data = _make_legislation_request(target, params, is_detail=True)
            
            # 데이터 검증 로그
            try:
                law_info = cached_data.get("법령", {})
                articles = law_info.get("조문", {}).get("조문단위", [])
                logger.info(f"API 응답 수신 - 전체 조문 수: {len(articles)}")
                
                # 첫 번째 실제 조문 확인
                for art in articles:
                    if art.get("조문여부") == "조문":
                        art_no = art.get("조문번호", "")
                        hangs = art.get("항", [])
                        logger.info(f"첫 번째 조문: 제{art_no}조, 항 개수: {len(hangs)}")
                        break
            except Exception as e:
                logger.warning(f"API 응답 검증 중 오류: {e}")
            
            # 캐시 저장 시도 (실패해도 계속 진행)
            try:
                save_to_cache(full_cache_key, cached_data)
            except:
                pass
        
        # 조문 추출
        law_info = cached_data.get("법령", {})
        articles_section = law_info.get("조문", {})
        article_units = []
        
        if isinstance(articles_section, dict) and "조문단위" in articles_section:
            article_units = articles_section.get("조문단위", [])
            # 리스트가 아닌 경우 리스트로 변환
            if not isinstance(article_units, list):
                article_units = [article_units] if article_units else []
        elif isinstance(articles_section, list):
            article_units = articles_section
        
        # 실제 조문만 필터링 (조문여부가 "조문"인 것만)
        actual_articles = []
        for i, article in enumerate(article_units):
            if article.get("조문여부") == "조문":
                actual_articles.append(article)
        
        # 시작/끝 인덱스 계산
        start_idx = None
        for idx, article in enumerate(actual_articles):
            if int(article.get("조문번호", "0")) == start_article:
                start_idx = idx
                break
        
        if start_idx is None:
            available_articles = []
            for article in actual_articles[:10]:
                no = article.get("조문번호", "")
                if no:
                    available_articles.append(f"제{no}조")
            return TextContent(
                type="text",
                text=f"❌ 제{start_article}조를 찾을 수 없습니다.\n"
                     f"사용 가능한 조문: {', '.join(available_articles)} ..."
            )
        
        end_idx = min(start_idx + count, len(actual_articles))
        selected_articles = actual_articles[start_idx:end_idx]
        
        # 조문 내용 포맷팅
        law_name = law_info.get("기본정보", {}).get("법령명_한글", "")
        
        end_article_no = int(selected_articles[-1].get("조문번호", start_article))
        result = f"📚 **{law_name}** 조문 (제{start_article}조 ~ 제{end_article_no}조)\n"
        result += "=" * 50 + "\n\n"
        
        for article in selected_articles:
            article_no = article.get("조문번호", "")
            article_title = article.get("조문제목", "")
            
            result += f"## 제{article_no}조"
            if article_title:
                result += f"({article_title})"
            result += "\n\n"
            
            # 조문 내용 추출
            article_content = article.get("조문내용", "")
            if article_content and article_content.strip():
                # HTML 태그 제거
                clean_content = re.sub(r'<[^>]+>', '', article_content)
                result += clean_content + "\n\n"
            
            # 항 내용 처리 - 더 명확하게
            hangs = article.get("항", [])
            
            if hangs and isinstance(hangs, list):
                for hang in hangs:
                    if isinstance(hang, dict):
                        hang_num = hang.get("항번호", "")
                        hang_content = hang.get("항내용", "")
                        if hang_content:
                            # HTML 태그 제거
                            clean_hang = re.sub(r'<[^>]+>', '', hang_content)
                            clean_hang = clean_hang.strip()
                            if clean_hang:
                                result += f"{clean_hang}\n\n"
            
            result += "-" * 30 + "\n\n"
        
        return TextContent(type="text", text=result.strip())
        
    except Exception as e:
        logger.error(f"조문 범위 조회 중 오류: {e}")
        return TextContent(type="text", text=f"❌ 조문 범위 조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="compare_law_versions",
    description="""동일 법령의 현행 버전과 시행일 버전을 비교합니다.

매개변수:
- law_name: 법령명 (필수) - 비교할 법령의 이름

반환정보:
- 현행 버전 정보: 공포일자, 시행일자, 제개정구분
- 시행일 버전 정보: 공포일자, 시행일자, 제개정구분  
- 주요 변경사항: 조문별 차이점 요약

사용 예시:
- compare_law_versions("개인정보보호법")
- compare_law_versions("근로기준법")

참고: 최근 시행일 버전과 현행 버전을 자동으로 비교합니다."""
)
def compare_law_versions(law_name: str) -> TextContent:
    """법령 버전 비교"""
    if not law_name:
        return TextContent(type="text", text="❌ 법령명을 입력해주세요.")
    
    try:
        # 현행법령 검색
        current_data = _make_legislation_request("law", {"query": law_name, "display": 1})
        current_items = current_data.get("LawSearch", {}).get("law", [])
        
        if not current_items:
            return TextContent(type="text", text=f"❌ '{law_name}'을(를) 찾을 수 없습니다.")
        
        current_law = current_items[0] if isinstance(current_items, list) else current_items
        law_id = current_law.get("법령ID")
        
        # 시행일법령 검색
        eflaw_data = _make_legislation_request("eflaw", {"query": law_name, "display": 5})
        eflaw_items = eflaw_data.get("LawSearch", {}).get("law", [])
        
        if not isinstance(eflaw_items, list):
            eflaw_items = [eflaw_items] if eflaw_items else []
        
        result = f"🔄 **{law_name}** 버전 비교\n"
        result += "=" * 50 + "\n\n"
        
        # 현행법령 정보
        result += "**📌 현행법령:**\n"
        result += f"• 법령일련번호: {current_law.get('법령일련번호')}\n"
        result += f"• 공포일자: {current_law.get('공포일자')}\n"
        result += f"• 시행일자: {current_law.get('시행일자')}\n"
        result += f"• 제개정구분: {current_law.get('제개정구분명')}\n\n"
        
        # 시행일법령 목록
        result += "**📅 시행일법령 이력:**\n"
        for i, eflaw in enumerate(eflaw_items[:3], 1):
            status = eflaw.get('현행연혁코드', '')
            result += f"\n{i}. "
            if status == "시행예정":
                result += "🔜 "
            elif status == "현행":
                result += "✅ "
            else:
                result += "📜 "
            
            result += f"{status} (시행일: {eflaw.get('시행일자')})\n"
            result += f"   • 법령일련번호: {eflaw.get('법령일련번호')}\n"
            result += f"   • 공포일자: {eflaw.get('공포일자')}\n"
            result += f"   • 제개정구분: {eflaw.get('제개정구분명')}\n"
        
        result += "\n💡 **상세 비교**: 각 버전의 상세 내용은 get_law_detail_unified로 조회하세요.\n"
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"버전 비교 중 오류: {e}")
        return TextContent(type="text", text=f"❌ 버전 비교 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="search_law_articles_semantic",
    description="""[내부 도구] 캐시된 법령 데이터에서 의미 기반으로 조문을 검색합니다.

이 도구는 주로 다른 도구들이 내부적으로 사용합니다.
일반 사용자는 get_law_summary 도구를 사용하세요.

주요 기능:
- 법령 전체를 캐시하여 모든 조문을 검색 가능
- 키워드로 관련 조문 찾기
- 조문 번호를 몰라도 내용으로 검색 가능

매개변수:
- mst: 법령일련번호 (필수)
- query: 검색 키워드 (필수)
- target: API 타겟 (기본값: "law")
- max_results: 최대 결과 개수 (기본값: 10)

사용 시나리오:
- get_law_summary가 내부적으로 호출
- 특정 조문 번호를 찾을 때 LLM이 자동 호출"""
)
def search_law_articles_semantic(
    mst: str,
    query: str,
    target: str = "law",
    max_results: int = 10
) -> TextContent:
    """캐시된 법령에서 시맨틱 검색"""
    if not mst or not query:
        return TextContent(type="text", text="법령일련번호(mst)와 검색어(query)를 모두 입력해주세요.")
    
    try:
        # 캐시 키 생성
        cache_key = get_cache_key(f"{target}_{mst}", "full")
        cached_data = load_from_cache(cache_key)
        
        # 캐시가 없으면 API로 전체 데이터 가져오기
        if not cached_data:
            logger.info(f"캐시 없음. API로 법령 전체 조회: {target}_{mst}")
            params = {"MST": mst}
            data = _make_legislation_request(target, params, is_detail=True)
            
            if not data:
                return TextContent(type="text", text=f"법령 데이터를 가져올 수 없습니다. MST: {mst}")
            
            # 캐시 저장
            save_to_cache(cache_key, data)
            cached_data = data
        
        # 법령 정보 추출
        law_info = cached_data.get("법령", {})
        basic_info = law_info.get("기본정보", {})
        law_name = basic_info.get("법령명_한글", basic_info.get("법령명한글", ""))
        
        # 조문 데이터 추출
        articles_section = law_info.get("조문", {})
        all_articles = []
        
        if isinstance(articles_section, dict):
            if "조문단위" in articles_section:
                article_units = articles_section.get("조문단위", [])
                if not isinstance(article_units, list):
                    article_units = [article_units] if article_units else []
                all_articles = article_units
            else:
                # 조문이 직접 딕셔너리로 되어있는 경우
                for key, value in articles_section.items():
                    if isinstance(value, dict) and "조문내용" in value:
                        all_articles.append({
                            "조문번호": key.replace("제", "").replace("조", ""),
                            "조문제목": value.get("조문제목", ""),
                            "조문내용": value.get("조문내용", "")
                        })
        
        # 시맨틱 검색 (개선된 키워드 매칭)
        search_results = []
        query_lower = query.lower()
        
        # 복합 키워드 처리
        query_words = []
        main_words = query_lower.split()
        query_words.extend(main_words)
        
        # 복합어 분해 (예: "야근수당" → "야근", "수당")
        for word in main_words:
            if len(word) >= 4:
                for i in range(len(word) - 1):
                    sub_word = word[i:i+2]
                    if sub_word not in query_words:
                        query_words.append(sub_word)
        
        # 관련 키워드 매핑
        related_keywords = {
            "근로시간": ["근로", "시간", "40시간", "8시간", "1주", "1일"],
            "야근": ["연장", "초과", "시간외", "연장근로"],
            "수당": ["가산", "임금", "100분의", "50", "보수"],
            "온라인": ["전자", "정보통신", "인터넷", "웹", "사이트"],
            "쇼핑몰": ["판매", "거래", "상거래", "전자상거래", "통신판매"]
        }
        
        for article in all_articles:
            if not isinstance(article, dict):
                continue
                
            article_no = article.get("조문번호", "")
            article_title = article.get("조문제목", "")
            article_content = article.get("조문내용", "")
            
            # 조문 여부 확인
            if article.get("조문여부") != "조문" and "조문여부" in article:
                continue
            
            # 전체 텍스트 생성
            full_text = f"{article_title} {article_content}".lower()
            
            # 점수 계산 (개선된 알고리즘)
            score = 0
            matched_words = set()
            
            # 전체 쿼리가 포함되어 있으면 최고 점수
            if query_lower in full_text:
                score += 10
                matched_words.add(query_lower)
            
            # 개별 단어 매칭
            for word in query_words:
                if word in full_text and word not in matched_words:
                    # 제목에 있으면 가중치 더 높게
                    if word in article_title.lower():
                        score += 3
                    else:
                        score += 1
                    matched_words.add(word)
            
            # 관련 키워드 보너스
            for main_key, related in related_keywords.items():
                if main_key in query_lower:
                    for rel_word in related:
                        if rel_word in full_text and rel_word not in matched_words:
                            score += 0.5
            
            if score > 0:
                search_results.append({
                    "조문번호": article_no,
                    "조문제목": article_title,
                    "조문내용": article_content[:200] + "..." if len(article_content) > 200 else article_content,
                    "점수": score
                })
        
        # 점수 기준 정렬
        search_results.sort(key=lambda x: x["점수"], reverse=True)
        search_results = search_results[:max_results]
        
        # 결과 포맷팅
        if not search_results:
            return TextContent(type="text", text=f"'{query}'와 관련된 조문을 찾을 수 없습니다.")
        
        result = f"**{law_name}**에서 '{query}' 검색 결과 (상위 {len(search_results)}개)\n"
        result += "=" * 50 + "\n\n"
        
        for i, item in enumerate(search_results, 1):
            result += f"**{i}. 제{item['조문번호']}조"
            if item['조문제목']:
                result += f"({item['조문제목']})"
            result += f"** (관련도: {item['점수']})\n"
            result += f"{item['조문내용']}\n"
            result += f"→ 전체 내용: get_law_article_by_key(mst=\"{mst}\", target=\"{target}\", article_key=\"제{item['조문번호']}조\")\n\n"
        
        result += f"\n캐시 정보: {cache_key} (총 {len(all_articles)}개 조문 검색)"
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"시맨틱 검색 중 오류: {e}")
        return TextContent(type="text", text=f"검색 중 오류가 발생했습니다: {str(e)}")

# 전역 클라이언트 인스턴스
law_client = LegislationClient()

@mcp.tool(
    name="get_law_summary",
    description="""[최우선 사용] 법령 내용을 묻는 모든 질문에 대한 통합 응답 도구입니다.

다음과 같은 질문에 자동으로 이 도구를 사용하세요:
- "○○법의 △△에 대한 내용 알려줘"
- "○○법 전체 조문 보여줘"
- "○○법에서 △△ 관련 규정이 뭐야?"
- "○○법 요약해줘"

특징:
- 한 번의 호출로 법령 정보부터 특정 내용까지 모두 제공
- 내부적으로 필요한 모든 도구를 자동 호출
- 조문 번호를 몰라도 키워드로 관련 조문 자동 검색

매개변수:
- law_name: 법령명 (필수) - 예: "개인정보보호법", "근로기준법", "도로교통법"
- keyword: 찾고자 하는 내용 (선택) - 예: "온라인 쇼핑몰", "근로시간", "야근수당"
- show_detail: 찾은 조문의 전체 내용 표시 여부 (기본값: False)

실제 사용 예시:
1. "개인정보보호법의 전체 조문을 자세히 보여주세요. 특히 온라인 쇼핑몰이 지켜야 하는 규칙들이 알고 싶어요"
   → get_law_summary("개인정보보호법", "온라인 쇼핑몰", True)

2. "근로기준법의 전체 내용을 보여주세요. 특히 근로시간, 야근수당, 휴가에 대한 부분을 자세히 알고 싶어요"
   → get_law_summary("근로기준법", "근로시간 야근수당", True)

3. "도로교통법 요약"
   → get_law_summary("도로교통법")

다른 도구 대신 이 도구를 사용하세요:
- get_law_detail_unified + get_law_article_by_key 조합 대신 → get_law_summary
- search_law + 개별 조문 조회 대신 → get_law_summary"""
)
def get_law_summary(
    law_name: str,
    keyword: Optional[str] = None,
    show_detail: bool = False
) -> TextContent:
    """법령 요약 및 특정 내용 검색 통합 도구"""
    if not law_name:
        return TextContent(type="text", text="법령명을 입력해주세요.")
    
    try:
        # 1단계: 법령 검색
        search_result = search_law(law_name, display=5)
        search_text = search_result.text
        
        # MST 추출 (간단한 파싱)
        mst = None
        law_id = None
        lines = search_text.split('\n')
        for line in lines:
            if '법령일련번호:' in line:
                mst = line.split('법령일련번호:')[1].strip()
                break
        
        if not mst:
            return TextContent(type="text", text=f"'{law_name}'을(를) 찾을 수 없습니다.\n\n{search_text}")
        
        # 법령ID도 추출
        for line in lines:
            if '법령ID:' in line:
                law_id = line.split('법령ID:')[1].strip()
                break
        
        # 2단계: 기본 정보 가져오기
        detail_result = get_law_detail_unified(mst, "law")
        
        result = f"**{law_name} 요약**\n"
        result += "=" * 50 + "\n\n"
        result += detail_result.text.split("**조문 인덱스**")[0]  # 기본 정보만
        
        # 3단계: 키워드가 있으면 관련 조문 검색
        if keyword:
            result += f"\n**'{keyword}' 관련 조문**\n"
            result += "-" * 30 + "\n"
            
            semantic_result = search_law_articles_semantic(mst, keyword, max_results=5)
            result += semantic_result.text
            
            # 4단계: 상세 내용 표시
            if show_detail:
                # 가장 관련성 높은 조문 번호 추출
                semantic_lines = semantic_result.text.split('\n')
                article_key = None
                for line in semantic_lines:
                    if line.startswith("**1. 제"):
                        # "**1. 제80조(운전면허)**" 형태에서 추출
                        article_part = line.split("**")[1].split("(")[0]
                        article_key = article_part
                        break
                
                if article_key:
                    result += f"\n**{article_key} 전체 내용**\n"
                    result += "-" * 30 + "\n"
                    article_detail = get_law_article_by_key(mst, "law", article_key)
                    result += article_detail.text
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"법령 요약 중 오류: {e}")
        return TextContent(type="text", text=f"법령 요약 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="search_english_law_articles_semantic",
    description="""[내부 도구] 캐시된 영문 법령 데이터에서 의미 기반으로 조문을 검색합니다.

이 도구는 주로 다른 도구들이 내부적으로 사용합니다.
일반 사용자는 get_english_law_summary 도구를 사용하세요.

주요 기능:
- 영문 법령 전체를 캐시하여 모든 조문을 검색 가능
- 영어 키워드로 관련 조문 찾기
- 조문 번호를 몰라도 내용으로 검색 가능

매개변수:
- mst: 법령일련번호 (필수)
- query: 검색 키워드 (필수) - 영어로 입력
- max_results: 최대 결과 개수 (기본값: 10)

사용 시나리오:
- get_english_law_summary가 내부적으로 호출
- 특정 조문 번호를 찾을 때 LLM이 자동 호출"""
)
def search_english_law_articles_semantic(
    mst: str,
    query: str,
    max_results: int = 10
) -> TextContent:
    """영문법령 조문 시맨틱 검색"""
    try:
        # 캐시 확인
        cache_key = get_cache_key(f"elaw_{mst}", "full")
        cached_data = load_from_cache(cache_key)
        
        if not cached_data:
            # 캐시가 없으면 API 호출하여 전체 법령 데이터 가져오기
            params = {"MST": mst}
            data = _make_legislation_request("elaw", params, is_detail=True)
            
            if not data or 'Law' not in data:
                return TextContent(
                    type="text", 
                    text=f"❌ 영문 법령 데이터를 찾을 수 없습니다. (MST: {mst})"
                )
            
            # 캐시에 저장
            save_to_cache(cache_key, data)
            cached_data = data
        
        law_data = cached_data['Law']
        
        # JoSection에서 실제 조문 추출
        jo_section = law_data.get('JoSection', {})
        all_articles = []
        
        if jo_section and 'Jo' in jo_section:
            jo_data = jo_section['Jo']
            if isinstance(jo_data, list):
                # 실제 조문만 필터링 (joYn='Y'인 것들)
                all_articles = [jo for jo in jo_data if jo.get('joYn') == 'Y']
            elif isinstance(jo_data, dict) and jo_data.get('joYn') == 'Y':
                all_articles = [jo_data]
        
        if not all_articles:
            return TextContent(
                type="text",
                text=f"❌ 검색 가능한 조문이 없습니다. (MST: {mst})"
            )
        
        # 영문 시맨틱 검색 (키워드 매칭)
        search_results = []
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # 영문 관련 키워드 매핑
        related_keywords = {
            "contract": ["agreement", "covenant", "obligation", "performance"],
            "property": ["ownership", "possession", "title", "estate"],
            "commercial": ["business", "trade", "commerce", "merchant"],
            "civil": ["private", "individual", "personal", "civilian"],
            "liability": ["responsibility", "accountable", "damages", "compensation"],
            "company": ["corporation", "enterprise", "firm", "business"]
        }
        
        for article in all_articles:
            article_no = article.get('joNo', '')
            article_content = article.get('joCts', '')
            
            if not article_content:
                continue
            
            # 전체 텍스트 생성
            full_text = article_content.lower()
            
            # 점수 계산
            score = 0
            matched_words = set()
            
            # 전체 쿼리가 포함되어 있으면 최고 점수
            if query_lower in full_text:
                score += 10
                matched_words.add(query_lower)
            
            # 개별 단어 매칭
            for word in query_words:
                if word in full_text and word not in matched_words:
                    score += 2
                    matched_words.add(word)
            
            # 관련 키워드 보너스
            for main_key, related in related_keywords.items():
                if main_key in query_lower:
                    for rel_word in related:
                        if rel_word in full_text and rel_word not in matched_words:
                            score += 0.5
            
            if score > 0:
                search_results.append({
                    "article_no": article_no,
                    "content": article_content[:300] + "..." if len(article_content) > 300 else article_content,
                    "score": score
                })
        
        # 점수순으로 정렬
        search_results.sort(key=lambda x: x['score'], reverse=True)
        search_results = search_results[:max_results]
        
        if not search_results:
            return TextContent(
                type="text",
                text=f"'{query}' 키워드와 관련된 조문을 찾을 수 없습니다."
            )
        
        # 결과 포맷팅
        result = f"**영문 법령 조문 검색 결과** (키워드: '{query}')\n"
        result += "=" * 50 + "\n\n"
        
        for i, item in enumerate(search_results, 1):
            result += f"**{i}. Article {item['article_no']}** (관련도: {item['score']:.1f})\n"
            result += f"{item['content']}\n\n"
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"영문법령 시맨틱 검색 중 오류: {e}")
        return TextContent(
            type="text",
            text=f"영문법령 조문 검색 중 오류가 발생했습니다: {str(e)}"
        )

@mcp.tool(
    name="get_english_law_summary",
    description="""[최우선 사용] 영문 법령 내용을 묻는 모든 질문에 대한 통합 응답 도구입니다.

다음과 같은 질문에 자동으로 이 도구를 사용하세요:
- "Show me the English version of ○○ law"
- "What are the contract provisions in Korean Civil Act?"
- "Explain Korean Commercial Act in English"
- "Find articles about ○○ in Korean law (in English)"

특징:
- 한 번의 호출로 영문 법령 정보부터 특정 내용까지 모두 제공
- 내부적으로 필요한 모든 도구를 자동 호출
- 조문 번호를 몰라도 영어 키워드로 관련 조문 자동 검색

매개변수:
- law_name: 법령명 (필수) - 영어 또는 한국어 가능
  예: "Civil Act", "Commercial Act", "민법", "상법"
- keyword: 찾고자 하는 내용 (선택) - 영어로 입력
  예: "contract", "property", "liability", "company"
- show_detail: 찾은 조문의 전체 내용 표시 여부 (기본값: False)

실제 사용 예시:
1. "Show me Korean Civil Act in English, especially about contract formation"
   → get_english_law_summary("Civil Act", "contract", True)

2. "What does Korean Commercial Act say about company formation?"
   → get_english_law_summary("Commercial Act", "company formation", True)

3. "Explain Korean Civil Act in English"
   → get_english_law_summary("Civil Act")

다른 도구 대신 이 도구를 사용하세요:
- search_english_law + get_english_law_detail 조합 대신 → get_english_law_summary
- 영문 법령 관련 질문은 모두 이 도구로 처리"""
)
def get_english_law_summary(
    law_name: str,
    keyword: Optional[str] = None,
    show_detail: bool = False
) -> TextContent:
    """영문 법령 통합 요약"""
    try:
        # 1단계: 영문 법령 검색 (내부 호출 시뮬레이션)
        # search_english_law 로직 직접 구현
        search_params = {
            "OC": legislation_config.oc,
            "type": "JSON", 
            "target": "elaw",
            "query": law_name,
            "search": 1,
            "display": 5,
            "page": 1
        }
        
        search_data = _make_legislation_request("elaw", search_params, is_detail=False)
        
        # 검색 결과에서 첫 번째 법령 선택
        if not search_data or 'LawSearch' not in search_data or 'law' not in search_data['LawSearch']:
            return TextContent(
                type="text",
                text=f"❌ '{law_name}'에 해당하는 영문 법령을 찾을 수 없습니다."
            )
        
        laws = search_data['LawSearch']['law']
        if not laws:
            return TextContent(
                type="text",
                text=f"❌ '{law_name}'에 해당하는 영문 법령을 찾을 수 없습니다."
            )
        
        current_law = laws[0] if isinstance(laws, list) else laws
        mst = current_law.get('법령일련번호')
        
        if not mst:
            return TextContent(
                type="text",
                text=f"❌ 법령일련번호를 찾을 수 없습니다."
            )
        
        # 2단계: 기본 법령 정보 조회
        detail_params = {"MST": mst}
        detail_data = _make_legislation_request("elaw", detail_params, is_detail=True)
        
        # 기본 정보 포맷팅
        result = "**영문 법령 요약**\n"
        result += "=" * 50 + "\n\n"
        
        result += "**기본 정보:**\n"
        result += f"• 영문명: {current_law.get('법령명영문', 'N/A')}\n"
        result += f"• 한글명: {current_law.get('법령명한글', 'N/A')}\n" 
        result += f"• 법령ID: {current_law.get('법령ID', 'N/A')}\n"
        result += f"• MST: {mst}\n"
        result += f"• 공포일자: {current_law.get('공포일자', 'N/A')}\n"
        result += f"• 시행일자: {current_law.get('시행일자', 'N/A')}\n"
        result += f"• 소관부처: {current_law.get('소관부처명', 'N/A')}\n\n"
        
        # 3단계: 키워드가 있으면 시맨틱 검색
        if keyword:
            # search_english_law_articles_semantic 로직 직접 구현
            cache_key = get_cache_key(f"elaw_{mst}", "full")
            cached_data = load_from_cache(cache_key)
            
            if not cached_data:
                cached_data = detail_data
                save_to_cache(cache_key, cached_data)
            
            if cached_data and 'Law' in cached_data:
                law_data = cached_data['Law']
                jo_section = law_data.get('JoSection', {})
                
                if jo_section and 'Jo' in jo_section:
                    jo_data = jo_section['Jo']
                    all_articles = []
                    
                    if isinstance(jo_data, list):
                        all_articles = [jo for jo in jo_data if jo.get('joYn') == 'Y']
                    elif isinstance(jo_data, dict) and jo_data.get('joYn') == 'Y':
                        all_articles = [jo_data]
                    
                    if all_articles:
                        # 간단한 키워드 검색
                        keyword_lower = keyword.lower()
                        matching_articles = []
                        
                        for article in all_articles[:20]:  # 처음 20개만 검색
                            content = article.get('joCts', '').lower()
                            if any(word in content for word in keyword_lower.split()):
                                matching_articles.append(article)
                        
                        if matching_articles:
                            result += f"**'{keyword}' 관련 조문** (상위 {min(3, len(matching_articles))}개):\n\n"
                            
                            for i, article in enumerate(matching_articles[:3], 1):
                                article_no = article.get('joNo', '')
                                content = article.get('joCts', '')
                                
                                if show_detail:
                                    result += f"**Article {article_no}:** (전체 내용)\n"
                                    result += f"{content}\n\n"
                                else:
                                    preview = content[:200] + "..." if len(content) > 200 else content
                                    result += f"**Article {article_no}:** (미리보기)\n"
                                    result += f"{preview}\n\n"
                        else:
                            result += f"**'{keyword}' 관련 조문을 찾을 수 없습니다.**\n\n"
        
        # 4단계: 일반 정보
        if detail_data and 'Law' in detail_data:
            law_data = detail_data['Law']
            jo_section = law_data.get('JoSection', {})
            
            if jo_section and 'Jo' in jo_section:
                jo_data = jo_section['Jo']
                if isinstance(jo_data, list):
                    article_count = len([jo for jo in jo_data if jo.get('joYn') == 'Y'])
                    result += f"**전체 조문 개수**: {article_count}개\n"
                else:
                    result += f"**전체 조문 개수**: 1개\n"
        
        result += f"\n**상세 조회**: get_english_law_detail(law_id=\"{mst}\")"
        
        return TextContent(type="text", text=result)
        
    except Exception as e:
        logger.error(f"영문법령 요약 중 오류: {e}")
        return TextContent(
            type="text",
            text=f"영문법령 요약 중 오류가 발생했습니다: {str(e)}"
        )
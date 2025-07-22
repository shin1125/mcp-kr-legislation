"""
법령 종합 정보 조회/분석 도구

예시 사용법:

from mcp_kr_legislation.tools.legislation_tools import search_legislation, search_by_law_name

result = search_legislation(keyword="근로기준법")
detail = search_by_law_name(law_name="자동차관리법")
"""

import logging
import json
from pathlib import Path
from typing import Any, Optional
import os

from ..server import mcp, ctx
from mcp.types import TextContent
from mcp_kr_legislation.utils.data_processor import get_cache_dir

logger = logging.getLogger(__name__)

def _save_legislation_data(data: dict, filename: str, target_dir: Optional[str] = None) -> str:
    """
    법령 데이터를 JSON 파일로 저장하고 경로 반환
    """
    if target_dir is None:
        target_dir = get_cache_dir()
    
    cache_dir = Path(target_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = cache_dir / f"{filename}.json"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return str(file_path)

@mcp.tool()
def search_legislation(
    query: Optional[str] = None,
    search_type: int = 1,
    display: int = 20,
    page: int = 1,
    sort: str = "lasc"
) -> TextContent:
    """
    법령을 검색합니다.
    
    Args:
        query (str, optional): 검색할 법령명 또는 키워드
        search_type (int): 검색범위 (1: 법령명, 2: 본문검색)
        display (int): 검색 결과 개수 (기본 20, 최대 100)
        page (int): 검색 결과 페이지
        sort (str): 정렬옵션 (lasc: 법령오름차순, ldes: 법령내림차순 등)
    
    Returns:
        TextContent: 검색 결과가 저장된 JSON 파일 경로
    """
    try:
        legislation_api = ctx.legislation_api
        result_json = legislation_api.search_legislation(
            query=query,
            search=search_type,
            display=display,
            page=page,
            sort=sort
        )
        result_data = json.loads(result_json)
        
        # 결과를 파일로 저장
        search_term = query or "all"
        filename = f"legislation_search_{search_term}_{search_type}_{page}"
        file_path = _save_legislation_data(result_data, filename)
        
        return TextContent(
            type="text",
            text=file_path
        )
    except Exception as e:
        logger.error(f"법령 검색 중 오류 발생: {e}")
        return TextContent(
            type="text", 
            text=f"법령 검색 중 오류가 발생했습니다: {str(e)}"
        )

@mcp.tool()
def search_by_law_name(law_name: str, display: int = 20, page: int = 1) -> TextContent:
    """
    법령명으로 정확히 검색합니다.
    
    Args:
        law_name (str): 검색할 법령명
        display (int): 검색 결과 개수 (기본 20, 최대 100)
        page (int): 검색 결과 페이지
    
    Returns:
        TextContent: 검색 결과가 저장된 JSON 파일 경로
    """
    try:
        legislation_api = ctx.legislation_api
        result_json = legislation_api.search_by_law_name(
            law_name=law_name,
            display=display,
            page=page
        )
        result_data = json.loads(result_json)
        
        # 결과를 파일로 저장
        filename = f"law_name_search_{law_name}_{page}"
        file_path = _save_legislation_data(result_data, filename)
        
        return TextContent(
            type="text",
            text=file_path
        )
    except Exception as e:
        logger.error(f"법령명 검색 중 오류 발생: {e}")
        return TextContent(
            type="text", 
            text=f"법령명 검색 중 오류가 발생했습니다: {str(e)}"
        )

@mcp.tool()
def search_by_content(keyword: str, display: int = 20, page: int = 1) -> TextContent:
    """
    법령 본문 내용으로 검색합니다.
    
    Args:
        keyword (str): 검색할 키워드
        display (int): 검색 결과 개수 (기본 20, 최대 100)
        page (int): 검색 결과 페이지
    
    Returns:
        TextContent: 검색 결과가 저장된 JSON 파일 경로
    """
    try:
        legislation_api = ctx.legislation_api
        result_json = legislation_api.search_by_content(
            keyword=keyword,
            display=display,
            page=page
        )
        result_data = json.loads(result_json)
        
        # 결과를 파일로 저장
        filename = f"content_search_{keyword}_{page}"
        file_path = _save_legislation_data(result_data, filename)
        
        return TextContent(
            type="text",
            text=file_path
        )
    except Exception as e:
        logger.error(f"본문 검색 중 오류 발생: {e}")
        return TextContent(
            type="text", 
            text=f"본문 검색 중 오류가 발생했습니다: {str(e)}"
        )

@mcp.tool()
def search_by_ministry(org_code: str, display: int = 20, page: int = 1) -> TextContent:
    """
    소관부처별로 법령을 검색합니다.
    
    Args:
        org_code (str): 소관부처 코드
        display (int): 검색 결과 개수 (기본 20, 최대 100)
        page (int): 검색 결과 페이지
    
    Returns:
        TextContent: 검색 결과가 저장된 JSON 파일 경로
    """
    try:
        legislation_api = ctx.legislation_api
        result_json = legislation_api.search_by_ministry(
            org_code=org_code,
            display=display,
            page=page
        )
        result_data = json.loads(result_json)
        
        # 결과를 파일로 저장
        filename = f"ministry_search_{org_code}_{page}"
        file_path = _save_legislation_data(result_data, filename)
        
        return TextContent(
            type="text",
            text=file_path
        )
    except Exception as e:
        logger.error(f"소관부처별 검색 중 오류 발생: {e}")
        return TextContent(
            type="text", 
            text=f"소관부처별 검색 중 오류가 발생했습니다: {str(e)}"
        )

@mcp.tool()
def get_recent_laws(days: int = 30, display: int = 20) -> TextContent:
    """
    최근 공포된 법령을 조회합니다.
    
    Args:
        days (int): 최근 며칠간의 법령 (기본 30일)
        display (int): 검색 결과 개수 (기본 20, 최대 100)
    
    Returns:
        TextContent: 검색 결과가 저장된 JSON 파일 경로
    """
    try:
        legislation_api = ctx.legislation_api
        result_json = legislation_api.get_recent_laws(
            days=days,
            display=display
        )
        result_data = json.loads(result_json)
        
        # 결과를 파일로 저장
        filename = f"recent_laws_{days}days"
        file_path = _save_legislation_data(result_data, filename)
        
        return TextContent(
            type="text",
            text=file_path
        )
    except Exception as e:
        logger.error(f"최근 법령 조회 중 오류 발생: {e}")
        return TextContent(
            type="text", 
            text=f"최근 법령 조회 중 오류가 발생했습니다: {str(e)}"
        )

@mcp.tool()
def search_by_date_range(
    start_date: str, 
    end_date: str, 
    date_type: str = "anc",
    display: int = 20,
    page: int = 1
) -> TextContent:
    """
    날짜 범위로 법령을 검색합니다.
    
    Args:
        start_date (str): 시작일자 (YYYYMMDD)
        end_date (str): 종료일자 (YYYYMMDD)
        date_type (str): 날짜 유형 ('anc': 공포일자, 'ef': 시행일자)
        display (int): 검색 결과 개수 (기본 20, 최대 100)
        page (int): 검색 결과 페이지
    
    Returns:
        TextContent: 검색 결과가 저장된 JSON 파일 경로
    """
    try:
        legislation_api = ctx.legislation_api
        result_json = legislation_api.search_by_date_range(
            start_date=start_date,
            end_date=end_date,
            date_type=date_type,
            display=display,
            page=page
        )
        result_data = json.loads(result_json)
        
        # 결과를 파일로 저장
        filename = f"date_range_search_{start_date}_{end_date}_{date_type}_{page}"
        file_path = _save_legislation_data(result_data, filename)
        
        return TextContent(
            type="text",
            text=file_path
        )
    except Exception as e:
        logger.error(f"날짜 범위 검색 중 오류 발생: {e}")
        return TextContent(
            type="text", 
            text=f"날짜 범위 검색 중 오류가 발생했습니다: {str(e)}"
        ) 
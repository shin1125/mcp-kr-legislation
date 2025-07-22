"""
법령 종합 정보 분석 도구

예시 사용법:

from mcp_kr_legislation.tools.analysis_tools import analyze_legislation, get_legislation_history

analysis = analyze_legislation(file_path="/path/to/legislation.json")
history = get_legislation_history(law_name="근로기준법")
"""

import logging
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import os

from ..server import mcp, ctx
from mcp.types import TextContent
from mcp_kr_legislation.utils.data_processor import get_cache_dir

logger = logging.getLogger(__name__)

def _save_analysis_data(data: dict, filename: str, target_dir: Optional[str] = None) -> str:
    """
    분석 결과 데이터를 JSON 파일로 저장하고 경로 반환
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
def analyze_legislation(file_path: str) -> TextContent:
    """
    법령 데이터 파일을 분석하여 요약 정보를 제공합니다.
    
    Args:
        file_path (str): 분석할 법령 데이터 JSON 파일 경로
    
    Returns:
        TextContent: 분석 결과가 저장된 JSON 파일 경로
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            legislation_data = json.load(f)
        
        # 분석 수행
        analysis_result = {
            "file_path": file_path,
            "analysis_summary": {
                "total_items": len(legislation_data.get('items', [])),
                "search_keyword": legislation_data.get('search_params', {}).get('keyword', ''),
                "key_legislation": []
            },
            "detailed_analysis": {
                "legislation_types": {},
                "recent_amendments": [],
                "related_areas": []
            }
        }
        
        # 상세 분석 (예시 구현)
        items = legislation_data.get('items', [])
        for item in items[:5]:  # 상위 5개만 분석
            analysis_result["analysis_summary"]["key_legislation"].append({
                "name": item.get("law_name", ""),
                "type": item.get("law_type", ""),
                "enact_date": item.get("enact_date", ""),
                "last_modified": item.get("last_modified", "")
            })
        
        # 결과 저장
        filename = f"legislation_analysis_{os.path.basename(file_path)}"
        result_path = _save_analysis_data(analysis_result, filename)
        
        return TextContent(
            type="text",
            text=result_path
        )
    except Exception as e:
        logger.error(f"법령 분석 중 오류 발생: {e}")
        return TextContent(
            type="text",
            text=f"법령 분석 중 오류가 발생했습니다: {str(e)}"
        )

@mcp.tool()
def get_legislation_history(law_name: str) -> TextContent:
    """
    법령의 개정 이력을 조회합니다.
    
    Args:
        law_name (str): 법령명
    
    Returns:
        TextContent: 개정 이력이 저장된 JSON 파일 경로
    """
    try:
        # 예시 개정 이력 데이터 (실제 구현에서는 API 호출)
        history_data = {
            "law_name": law_name,
            "amendment_history": [
                {
                    "amendment_date": "2023-12-31",
                    "amendment_type": "일부개정",
                    "main_changes": "근로시간 단축 관련 규정 신설",
                    "effective_date": "2024-01-01"
                },
                {
                    "amendment_date": "2022-05-01",
                    "amendment_type": "일부개정", 
                    "main_changes": "최저임금 관련 조항 개정",
                    "effective_date": "2022-07-01"
                }
            ],
            "total_amendments": 2
        }
        
        # 결과 저장
        filename = f"legislation_history_{law_name}"
        result_path = _save_analysis_data(history_data, filename)
        
        return TextContent(
            type="text",
            text=result_path
        )
    except Exception as e:
        logger.error(f"법령 개정 이력 조회 중 오류 발생: {e}")
        return TextContent(
            type="text",
            text=f"법령 개정 이력 조회 중 오류가 발생했습니다: {str(e)}"
        )
from typing import Dict, Any, Optional, List
from mcp_kr_legislation.apis.client import LegislationClient
from pathlib import Path
import os
import json
from dotenv import load_dotenv

load_dotenv()

class LegislationAPI:
    """법령 종합 정보 API"""
    def __init__(self, client: LegislationClient):
        self.client = client

    def search_legislation(
        self, 
        query: Optional[str] = None,
        search: int = 1,  # 1: 법령명, 2: 본문검색
        display: int = 20,  # 검색 결과 개수 (max=100)
        page: int = 1,  # 페이지 번호
        sort: str = "lasc",  # 정렬옵션
        **kwargs
    ) -> str:
        """
        법령 검색 API
        Args:
            query (str, optional): 검색할 법령명 또는 키워드
            search (int): 검색범위 (1: 법령명, 2: 본문검색)
            display (int): 검색 결과 개수 (기본 20, 최대 100)
            page (int): 검색 결과 페이지
            sort (str): 정렬옵션 (lasc: 법령오름차순, ldes: 법령내림차순 등)
            **kwargs: 기타 검색 옵션들
        Returns:
            str: 검색 결과가 포함된 JSON 문자열
        """
        params = {
            "search": search,
            "display": min(display, 100),  # 최대 100개 제한
            "page": page,
            "sort": sort
        }
        
        if query:
            params["query"] = query
            
        # 추가 검색 옵션들
        optional_params = [
            'date', 'efYd', 'ancYd', 'ancNo', 'rrClsCd', 
            'nb', 'org', 'knd', 'lsChapNo', 'gana', 'popYn'
        ]
        
        for param in optional_params:
            if param in kwargs and kwargs[param] is not None:
                params[param] = kwargs[param]
        
        try:
            response = self.client.get(params)
            
            if "error" in response:
                raise Exception(f"API 오류: {response['error']}")
            
            return json.dumps(response, ensure_ascii=False, indent=2)
                
        except Exception as e:
            raise Exception(f"법령 검색 중 오류가 발생했습니다: {str(e)}")

    def search_by_law_name(self, law_name: str, **kwargs) -> str:
        """
        법령명으로 검색
        """
        return self.search_legislation(query=law_name, search=1, **kwargs)

    def search_by_content(self, keyword: str, **kwargs) -> str:
        """
        본문 내용으로 검색
        """
        return self.search_legislation(query=keyword, search=2, **kwargs)

    def search_by_ministry(self, org_code: str, **kwargs) -> str:
        """
        소관부처별 검색
        """
        return self.search_legislation(org=org_code, **kwargs)

    def search_by_law_type(self, law_type_code: str, **kwargs) -> str:
        """
        법령종류별 검색
        """
        return self.search_legislation(knd=law_type_code, **kwargs)

    def search_by_date_range(self, start_date: str, end_date: str, date_type: str = "anc", **kwargs) -> str:
        """
        날짜 범위로 검색
        Args:
            start_date (str): 시작일자 (YYYYMMDD)
            end_date (str): 종료일자 (YYYYMMDD)
            date_type (str): 날짜 유형 ('anc': 공포일자, 'ef': 시행일자)
        """
        date_range = f"{start_date}~{end_date}"
        if date_type == "anc":
            return self.search_legislation(ancYd=date_range, **kwargs)
        elif date_type == "ef":
            return self.search_legislation(efYd=date_range, **kwargs)
        else:
            raise ValueError("date_type은 'anc' 또는 'ef'여야 합니다.")

    def get_recent_laws(self, days: int = 30, **kwargs) -> str:
        """
        최근 공포된 법령 조회
        """
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.search_by_date_range(
            start_date.strftime("%Y%m%d"),
            end_date.strftime("%Y%m%d"),
            date_type="anc",
            sort="ddes",  # 공포일자 내림차순
            **kwargs
        )

"""
법령 종합 정보 API 클라이언트
""" 
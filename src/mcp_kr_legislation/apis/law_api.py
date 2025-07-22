"""
법령 관련 API (16개)

1. 법령 목록 조회 (lawSearch.do?target=law)
2. 법령 본문 조회 (lawService.do?target=law)
3. 영문법령 목록 조회 (lawSearch.do?target=englaw)
4. 영문법령 본문 조회 (lawService.do?target=englaw)
5. 시행일법령 목록 조회 (lawSearch.do?target=eflaw)
6. 법령 변경이력 조회 (lawSearch.do?target=lsHistSearch)
7. 법령 연혁 조회 (lawService.do?target=lsHist)
8. 법령 체계도 조회 (lawService.do?target=lsTree)
9. 신구법비교 조회 (lawService.do?target=lsInfoCmp)
10. 3단 비교 조회 (lawService.do?target=lsTriCmp)
11. 법령 약칭 조회 (lawSearch.do?target=lsNickNm)
12. 삭제데이터 조회 (lawSearch.do?target=deldata)
13. 법령 한눈보기 조회 (lawService.do?target=lsGlance)
14. 조문별 조회 (lawSearch.do?target=jolaw)
15. 별표서식 목록 조회 (lawSearch.do?target=licbyl)
16. 모바일 법령 목록 조회 (lawSearch.do?target=law&mobileYn=Y)
"""

from typing import Dict, Any, Optional, Union
from mcp_kr_legislation.apis.client import LegislationClient


class LawAPI:
    """법령 관련 API 클래스"""
    
    def __init__(self, client: LegislationClient):
        self.client = client

    # ===========================================
    # 기본 법령 API (2개)
    # ===========================================
    
    def search_law(self, 
                   query: Optional[str] = None,
                   search: int = 1,  # 1: 법령명, 2: 본문검색
                   display: int = 20,
                   page: int = 1,
                   sort: str = "lasc",  # lasc: 법령오름차순, ldes: 법령내림차순, dasc: 공포일자오름차순 등
                   **kwargs) -> Dict[str, Any]:
        """
        법령 목록 조회
        
        Args:
            query: 검색할 법령명 또는 키워드
            search: 검색범위 (1: 법령명, 2: 본문검색)
            display: 검색 결과 개수 (기본 20, 최대 100)
            page: 검색 결과 페이지
            sort: 정렬옵션
            **kwargs: 추가 파라미터 (date, efYd, ancYd, ancNo, rrClsCd, nb, org, knd, gana, popYn)
        """
        params = {
            "target": "law",
            "search": search,
            "display": min(display, 100),
            "page": page,
            "sort": sort
        }
        
        if query:
            params["query"] = query
            
        params.update(kwargs)
        return self.client.search("law", params)
    
    def get_law_info(self,
                     law_id: Optional[Union[str, int]] = None,
                     mst: Optional[Union[str, int]] = None,
                     law_name: Optional[str] = None,
                     law_date: Optional[int] = None,
                     law_number: Optional[int] = None,
                     jo: Optional[str] = None,  # 조번호 (000200: 2조)
                     pd: Optional[str] = None,  # 부칙표시
                     pn: Optional[int] = None,  # 부칙번호
                     bd: Optional[str] = None,  # 별표표시
                     bt: Optional[int] = None,  # 별표구분
                     bn: Optional[int] = None,  # 별표번호
                     bg: Optional[int] = None,  # 별표가지번호
                     **kwargs) -> Dict[str, Any]:
        """
        법령 본문 조회
        
        Args:
            law_id: 법령 ID
            mst: 법령 마스터 번호
            law_name: 법령명
            law_date: 법령 공포일자
            law_number: 법령 공포번호
            jo: 조번호 (6자리: 조번호4자리+조가지번호2자리)
            pd: 부칙표시 (ON: 부칙만 출력)
            pn: 부칙번호
            bd: 별표표시 (ON: 모든 별표 표시)
            bt: 별표구분 (1: 별표, 2: 서식, 3: 별지, 4: 별도, 5: 부록)
            bn: 별표번호
            bg: 별표가지번호
        """
        params = {"target": "law"}
        
        if law_id:
            params["ID"] = str(law_id)
        if mst:
            params["MST"] = str(mst)
        if law_name:
            params["LM"] = law_name
        if law_date:
            params["LD"] = law_date
        if law_number:
            params["LN"] = law_number
        if jo:
            params["JO"] = jo
        if pd:
            params["PD"] = pd
        if pn:
            params["PN"] = pn
        if bd:
            params["BD"] = bd
        if bt:
            params["BT"] = bt
        if bn:
            params["BN"] = bn
        if bg:
            params["BG"] = bg
            
        params.update(kwargs)
        return self.client.service("law", params)

    # ===========================================
    # 영문법령 API (2개)
    # ===========================================
    
    def search_englaw(self,
                      query: Optional[str] = None,
                      search: int = 1,  # 1: 법령명, 2: 본문검색
                      display: int = 20,
                      page: int = 1,
                      sort: str = "lasc",
                      **kwargs) -> Dict[str, Any]:
        """영문법령 목록 조회"""
        params = {
            "target": "englaw",
            "search": search,
            "display": min(display, 100),
            "page": page,
            "sort": sort
        }
        
        if query:
            params["query"] = query
            
        params.update(kwargs)
        return self.client.search("englaw", params)
    
    def get_englaw_info(self,
                        law_id: Union[str, int],
                        chr_cls_cd: str = "010202",  # 010202: 한글, 010203: 영문
                        **kwargs) -> Dict[str, Any]:
        """영문법령 본문 조회"""
        params = {
            "target": "englaw",
            "ID": str(law_id),
            "chrClsCd": chr_cls_cd
        }
        
        params.update(kwargs)
        return self.client.service("englaw", params)

    # ===========================================
    # 시행일법령 API (1개)
    # ===========================================
    
    def search_eflaw(self,
                     query: Optional[str] = None,
                     search: int = 1,
                     display: int = 20,
                     page: int = 1,
                     sort: str = "lasc",
                     **kwargs) -> Dict[str, Any]:
        """시행일법령 목록 조회"""
        params = {
            "target": "eflaw",
            "search": search,
            "display": min(display, 100),
            "page": page,
            "sort": sort
        }
        
        if query:
            params["query"] = query
            
        params.update(kwargs)
        return self.client.search("eflaw", params)

    # ===========================================
    # 법령 연혁/변경이력 API (2개)
    # ===========================================
    
    def search_law_history(self,
                           query: Optional[str] = None,
                           search: int = 1,
                           display: int = 20,
                           page: int = 1,
                           **kwargs) -> Dict[str, Any]:
        """법령 변경이력 목록 조회"""
        params = {
            "target": "lsHistSearch",
            "search": search,
            "display": min(display, 100),
            "page": page
        }
        
        if query:
            params["query"] = query
            
        params.update(kwargs)
        return self.client.search("lsHistSearch", params)
    
    def get_law_history_info(self,
                             law_id: Union[str, int],
                             **kwargs) -> Dict[str, Any]:
        """법령 연혁 조회"""
        params = {
            "target": "lsHist",
            "ID": str(law_id)
        }
        
        params.update(kwargs)
        return self.client.service("lsHist", params)

    # ===========================================
    # 법령 체계도 API (1개)
    # ===========================================
    
    def get_law_tree(self,
                     law_id: Union[str, int],
                     **kwargs) -> Dict[str, Any]:
        """법령 체계도 조회"""
        params = {
            "target": "lsTree",
            "ID": str(law_id)
        }
        
        params.update(kwargs)
        return self.client.service("lsTree", params)

    # ===========================================
    # 신구법비교/3단비교 API (2개)
    # ===========================================
    
    def get_law_comparison(self,
                           law_id: Union[str, int],
                           **kwargs) -> Dict[str, Any]:
        """신구법비교 조회"""
        params = {
            "target": "lsInfoCmp",
            "ID": str(law_id)
        }
        
        params.update(kwargs)
        return self.client.service("lsInfoCmp", params)
    
    def get_law_tri_comparison(self,
                               law_id: Union[str, int],
                               **kwargs) -> Dict[str, Any]:
        """3단 비교 조회"""
        params = {
            "target": "lsTriCmp",
            "ID": str(law_id)
        }
        
        params.update(kwargs)
        return self.client.service("lsTriCmp", params)

    # ===========================================
    # 법령 약칭/삭제데이터 API (2개)
    # ===========================================
    
    def search_law_nickname(self,
                            query: Optional[str] = None,
                            display: int = 20,
                            page: int = 1,
                            **kwargs) -> Dict[str, Any]:
        """법령 약칭 조회"""
        params = {
            "target": "lsNickNm",
            "display": min(display, 100),
            "page": page
        }
        
        if query:
            params["query"] = query
            
        params.update(kwargs)
        return self.client.search("lsNickNm", params)
    
    def search_deleted_data(self,
                            query: Optional[str] = None,
                            search: int = 1,
                            display: int = 20,
                            page: int = 1,
                            **kwargs) -> Dict[str, Any]:
        """삭제데이터 조회"""
        params = {
            "target": "deldata",
            "search": search,
            "display": min(display, 100),
            "page": page
        }
        
        if query:
            params["query"] = query
            
        params.update(kwargs)
        return self.client.search("deldata", params)

    # ===========================================
    # 법령 한눈보기/조문별 API (2개)
    # ===========================================
    
    def get_law_glance(self,
                       law_id: Union[str, int],
                       **kwargs) -> Dict[str, Any]:
        """법령 한눈보기 조회"""
        params = {
            "target": "lsGlance",
            "ID": str(law_id)
        }
        
        params.update(kwargs)
        return self.client.service("lsGlance", params)
    
    def search_law_articles(self,
                            law_id: Union[str, int],
                            display: int = 20,
                            page: int = 1,
                            **kwargs) -> Dict[str, Any]:
        """조문별 조회"""
        params = {
            "target": "jolaw",
            "ID": str(law_id),
            "display": min(display, 100),
            "page": page
        }
        
        params.update(kwargs)
        return self.client.search("jolaw", params)

    # ===========================================
    # 별표서식/모바일 API (2개)
    # ===========================================
    
    def search_law_appendix(self,
                            query: Optional[str] = None,
                            search: int = 1,  # 1: 별표서식명, 2: 해당법령검색, 3: 별표본문검색
                            display: int = 20,
                            page: int = 1,
                            sort: str = "lasc",
                            org: Optional[str] = None,  # 소관부처코드
                            knd: Optional[str] = None,  # 별표종류 (1: 별표, 2: 서식, 3: 별지, 4: 별도, 5: 부록)
                            **kwargs) -> Dict[str, Any]:
        """별표서식 목록 조회"""
        params = {
            "target": "licbyl",
            "search": search,
            "display": min(display, 100),
            "page": page,
            "sort": sort
        }
        
        if query:
            params["query"] = query
        if org:
            params["org"] = org
        if knd:
            params["knd"] = knd
            
        params.update(kwargs)
        return self.client.search("licbyl", params)
    
    def search_mobile_law(self,
                          query: Optional[str] = None,
                          search: int = 1,
                          display: int = 20,
                          page: int = 1,
                          sort: str = "lasc",
                          **kwargs) -> Dict[str, Any]:
        """모바일 법령 목록 조회"""
        params = {
            "target": "law",
            "mobileYn": "Y",
            "search": search,
            "display": min(display, 100),
            "page": page,
            "sort": sort
        }
        
        if query:
            params["query"] = query
            
        params.update(kwargs)
        return self.client.search("law", params)
    
    def get_mobile_law_info(self,
                            law_id: Optional[Union[str, int]] = None,
                            mst: Optional[Union[str, int]] = None,
                            **kwargs) -> Dict[str, Any]:
        """모바일 법령 본문 조회"""
        params = {
            "target": "law",
            "mobileYn": "Y",
            "type": "HTML"  # 모바일은 HTML만 지원
        }
        
        if law_id:
            params["ID"] = str(law_id)
        if mst:
            params["MST"] = str(mst)
            
        params.update(kwargs)
        return self.client.service("law", params) 
"""
레지스트리 초기화
"""

from mcp_kr_legislation.registry.tool_registry import ToolRegistry

def initialize_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register_tool(
        name="search_legislation",
        korean_name="법령 검색",
        description="""
법령을 검색합니다.

Arguments:
- query (str, optional): 검색할 법령명 또는 키워드
- search_type (int): 검색범위 (1: 법령명, 2: 본문검색)
- display (int): 검색 결과 개수 (기본 20, 최대 100)
- page (int): 검색 결과 페이지
- sort (str): 정렬옵션 (lasc: 법령오름차순, ldes: 법령내림차순 등)

Returns: 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 법령명 또는 키워드"},
                "search_type": {"type": "integer", "description": "검색범위 (1: 법령명, 2: 본문검색)", "default": 1},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1},
                "sort": {"type": "string", "description": "정렬옵션", "default": "lasc"}
            },
            "required": []
        },
        linked_tools=["search_by_law_name", "search_by_content"]
    )

    registry.register_tool(
        name="search_by_law_name",
        korean_name="법령명 검색",
        description="""
법령명으로 정확히 검색합니다.

Arguments:
- law_name (str, required): 검색할 법령명
- display (int): 검색 결과 개수 (기본 20, 최대 100)
- page (int): 검색 결과 페이지

Returns: 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "law_name": {"type": "string", "description": "검색할 법령명"},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1}
            },
            "required": ["law_name"]
        },
        linked_tools=["search_by_content"]
    )

    registry.register_tool(
        name="search_by_content",
        korean_name="본문 검색",
        description="""
법령 본문 내용으로 검색합니다.

Arguments:
- keyword (str, required): 검색할 키워드
- display (int): 검색 결과 개수 (기본 20, 최대 100)
- page (int): 검색 결과 페이지

Returns: 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "검색할 키워드"},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1}
            },
            "required": ["keyword"]
        },
        linked_tools=[]
    )

    registry.register_tool(
        name="search_by_ministry",
        korean_name="소관부처별 검색",
        description="""
소관부처별로 법령을 검색합니다.

Arguments:
- org_code (str, required): 소관부처 코드
- display (int): 검색 결과 개수 (기본 20, 최대 100)
- page (int): 검색 결과 페이지

Returns: 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "org_code": {"type": "string", "description": "소관부처 코드"},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1}
            },
            "required": ["org_code"]
        },
        linked_tools=[]
    )

    registry.register_tool(
        name="get_recent_laws",
        korean_name="최근 법령 조회",
        description="""
최근 공포된 법령을 조회합니다.

Arguments:
- days (int): 최근 며칠간의 법령 (기본 30일)
- display (int): 검색 결과 개수 (기본 20, 최대 100)

Returns: 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "days": {"type": "integer", "description": "최근 며칠간의 법령", "default": 30},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20}
            },
            "required": []
        },
        linked_tools=[]
    )

    registry.register_tool(
        name="search_by_date_range",
        korean_name="날짜 범위 검색",
        description="""
날짜 범위로 법령을 검색합니다.

Arguments:
- start_date (str, required): 시작일자 (YYYYMMDD)
- end_date (str, required): 종료일자 (YYYYMMDD)
- date_type (str): 날짜 유형 ('anc': 공포일자, 'ef': 시행일자)
- display (int): 검색 결과 개수 (기본 20, 최대 100)
- page (int): 검색 결과 페이지

Returns: 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "description": "시작일자 (YYYYMMDD)"},
                "end_date": {"type": "string", "description": "종료일자 (YYYYMMDD)"},
                "date_type": {"type": "string", "description": "날짜 유형", "default": "anc"},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1}
            },
            "required": ["start_date", "end_date"]
        },
        linked_tools=[]
    )

    return registry 
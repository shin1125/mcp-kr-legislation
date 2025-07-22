"""
한국 법제처 OPEN API 125개 완전 통합 도구 레지스트리 초기화
"""

from mcp_kr_legislation.registry.tool_registry import ToolRegistry

def initialize_registry() -> ToolRegistry:
    registry = ToolRegistry()

    # ===========================================
    # 법령 관련 도구 (16개)
    # ===========================================
    
    registry.register_tool(
        name="search_law",
        korean_name="법령 검색",
        description="""
법령 목록을 검색합니다.

Arguments:
- query: 검색할 법령명 또는 키워드
- search_type: 검색범위 (1: 법령명, 2: 본문검색)
- display: 검색 결과 개수 (기본 20, 최대 100)
- page: 검색 결과 페이지
- sort: 정렬옵션 (lasc: 법령오름차순, ldes: 법령내림차순 등)
- date: 검색일자 (YYYYMMDD~YYYYMMDD)
- ef_yd: 시행일자 (YYYYMMDD~YYYYMMDD)
- anc_yd: 공포일자 (YYYYMMDD~YYYYMMDD)
- anc_no: 공포번호
- rr_cls_cd: 법령구분코드
- nb: 호별
- org: 소관부처코드
- knd: 법령종류
- gana: 가나다순
- pop_yn: 인기법령 여부

Returns: 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 법령명 또는 키워드"},
                "search_type": {"type": "integer", "description": "검색범위 (1: 법령명, 2: 본문검색)", "default": 1},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1},
                "sort": {"type": "string", "description": "정렬옵션", "default": "lasc"},
                "date": {"type": "string", "description": "검색일자 (YYYYMMDD~YYYYMMDD)"},
                "ef_yd": {"type": "string", "description": "시행일자 (YYYYMMDD~YYYYMMDD)"},
                "anc_yd": {"type": "string", "description": "공포일자 (YYYYMMDD~YYYYMMDD)"},
                "anc_no": {"type": "string", "description": "공포번호"},
                "rr_cls_cd": {"type": "string", "description": "법령구분코드"},
                "nb": {"type": "string", "description": "호별"},
                "org": {"type": "string", "description": "소관부처코드"},
                "knd": {"type": "string", "description": "법령종류"},
                "gana": {"type": "string", "description": "가나다순"},
                "pop_yn": {"type": "string", "description": "인기법령 여부"}
            },
            "required": []
        },
        linked_tools=["get_law_info", "search_englaw"]
    )

    registry.register_tool(
        name="get_law_info",
        korean_name="법령 본문 조회",
        description="""
법령 본문을 조회합니다.

Arguments:
- law_id: 법령 ID
- mst: 법령 마스터 번호
- law_name: 법령명
- law_date: 법령 공포일자
- law_number: 법령 공포번호
- jo: 조번호 (6자리: 조번호4자리+조가지번호2자리)
- pd: 부칙표시 (ON: 부칙만 출력)
- pn: 부칙번호
- bd: 별표표시 (ON: 모든 별표 표시)
- bt: 별표구분 (1: 별표, 2: 서식, 3: 별지, 4: 별도, 5: 부록)
- bn: 별표번호
- bg: 별표가지번호

Returns: 법령 본문이 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "law_id": {"type": ["string", "integer"], "description": "법령 ID"},
                "mst": {"type": ["string", "integer"], "description": "법령 마스터 번호"},
                "law_name": {"type": "string", "description": "법령명"},
                "law_date": {"type": "integer", "description": "법령 공포일자"},
                "law_number": {"type": "integer", "description": "법령 공포번호"},
                "jo": {"type": "string", "description": "조번호 (6자리)"},
                "pd": {"type": "string", "description": "부칙표시 (ON: 부칙만 출력)"},
                "pn": {"type": "integer", "description": "부칙번호"},
                "bd": {"type": "string", "description": "별표표시 (ON: 모든 별표 표시)"},
                "bt": {"type": "integer", "description": "별표구분 (1: 별표, 2: 서식, 3: 별지, 4: 별도, 5: 부록)"},
                "bn": {"type": "integer", "description": "별표번호"},
                "bg": {"type": "integer", "description": "별표가지번호"}
            },
            "required": []
        },
        linked_tools=["search_law"]
    )

    registry.register_tool(
        name="search_englaw",
        korean_name="영문법령 검색",
        description="""
영문법령 목록을 조회합니다.

Arguments:
- query: 검색할 법령명 또는 키워드
- search_type: 검색범위 (1: 법령명, 2: 본문검색)
- display: 검색 결과 개수
- page: 검색 결과 페이지
- sort: 정렬옵션

Returns: 영문법령 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
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
        linked_tools=["get_englaw_info"]
    )

    registry.register_tool(
        name="get_englaw_info",
        korean_name="영문법령 본문 조회",
        description="""
영문법령 본문을 조회합니다.

Arguments:
- law_id: 법령 ID
- chr_cls_cd: 문자셋코드 (010202: 한글, 010203: 영문)

Returns: 영문법령 본문이 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "law_id": {"type": ["string", "integer"], "description": "법령 ID"},
                "chr_cls_cd": {"type": "string", "description": "문자셋코드 (010202: 한글, 010203: 영문)", "default": "010202"}
            },
            "required": ["law_id"]
        },
        linked_tools=["search_englaw"]
    )

    # ===========================================
    # 행정규칙 관련 도구 (2개)
    # ===========================================
    
    registry.register_tool(
        name="search_admrul",
        korean_name="행정규칙 검색",
        description="""
행정규칙 목록을 조회합니다.

Arguments:
- query: 검색할 행정규칙명 또는 키워드
- search_type: 검색범위 (1: 법령명, 2: 본문검색)
- display: 검색 결과 개수
- page: 검색 결과 페이지
- sort: 정렬옵션

Returns: 행정규칙 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 행정규칙명 또는 키워드"},
                "search_type": {"type": "integer", "description": "검색범위 (1: 법령명, 2: 본문검색)", "default": 1},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1},
                "sort": {"type": "string", "description": "정렬옵션", "default": "lasc"}
            },
            "required": []
        },
        linked_tools=["get_admrul_info"]
    )

    registry.register_tool(
        name="get_admrul_info",
        korean_name="행정규칙 본문 조회",
        description="""
행정규칙 본문을 조회합니다.

Arguments:
- admrul_id: 행정규칙 ID

Returns: 행정규칙 본문이 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "admrul_id": {"type": ["string", "integer"], "description": "행정규칙 ID"}
            },
            "required": ["admrul_id"]
        },
        linked_tools=["search_admrul"]
    )

    # ===========================================
    # 자치법규 관련 도구 (2개)
    # ===========================================
    
    registry.register_tool(
        name="search_ordin",
        korean_name="자치법규 검색",
        description="""
자치법규 목록을 조회합니다.

Arguments:
- query: 검색할 자치법규명 또는 키워드
- search_type: 검색범위 (1: 법령명, 2: 본문검색)
- display: 검색 결과 개수
- page: 검색 결과 페이지
- sort: 정렬옵션

Returns: 자치법규 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 자치법규명 또는 키워드"},
                "search_type": {"type": "integer", "description": "검색범위 (1: 법령명, 2: 본문검색)", "default": 1},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1},
                "sort": {"type": "string", "description": "정렬옵션", "default": "lasc"}
            },
            "required": []
        },
        linked_tools=["get_ordin_info"]
    )

    registry.register_tool(
        name="get_ordin_info",
        korean_name="자치법규 본문 조회",
        description="""
자치법규 본문을 조회합니다.

Arguments:
- ordin_id: 자치법규 ID

Returns: 자치법규 본문이 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "ordin_id": {"type": ["string", "integer"], "description": "자치법규 ID"}
            },
            "required": ["ordin_id"]
        },
        linked_tools=["search_ordin"]
    )

    # ===========================================
    # 판례 관련 도구 (2개)
    # ===========================================
    
    registry.register_tool(
        name="search_prec",
        korean_name="판례 검색",
        description="""
판례 목록을 조회합니다.

Arguments:
- query: 검색할 키워드
- search_type: 검색범위
- display: 검색 결과 개수
- page: 검색 결과 페이지
- sort: 정렬옵션

Returns: 판례 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 키워드"},
                "search_type": {"type": "integer", "description": "검색범위", "default": 1},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1},
                "sort": {"type": "string", "description": "정렬옵션", "default": "lasc"}
            },
            "required": []
        },
        linked_tools=["get_prec_info"]
    )

    registry.register_tool(
        name="get_prec_info",
        korean_name="판례 본문 조회",
        description="""
판례 본문을 조회합니다.

Arguments:
- prec_id: 판례 ID

Returns: 판례 본문이 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "prec_id": {"type": ["string", "integer"], "description": "판례 ID"}
            },
            "required": ["prec_id"]
        },
        linked_tools=["search_prec"]
    )

    # ===========================================
    # 법령용어 관련 도구 (2개)
    # ===========================================
    
    registry.register_tool(
        name="search_lstrm",
        korean_name="법령용어 검색",
        description="""
법령용어 목록을 조회합니다.

Arguments:
- query: 검색할 용어
- search_type: 검색범위
- display: 검색 결과 개수
- page: 검색 결과 페이지

Returns: 법령용어 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 용어"},
                "search_type": {"type": "integer", "description": "검색범위", "default": 1},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1}
            },
            "required": []
        },
        linked_tools=["get_lstrm_info"]
    )

    registry.register_tool(
        name="get_lstrm_info",
        korean_name="법령용어 본문 조회",
        description="""
법령용어 본문을 조회합니다.

Arguments:
- query: 조회할 용어

Returns: 법령용어 본문이 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "조회할 용어"}
            },
            "required": ["query"]
        },
        linked_tools=["search_lstrm"]
    )

    # ===========================================
    # 조약 관련 도구 (2개)
    # ===========================================
    
    registry.register_tool(
        name="search_trty",
        korean_name="조약 검색",
        description="""
조약 목록을 조회합니다.

Arguments:
- query: 검색할 조약명 또는 키워드
- search_type: 검색범위
- display: 검색 결과 개수
- page: 검색 결과 페이지
- sort: 정렬옵션

Returns: 조약 검색 결과가 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 조약명 또는 키워드"},
                "search_type": {"type": "integer", "description": "검색범위", "default": 1},
                "display": {"type": "integer", "description": "검색 결과 개수", "default": 20},
                "page": {"type": "integer", "description": "검색 결과 페이지", "default": 1},
                "sort": {"type": "string", "description": "정렬옵션", "default": "lasc"}
            },
            "required": []
        },
        linked_tools=["get_trty_info"]
    )

    registry.register_tool(
        name="get_trty_info",
        korean_name="조약 본문 조회",
        description="""
조약 본문을 조회합니다.

Arguments:
- trty_id: 조약 ID

Returns: 조약 본문이 저장된 JSON 파일 경로를 반환합니다.
""",
        parameters={
            "type": "object",
            "properties": {
                "trty_id": {"type": ["string", "integer"], "description": "조약 ID"}
            },
            "required": ["trty_id"]
        },
        linked_tools=["search_trty"]
    )

    return registry 
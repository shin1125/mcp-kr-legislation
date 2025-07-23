"""
데이터 처리 및 캐시 관리 유틸리티
"""

import os
import sys
import tempfile
from pathlib import Path

def get_cache_dir():
    """
    Returns the cache directory for storing legislation data.
    Priority:
    1. MCP_LEGISLATION_CACHE_DIR environment variable
    2. Project's data directory (./data)
    3. OS user cache dir (fallback)
    4. /tmp (as last resort)
    """
    # 1. 환경변수 우선
    cache_dir = os.environ.get("MCP_LEGISLATION_CACHE_DIR")
    if cache_dir:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    # 2. 프로젝트 내 data 디렉토리 (기본값)
    try:
        # 현재 파일의 위치를 기준으로 프로젝트 루트 찾기
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent  # utils -> mcp_kr_legislation -> src -> project_root
        data_dir = project_root / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return str(data_dir)
    except Exception:
        pass
    
    # 3. OS별 표준 사용자 캐시 디렉토리 (fallback)
    if sys.platform == "win32":
        local_appdata = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
        cache_dir = os.path.join(local_appdata, "mcp-kr-legislation-cache")
    else:
        cache_dir = os.path.expanduser("~/.cache/mcp-kr-legislation")
    
    try:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        return cache_dir
    except Exception:
        pass
    
    # 4. /tmp (최후의 수단)
    tmp_cache = os.path.join(tempfile.gettempdir(), "mcp-kr-legislation-cache")
    Path(tmp_cache).mkdir(parents=True, exist_ok=True)
    return tmp_cache 
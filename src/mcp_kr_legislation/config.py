"""
환경변수 및 설정 관리
""" 

import os
import logging
from typing import Literal, cast
from dataclasses import dataclass
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class LegislationConfig:
    """법령 종합 정보 API configuration."""
    oc: str  # 사용자 이메일 ID
    base_url: str = "http://www.law.go.kr/DRF/lawSearch.do"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "legislation.log"

    @classmethod
    def from_env(cls) -> "LegislationConfig":
        oc = os.getenv("LEGISLATION_API_KEY")
        if not oc:
            raise ValueError("법령 API 키(OC)가 설정되지 않았습니다. .env 파일을 확인하세요.")
        return cls(
            oc=oc,
            base_url=os.getenv("LEGISLATION_BASE_URL", "http://www.law.go.kr/DRF/lawSearch.do"),
            log_format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            log_file=os.getenv("LOG_FILE", "legislation.log")
        )

@dataclass
class MCPConfig:
    host: str = "0.0.0.0"
    port: int = 8001
    log_level: str = "INFO"
    server_name: str = "kr-legislation-mcp"
    transport: Literal["stdio", "sse"] = "stdio"

    @classmethod
    def from_env(cls) -> "MCPConfig":
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8001")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            server_name=os.getenv("MCP_SERVER_NAME", "kr-legislation-mcp"),
            transport=cast(Literal["stdio", "sse"], os.getenv("TRANSPORT", "stdio"))
        )

# 설정 인스턴스 생성
def _try_make_config():
    try:
        return LegislationConfig.from_env()
    except Exception:
        return None

legislation_config = _try_make_config()
mcp_config = MCPConfig.from_env() 
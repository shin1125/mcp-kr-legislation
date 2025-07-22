import os
import requests
from dotenv import load_dotenv
from urllib.parse import urljoin, urlencode
import json
import logging
from typing import Dict, Any, Optional
import zipfile
import io
from mcp_kr_legislation.config import LegislationConfig, legislation_config

load_dotenv()

logger = logging.getLogger(__name__)

class LegislationClient:
    """법령 종합 정보 API 클라이언트"""
    def __init__(self, config: Optional[LegislationConfig] = None):
        self.config = config or legislation_config
        self.oc = self.config.oc  # 사용자 이메일 ID
        self.base_url = self.config.base_url
        if not self.oc:
            raise ValueError("법령 API 키(OC)가 설정되지 않았습니다.")

    def _make_request(self, params: Optional[Dict[str, Any]] = None, method: str = "GET") -> Dict[str, Any]:
        if params is None:
            params = {}
        
        # 기본 파라미터 설정
        params.update({
            "OC": self.oc,
            "target": "law",
            "type": "JSON"
        })
        
        # URL 생성
        if method.upper() == "GET":
            query_string = urlencode(params, safe='~')
            url = f"{self.base_url}?{query_string}"
        else:
            url = self.base_url
            
        logger.debug(f"\n=== API 요청 정보 ===")
        logger.debug(f"URL: {url}")
        logger.debug(f"Method: {method}")
        logger.debug(f"Parameters: {params}")
        logger.debug("====================")
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, data=params, timeout=30)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")
                
            logger.debug(f"\n=== API 응답 정보 ===")
            logger.debug(f"상태 코드: {response.status_code}")
            logger.debug(f"Content-Type: {response.headers.get('Content-Type', '없음')}")
            logger.debug("====================")
            
            response.raise_for_status()
            
            # 응답 처리
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                response_data: Dict[str, Any] = response.json()
                return response_data
            else:
                # JSON이 아닌 경우 텍스트로 처리한 후 JSON 파싱 시도
                try:
                    parsed_data: Dict[str, Any] = json.loads(response.text)
                    return parsed_data
                except json.JSONDecodeError:
                    return {"status": "000", "message": "정상", "content": response.text}
                    
        except requests.RequestException as e:
            logger.error(f"API 요청 실패: {str(e)}")
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}

    def get(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request(params, "GET")

    def post(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._make_request(params, "POST")

"""
법령 정보 HTTP 클라이언트
""" 
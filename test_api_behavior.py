#!/usr/bin/env python3
"""
법제처 API 동작 테스트 스크립트
실제 API 호출을 통해 동작을 검증합니다.
"""

import urllib.request
import urllib.parse
import json
import sys

def test_api_call(description, url, params):
    """API 호출 테스트"""
    print(f"\n{'=' * 60}")
    print(f"테스트: {description}")
    print(f"{'=' * 60}")
    
    # URL 인코딩
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    print(f"URL: {full_url[:100]}...")
    print(f"Params: {params}")
    
    try:
        # API 호출
        with urllib.request.urlopen(full_url, timeout=10) as response:
            content_type = response.headers.get('Content-Type', '')
            content = response.read().decode('utf-8')
            
            print(f"Status: {response.status}")
            print(f"Content-Type: {content_type}")
            print(f"Response Size: {len(content)} bytes")
            
            # JSON 파싱 시도
            if 'json' in content_type.lower():
                data = json.loads(content)
                
                # 검색 결과 분석
                if 'LawSearch' in data:
                    search_result = data['LawSearch']
                    total = search_result.get('totalCnt', 0)
                    result_code = search_result.get('resultCode')
                    result_msg = search_result.get('resultMsg')
                    
                    print(f"\n✅ 검색 성공!")
                    print(f"총 결과: {total}건")
                    print(f"결과 코드: {result_code} ({result_msg})")
                    
                    # 첫 번째 결과 표시
                    laws = search_result.get('law', [])
                    if isinstance(laws, list) and laws:
                        first_law = laws[0]
                        print(f"\n첫 번째 결과:")
                        print(f"  - 법령명: {first_law.get('법령명한글', 'N/A')}")
                        print(f"  - 법령ID: {first_law.get('법령ID', 'N/A')}")
                        print(f"  - MST: {first_law.get('법령일련번호', 'N/A')}")
                else:
                    print("\n⚠️ LawSearch 키가 없는 응답")
                    print(f"응답 키: {list(data.keys())[:5]}")
            else:
                print("\n❌ JSON이 아닌 응답")
                if '사용자인증에 실패' in content:
                    print("→ 인증 실패 (OC 확인 필요)")
                elif '페이지 접속에 실패' in content:
                    print("→ 접속 실패")
                else:
                    print(f"응답 일부: {content[:200]}...")
                    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

def main():
    """메인 테스트 실행"""
    base_search_url = "http://www.law.go.kr/DRF/lawSearch.do"
    base_service_url = "http://www.law.go.kr/DRF/lawService.do"
    oc = "lchangoo"
    
    # 테스트 1: 기본 검색 - 정확한 법령명
    test_api_call(
        "정확한 법령명 검색",
        base_search_url,
        {
            "OC": oc,
            "type": "JSON",
            "target": "law",
            "query": "개인정보보호법",
            "display": 5
        }
    )
    
    # 테스트 2: 키워드만 검색
    test_api_call(
        "키워드만 검색 (법 없이)",
        base_search_url,
        {
            "OC": oc,
            "type": "JSON",
            "target": "law",
            "query": "개인정보보호",
            "display": 5
        }
    )
    
    # 테스트 3: 본문검색
    test_api_call(
        "본문검색 모드",
        base_search_url,
        {
            "OC": oc,
            "type": "JSON",
            "target": "law",
            "query": "개인정보보호",
            "search": 2,
            "display": 5
        }
    )
    
    # 테스트 4: 잘못된 OC
    test_api_call(
        "잘못된 OC로 인증 실패",
        base_search_url,
        {
            "OC": "wrongkey",
            "type": "JSON",
            "target": "law",
            "query": "개인정보보호법"
        }
    )
    
    # 테스트 5: OC 없이 호출
    test_api_call(
        "OC 파라미터 없이",
        base_search_url,
        {
            "type": "JSON",
            "target": "law",
            "query": "개인정보보호법"
        }
    )

if __name__ == "__main__":
    main() 
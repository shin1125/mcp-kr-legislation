#!/usr/bin/env python3
"""
search_law의 법령일련번호(MST) 표시 테스트
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_kr_legislation.tools.law_tools import search_law

# 개선 전후 비교
print("=== search_law 응답에 법령일련번호(MST) 표시 테스트 ===\n")

# 테스트 실행
result = search_law("개인정보보호법", display=3)

print(result.text)

print("\n" + "="*60)
print("✅ 이제 search_law 응답에 다음 정보가 포함됩니다:")
print("1. 법령ID (예: 011357)")
print("2. 법령일련번호(MST) (예: 248613) ← 새로 추가!")
print("3. 상세조회 가이드")
print("   - MST가 있으면: get_law_detail_unified(mst=\"248613\", target=\"law\")")
print("   - 법령ID만 있으면: get_law_detail(law_id=\"011357\")") 
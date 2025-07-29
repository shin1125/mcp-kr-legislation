# 🌍 영문 법령 검색 워크플로우 가이드

## 📋 권장 검색 순서

### 🥇 **1순위: get_english_law_summary (통합 도구)**
- **모든 영문 법령 관련 질문의 시작점**
- 한 번의 호출로 검색 → 상세 정보 → 키워드 검색까지 모두 처리
- 캐시 활용으로 빠른 응답

```
사용자 질문 → get_english_law_summary → 완성된 답변
```

### 🥈 **2순위: 개별 도구 (특수한 경우만)**
- 매우 구체적인 요구사항이 있을 때만 사용
- get_english_law_summary로 해결되지 않는 경우

## 🎯 사용 예시

### 📝 **예시 1: 기본 법령 정보 요청**
```
사용자: "Show me Korean Civil Act in English"
LLM: get_english_law_summary("Civil Act")
```

### 📝 **예시 2: 특정 주제 검색**
```
사용자: "What does Korean Commercial Act say about company formation?"
LLM: get_english_law_summary("Commercial Act", "company formation", True)
```

### 📝 **예시 3: 계약 관련 조항**
```
사용자: "Find contract provisions in Korean Civil Act"
LLM: get_english_law_summary("Civil Act", "contract", True)
```

## ⚙️ 내부 동작 원리

### get_english_law_summary의 자동 처리 과정:

1. **🔍 법령 검색**: search_english_law 로직으로 영문 법령 찾기
2. **📄 기본 정보**: 영문명, 한글명, 공포일자, 시행일자 등 표시
3. **🎯 키워드 검색**: (선택) search_english_law_articles_semantic으로 관련 조문 찾기
4. **📖 상세 내용**: (선택) 전체 조문 내용 표시
5. **💾 캐시 저장**: 향후 빠른 검색을 위해 데이터 캐시

## 🛠️ 도구별 역할

| 도구명 | 역할 | 사용 빈도 | 비고 |
|--------|------|-----------|------|
| **get_english_law_summary** | **메인** | **90%** | **영문 법령 질문의 첫 번째 선택** |
| search_english_law | 보조 | 5% | 단순 검색 목록만 필요할 때 |
| get_english_law_detail | 보조 | 5% | 특정 MST의 상세 조문만 필요할 때 |
| search_english_law_articles_semantic | **내부용** | 0% | **사용자가 직접 호출하지 않음** |

## ✅ 권장 사용법

### 🎯 **LLM이 자동으로 해야 할 것:**
1. 영문 법령 관련 질문 → **무조건 get_english_law_summary 사용**
2. 키워드가 포함된 질문 → keyword 파라미터 활용
3. 상세 내용 요청 → show_detail=True 설정
4. 영어/한국어 법령명 모두 지원

### 🎯 **사용자에게 제공할 것:**
- 영문 법령명과 한글 법령명 병기
- 기본 정보 (공포일자, 시행일자, 소관부처)
- 키워드 관련 조문 (영어로 표시)
- 추가 상세 조회 방법 안내

## ❌ 피해야 할 사용법

### 🚫 **하지 말아야 할 것:**
- search_english_law + get_english_law_detail 개별 호출
- search_english_law_articles_semantic 직접 호출
- 영문 법령 질문에 한글 법령 도구 사용

### 🚫 **잘못된 예시:**
```
❌ search_english_law("Civil Act") → 검색 결과만 나옴
❌ get_english_law_detail("123456") → MST 없이 호출
❌ get_law_summary("Civil Act") → 한글 도구 사용
```

### ✅ **올바른 예시:**
```
✅ get_english_law_summary("Civil Act", "contract", True)
✅ get_english_law_summary("Commercial Act", "company")
✅ get_english_law_summary("민법") → 한국어 법령명도 지원
```

## 🎁 주요 장점

### 📈 **성능 향상:**
- 캐시 활용으로 2회째부터 빠른 응답
- 한 번의 호출로 모든 정보 제공
- 불필요한 API 호출 최소화

### 🎯 **사용성 향상:**
- 영어 키워드로 한국 법령 조문 검색 가능
- 복잡한 절차 없이 원하는 정보 바로 제공
- 외국인도 쉽게 이해할 수 있는 영문 표시

### 🌍 **국제화 지원:**
- 한국 법령의 영문 번역본 제공
- 외국인 대상 법률 상담 지원
- 국제 업무에서 한국 법령 참조 용이

---

## 📞 사용자 질문 패턴별 대응

| 질문 유형 | LLM 대응 | 예시 |
|-----------|----------|------|
| 기본 정보 | `get_english_law_summary("법령명")` | "Show me Civil Act" |
| 특정 주제 | `get_english_law_summary("법령명", "키워드")` | "Contract in Civil Act" |
| 상세 내용 | `get_english_law_summary("법령명", "키워드", True)` | "Full article about company" |
| 비교 분석 | 여러 번 호출 후 비교 | "Compare Civil vs Commercial" |

이 가이드를 따라 영문 법령 검색 기능을 최적으로 활용하세요! 🚀 
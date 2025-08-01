# 한국 법제처 API - 법령 도구 종합 테스트 가이드 (완전판)

> 💡 **이 가이드는 법 지식이 없는 일반인도 쉽게 따라할 수 있도록 작성되었습니다.**
> 
> 각 섹션의 프롬프트를 Claude에게 순서대로 입력하면서 모든 법령 도구를 체험해보세요!
> 
> 🎯 **디버깅 목적**: 각 단계마다 도구명, 응답 결과, 오류 등을 상세히 분석합니다.

---

## 🏁 1단계: 기본 법령 검색 (일상생활 관련) - 도로교통법 & 부동산거래

### 1-1. 도로교통법 통합 검색 (search_law_unified 테스트)
```
자동차 운전할 때 지켜야 할 법령을 검색해주세요. "도로교통법" 또는 "교통" 키워드로 관련 법령들을 모두 찾아주세요. search_law_unified 도구를 사용해서 포괄적으로 검색해주세요.
```

### 1-2. 도로교통법 정밀 검색 (search_law 테스트)
```
위에서 찾은 도로교통법을 이제 정확한 법령명으로 정밀 검색해주세요. search_law 도구를 사용해서 "도로교통법"을 검색하고, 법령ID와 MST 정보를 확인해주세요.
```

### 1-3. 도로교통법 전체 요약 (get_law_summary 테스트)
```
도로교통법의 전체 내용을 요약해서 보여주세요. get_law_summary 도구를 사용해서 법령의 목적, 주요 조문, 제개정 이유 등을 포함한 종합적인 정보를 제공해주세요. 특히 운전면허나 교통사고 처리에 대한 내용이 궁금합니다.
```

### 1-4. 도로교통법 상세 조회 (get_law_detail_unified 테스트)
```
도로교통법의 상세 내용을 조회해주세요. get_law_detail_unified 도구를 사용해서 조문 목록과 기본 정보를 확인해주세요. MST 번호는 위 단계에서 얻은 정보를 사용하세요.
```

### 1-5. 도로교통법 특정 조문 조회 (get_law_article_by_key 테스트)
```
도로교통법의 제54조(교통사고 처리)와 제80조(운전면허) 조문을 각각 상세히 조회해주세요. get_law_article_by_key 도구를 사용해서 두 조문의 전체 내용을 보여주세요.
```

### 1-6. 부동산 거래 관련 법령 통합 검색
```
집을 사거나 전세를 구할 때 알아야 할 법적 규정을 찾아주세요. "부동산" 키워드로 search_law_unified를 사용해서 관련 법령들을 모두 검색해주세요.
```

### 1-7. 공인중개사법 상세 분석
```
부동산 거래와 관련된 공인중개사법의 전체 내용을 분석해주세요. get_law_summary를 사용해서 법령 전체를 요약하고, 특히 중개수수료(제32조)와 계약서 작성(제25조) 관련 조문을 get_law_article_by_key로 상세 조회해주세요.
```

**🔍 1단계 분석 요청:**
```
위 1단계 테스트를 수행한 결과를 분석해주세요:
1. 사용된 MCP 도구명과 각각의 성공/실패 여부
2. 응답 데이터의 품질과 완성도 
3. 오류가 발생한 부분과 구체적인 오류 내용
4. 재호출이 필요했던 경우와 그 이유
5. 각 도구의 응답 시간과 데이터 크기
6. 도구 간 연계성과 워크플로우의 자연스러움
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 🌍 2단계: 영문 법령 검색 (국제 업무용) - 영문법령 완전 테스트

### 2-1. 영문 법령 검색 (search_english_law 테스트)
```
외국인 친구에게 한국의 민법에 대해 설명해야 합니다. search_english_law 도구를 사용해서 "Civil Act"로 영문 민법을 검색해주세요. 검색 결과에서 법령ID와 MST 정보를 확인해주세요.
```

### 2-2. 영문 민법 상세 내용
```
위에서 찾은 영문 민법의 상세 내용을 get_english_law_detail 도구로 조회해주세요. 영문 법령의 구조와 조문 정보를 확인해주세요.
```

### 2-3. 영문 민법 종합 요약 (get_english_law_summary 테스트)
```
영문 민법의 전체 내용을 get_english_law_summary 도구로 요약해주세요. 외국인이 한국에서 계약할 때 알아야 할 내용들을 "contract" 키워드로 검색해서 관련 조문들을 찾아주세요.
```

### 2-4. 영문 상법 검색 및 분석
```
한국의 상법도 영어 번역본을 찾아주세요. "Commercial Act"로 search_english_law를 사용해서 검색하고, get_english_law_summary로 요약해주세요. 특히 "company" 키워드로 회사 설립 관련 내용을 찾아주세요.
```

**🔍 2단계 분석 요청:**
```
위 2단계 영문법령 테스트 결과를 분석해주세요:
1. 영문법령 검색 도구들의 정확성과 완성도
2. 한글법령과 영문법령 간의 데이터 일치성
3. 영문 번역 품질과 법률 용어의 적절성
4. 키워드 검색 기능의 효과성
5. 응답 속도와 데이터 구조의 차이점
6. 국제 업무에서의 실용성 평가
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## ⏰ 3단계: 시행일 기준 법령 (언제부터 적용되는지) - 시행일법령 완전 테스트

### 3-1. 최근 시행 법령 검색 (search_effective_law 테스트)
```
최근에 새로 시행된 법령들이 있나요? search_effective_law 도구를 사용해서 2024년에 시행된 법령들을 검색해주세요. status_type=100(시행)으로 설정하고, effective_date_range="20240101~20241231"로 기간을 지정해주세요.
```

### 3-2. 시행일 법령 상세 보기
```
위에서 찾은 최근 시행 법령 중 하나의 상세 내용을 보여주세요. 언제부터 어떤 내용이 바뀌었는지 알고 싶어요.
```

### 3-3. 시행일 법령 조항호목 조회 (get_effective_law_articles 테스트)
```
선택한 시행일 법령의 조문들을 get_effective_law_articles 도구로 조회해주세요. 특정 조문번호를 지정해서 상세 내용을 확인해주세요.
```

### 3-4. 미시행 및 폐지 법령 확인
```
앞으로 시행될 예정인 법령(status_type=200)과 폐지된 법령(status_type=300)도 각각 검색해서 비교해주세요. 법령의 생명주기를 이해할 수 있도록 설명해주세요.
```

**🔍 3단계 분석 요청:**
```
위 3단계 시행일법령 테스트 결과를 분석해주세요:
1. 시행일 기준 검색의 정확성과 유용성
2. 법령 상태별(시행/미시행/폐지) 데이터 품질
3. 시행일 정보의 신뢰성과 최신성
4. 조문별 시행일 정보의 상세성
5. 법령 변경 추적의 용이성
6. 컴플라이언스 업무에서의 실용성
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 📚 4단계: 법령 변경 이력 (법이 어떻게 바뀌었는지) - 연혁 추적 완전 테스트

### 4-1. 도로교통법 연혁 검색 (search_law_history 테스트)
```
도로교통법이 제정된 이후 어떻게 변경되어 왔는지 search_law_history 도구로 연혁을 검색해주세요. 최근 5년간의 주요 개정 사항들을 확인해주세요.
```

### 4-2. 법령 연혁 상세 보기
```
위에서 본 도로교통법 연혁 중 가장 최근 개정 내용을 get_law_history_detail 도구로 자세히 조회해주세요. 구체적인 개정 사유와 내용을 확인해주세요.
```

### 4-3. 일자별 조문 개정 이력 (search_daily_article_revision 테스트)
```
2024년에 개정된 조문들을 search_daily_article_revision 도구로 검색해주세요. 특정 날짜나 법령을 지정해서 어떤 조문이 언제 바뀌었는지 추적해주세요.
```

### 4-4. 조문별 변경 이력 (search_article_change_history 테스트)
```
특정 조문이 시간에 따라 어떻게 변경되었는지 search_article_change_history 도구로 추적해주세요. "제50조" 같은 조문번호로 검색해서 변경 패턴을 분석해주세요.
```

### 4-5. 법령 변경이력 종합 (search_law_change_history 테스트)
```
전체적인 법령 변경 동향을 search_law_change_history 도구로 파악해주세요. 2024년 기준으로 가장 활발하게 개정된 법령들을 찾아주세요.
```

**🔍 4단계 분석 요청:**
```
위 4단계 법령변경이력 테스트 결과를 분석해주세요:
1. 연혁 추적 도구들의 완성도와 정확성
2. 시계열 데이터의 연속성과 일관성
3. 개정 사유와 내용의 상세성
4. 법령 변화 패턴 분석의 유용성
5. 정책 변화 추적의 실효성
6. 법무 실무에서의 활용 가능성
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 📖 5단계: 조문별 세부 검색 (법령의 특정 부분) - 조문 분석 완전 테스트

### 5-1. 법령 조문 목록 조회 (search_law_articles 테스트)
```
도로교통법의 전체 조문 목록을 search_law_articles 도구로 조회해주세요. 조문 구조와 제목들을 파악해서 법령의 전체적인 구성을 이해해주세요.
```

### 5-2. 현행법령 조문 조회 (get_current_law_articles 테스트)
```
도로교통법의 특정 조문들을 get_current_law_articles 도구로 조회해주세요. 제1조부터 제10조까지 연속으로 조회해서 총칙 부분을 분석해주세요.
```

### 5-3. 연속 조문 범위 조회 (get_law_articles_range 테스트)
```
도로교통법의 제50조부터 제60조까지를 get_law_articles_range 도구로 한번에 조회해주세요. 근로시간 관련 조문들의 연관성을 분석해주세요.
```

### 5-4. 의미 기반 조문 검색 (search_law_articles_semantic 테스트)
```
도로교통법에서 "사고처리"와 관련된 조문들을 search_law_articles_semantic 도구로 찾아주세요. 키워드 기반으로 관련 조문들이 정확히 검색되는지 확인해주세요.
```

### 5-5. 부동산 관련 법령 조문 분석
```
공인중개사법의 조문들도 동일한 방식으로 분석해주세요. search_law_articles로 전체 조문을 파악하고, "중개수수료" 관련 조문들을 의미 기반으로 검색해주세요.
```

**🔍 5단계 분석 요청:**
```
위 5단계 조문분석 테스트 결과를 분석해주세요:
1. 조문 검색 도구들의 정확성과 완성도
2. 조문 번호 체계의 일관성과 정확성
3. 의미 기반 검색의 정밀도와 재현율
4. 조문 간 연관성 분석의 유용성
5. 법령 해석 업무에서의 실용성
6. 조문 데이터의 구조화 수준
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 🗂️ 6단계: 법령 체계도 (법령의 구조 파악) - 법령 관계 완전 테스트

### 6-1. 법령 체계도 검색 (search_law_system_diagram 테스트)
```
복잡한 법령의 구조를 파악하기 위해 search_law_system_diagram 도구로 교통 관련 체계도를 검색해주세요. 법령 간의 계층구조를 확인해주세요.
```

### 6-2. 체계도 상세 내용
```
위에서 찾은 체계도의 상세 내용을 보여주세요. 법령들이 어떻게 연결되어 있는지 알고 싶어요.
```

### 6-3. 한눈보기 기능
```
법령을 요약해서 한눈에 볼 수 있는 기능이 있나요? 도로교통법을 한눈보기로 보여주세요.
```

### 6-4. 위임법령 조회 (get_delegated_law 테스트)
```
도로교통법에서 다른 하위 법령에 위임한 내용들을 get_delegated_law 도구로 확인해주세요. 상위법-하위법 관계를 파악해주세요.
```

### 6-5. 관련법령 검색 (search_related_law 테스트)
```
도로교통법과 관련된 다른 법령들을 search_related_law 도구로 찾아주세요. 법령 간의 연관관계와 참조관계를 분석해주세요.
```

**🔍 6단계 분석 요청:**
```
위 6단계 법령구조분석 테스트 결과를 분석해주세요:
1. 법령 체계도의 정확성과 완성도
2. 위임관계 정보의 상세성과 유용성
3. 관련법령 연결의 논리적 타당성
4. 한눈보기 자료의 품질과 실용성
5. 법령 간 관계 파악의 용이성
6. 법체계 이해에 대한 도움 정도
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 🔗 7단계: 법령-자치법규 연계 정보 - 중앙-지방 연결 완전 테스트

### 7-1. 법령-자치법규 연계 검색 (search_law_ordinance_link 테스트)
```
도로교통법과 관련된 지방자치단체의 조례나 규칙을 search_law_ordinance_link 도구로 찾아주세요. 상위 법령이 각 지자체에서 어떻게 구현되는지 확인해주세요.
```

### 7-2. 법령-자치법규 연계 상세 (get_law_ordinance_connection 테스트)
```
위에서 찾은 연계 정보 중 하나를 get_law_ordinance_connection 도구로 상세 조회해주세요. 구체적인 연계 내용과 근거를 확인해주세요.
```

### 7-3. 자치법규-법령 연계 검색 (search_ordinance_law_link 테스트)
```
반대로 특정 자치법규가 어떤 상위 법령에 근거하는지 search_ordinance_law_link 도구로 찾아주세요. "서울특별시" 또는 "주차장 조례" 키워드로 검색해주세요.
```

### 7-4. 연계 자치법규 검색 (search_linked_ordinance 테스트)
```
법령과 연계된 조례를 search_linked_ordinance 도구로 더 자세히 검색해주세요. 특정 법령ID를 사용해서 직접 연결된 자치법규들을 찾아주세요.
```

**🔍 7단계 분석 요청:**
```
위 7단계 법령-자치법규 연계 테스트 결과를 분석해주세요:
1. 중앙법령과 지방법규 간 연계정보의 정확성
2. 연계관계 데이터의 완성도와 최신성
3. 지자체별 법규 구현의 일관성
4. 법령 위임과 조례 제정의 적절성
5. 지방자치 연구에서의 활용 가능성
6. 실무에서 법령-조례 관계 파악의 용이성
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 📋 8단계: 별표와 서식 - 실무 양식 완전 테스트

### 8-1. 법령 별표서식 검색 (search_law_appendix 테스트)
```
법령에 첨부된 별표나 서식들을 search_law_appendix 도구로 검색해주세요. "신청서" 관련 서식들을 찾고, appendix_type=2(서식)으로 필터링해서 검색해주세요.
```

### 8-2. 별표서식 상세 내용
```
위에서 찾은 서식의 상세 내용을 보여주세요. 실제로 어떤 양식인지 알고 싶어요.
```

### 8-3. 자치법규 별표서식 검색 (search_ordinance_appendix 테스트)
```
지방자치단체의 조례와 규칙에 첨부된 별표 및 서식도 search_ordinance_appendix 도구로 검색해주세요. 중앙정부와 지방정부 서식의 차이를 비교해주세요.
```

### 8-4. 자치법규 별표서식 상세 (get_ordinance_appendix_detail 테스트)
```
지방 조례의 서식을 get_ordinance_appendix_detail 도구로 상세 조회해서 실무에서 실제로 사용할 수 있는 양식인지 확인해주세요.
```

**🔍 8단계 분석 요청:**
```
위 8단계 별표서식 테스트 결과를 분석해주세요:
1. 별표서식 검색의 정확성과 완성도
2. 서식 분류 체계의 논리성과 일관성
3. 실무에서 사용 가능한 양식의 품질
4. 중앙정부와 지방정부 서식의 연계성
5. 서식 업데이트의 신속성과 정확성
6. 행정업무 효율화에 대한 기여도
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## ⚖️ 9단계: 신구법 비교 - 개정 전후 비교 완전 테스트

### 9-1. 신구법 비교 검색 (search_old_and_new_law 테스트)
```
법령이 개정될 때 이전 내용과 새로운 내용을 비교할 수 있는 search_old_and_new_law 도구로 교통 관련 신구법 비교 자료를 찾아주세요. 최근 개정된 법령들을 확인해주세요.
```

### 9-2. 3단 비교 검색 (search_three_way_comparison 테스트)
```
상위법령-하위법령-위임조문의 3단계 관계를 비교하는 search_three_way_comparison 도구로 관련 자료를 찾아주세요. 법령 간의 복잡한 관계를 이해해주세요.
```

### 9-3. 법령 버전 비교 (compare_law_versions 테스트)
```
동일 법령의 현행 버전과 시행일 버전을 compare_law_versions 도구로 비교해주세요. "개인정보보호법"이나 "근로기준법"으로 테스트해서 주요 변경사항을 확인해주세요.
```

**🔍 9단계 분석 요청:**
```
위 9단계 신구법비교 테스트 결과를 분석해주세요:
1. 신구법 비교 기능의 정확성과 상세성
2. 변경사항 식별의 정밀도와 완성도
3. 3단 비교의 논리적 타당성과 유용성
4. 법령 버전 관리의 체계성
5. 개정 영향 분석의 실용성
6. 법무 실무에서의 활용 가능성
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 🎯 10단계: 맞춤형 검색 - 사용자 맞춤 완전 테스트

### 10-1. 맞춤형 법령 검색 (search_custom_law 테스트)
```
사용자 맞춤형으로 분류된 법령들을 search_custom_law 도구로 검색해주세요. 일반인이 자주 찾는 법령이나 특정 주제별로 분류된 법령들을 확인해주세요.
```

### 10-2. 맞춤형 법령 조문 검색 (search_custom_law_articles 테스트)
```
위에서 찾은 맞춤형 법령의 조문들도 보여주세요.
```

### 10-3. 맞춤형 자치법규 검색 (search_custom_ordinance 테스트)
```
맞춤형으로 분류된 자치법규를 search_custom_ordinance 도구로 검색해주세요. 시민들이 자주 찾는 조례나 규칙들을 확인해주세요.
```

### 10-4. 맞춤형 자치법규 조문 검색 (search_custom_ordinance_articles 테스트)
```
맞춤형 자치법규의 조문들을 search_custom_ordinance_articles 도구로 검색해주세요. 생활밀착형 조례 조문들을 찾아주세요.
```

### 10-5. 맞춤형 판례 검색 (search_custom_precedent 테스트)
```
맞춤형으로 분류된 판례들을 search_custom_precedent 도구로 검색해주세요. 일반인들이 관심있어 할 판례들을 확인해주세요.
```

**🔍 10단계 분석 요청:**
```
위 10단계 맞춤형검색 테스트 결과를 분석해주세요:
1. 맞춤형 분류 체계의 논리성과 실용성
2. 사용자 관점에서의 접근성과 편의성
3. 분류 기준의 일관성과 적절성
4. 일반인 대상 법령 서비스의 품질
5. 맞춤형 검색의 정확성과 유용성
6. 법령 대중화에 대한 기여도
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 🏷️ 11단계: 기타 유용한 기능들 - 특수 기능 완전 테스트

### 11-1. 법령 약칭 검색 (search_law_nickname 테스트)
```
법령들의 줄임말이나 약칭을 search_law_nickname 도구로 검색해주세요. 2024년에 등록된 약칭들과 전체 약칭 목록을 확인해주세요.
```

### 11-2. 삭제된 법령 데이터 검색 (search_deleted_law_data 테스트)
```
과거에 있다가 폐지된 법령들의 정보를 search_deleted_law_data 도구로 검색해주세요. 데이터 타입별로 삭제된 정보들을 확인해주세요.
```

### 11-3. 삭제 이력 검색 (search_deleted_history 테스트)
```
법령 데이터의 삭제 이력을 search_deleted_history 도구로 확인해주세요. 2024년 관련 삭제 이력을 추적해주세요.
```

**🔍 11단계 분석 요청:**
```
위 11단계 특수기능 테스트 결과를 분석해주세요:
1. 법령 약칭 관리의 체계성과 유용성
2. 삭제 데이터 추적의 정확성과 완성도
3. 데이터 무결성 관리의 신뢰성
4. 이력 관리 시스템의 투명성
5. 감사 추적 기능의 실효성
6. 데이터 거버넌스 관점에서의 품질
보수적으로 평가하고 개선점을 제시해주세요.
```

---

## 🚀 12단계: 실제 생활 시나리오 (종합 테스트) - 실무 워크플로우 완전 테스트

### 12-1. 운전면허 취득 시나리오 (종합 워크플로우)
```
운전면허를 취득하려고 합니다. 다음 워크플로우로 종합적으로 테스트해주세요:
1. search_law_unified로 "도로교통법" 관련 법령들 탐색
2. get_law_summary로 도로교통법 전체 요약
3. get_law_article_by_key로 운전면허(제80조) 상세 조회
4. search_law_appendix로 운전면허 관련 서식 찾기
5. search_administrative_rule로 운전면허 관련 행정규칙 확인
6. search_local_ordinance로 지역별 교통 관련 조례 확인
7. search_faq로 운전면허 관련 자주 묻는 질문 확인

전체 과정의 연결성과 실용성을 평가해주세요.
```

### 12-2. 부동산 거래 시나리오 (종합 워크플로우)
```
집을 구매하려고 합니다. 다음 워크플로우로 종합적으로 테스트해주세요:
1. search_law_unified로 "부동산" 관련 법령들 탐색
2. get_law_summary로 공인중개사법 전체 요약
3. get_law_article_by_key로 중개수수료(제32조) 상세 조회
4. search_precedent로 부동산 거래 관련 판례 검색
5. search_legal_term으로 "계약" 용어 정의 확인
6. search_counsel로 부동산 거래 상담 사례 확인
7. search_law_appendix로 부동산 계약 관련 서식 찾기

전체 과정의 완성도와 실무 적용 가능성을 평가해주세요.
```

### 12-3. 온라인 쇼핑몰 창업 시나리오 (종합 워크플로우)
```
온라인 쇼핑몰을 창업하려고 합니다. 다음 워크플로우로 종합적으로 테스트해주세요:
1. search_law_unified로 "개인정보보호법" 검색
2. get_law_summary로 개인정보보호법 전체 요약 (키워드: "온라인 쇼핑몰")
3. search_legal_ai로 "전자상거래" 관련 모든 법적 문서 검색
4. search_moef_interpretation으로 사업자등록 관련 해석례 확인
5. search_custom_law로 중소기업 지원 관련 맞춤 법령 확인
6. search_knowledge_base로 창업 관련 종합 정보 확인
7. search_faq로 창업 관련 자주 묻는 질문 확인

창업 지원 정보의 종합성과 실용성을 평가해주세요.
```

### 12-4. 직장인 권리 보호 시나리오 (종합 워크플로우)
```
직장에서 부당한 대우를 받고 있는 것 같습니다. 다음 워크플로우로 종합적으로 테스트해주세요:
1. search_law_unified로 "근로기준법" 검색
2. get_law_summary로 근로기준법 전체 요약 (키워드: "근로시간 야근수당")
3. search_labor_committee로 노동위원회 결정문 검색
4. search_moel_interpretation으로 고용노동부 해석례 확인
5. search_precedent로 노동 관련 판례 검색
6. search_counsel로 노동 상담 사례 확인
7. search_civil_petition으로 노동 관련 민원 처리 현황 확인

근로자 권리 보호 정보의 접근성과 실효성을 평가해주세요.
```

**🔍 12단계 분석 요청:**
```
위 12단계 실생활시나리오 테스트 결과를 종합 분석해주세요:
1. 각 시나리오별 워크플로우의 논리성과 완성도
2. 도구 간 연계성과 정보의 일관성
3. 실제 생활 문제 해결에 대한 기여도
4. 일반인이 따라하기 쉬운 정도
5. 법령 정보의 실용성과 접근성
6. 전체 시스템의 사용자 친화성
7. 각 시나리오에서 부족한 정보나 기능
8. 실무 활용 시 예상되는 장벽과 한계
보수적으로 평가하고 전체적인 개선 방향을 제시해주세요.
```

---

## 🎓 13단계: 고급 기능 테스트

### 13-1. 조문별 상세 분석
```
도로교통법의 제1조부터 제10조까지 각 조문의 내용을 상세히 분석해주세요.
```

### 13-2. 법령 간 관계 분석
```
도로교통법, 자동차관리법, 교통사고처리법이 서로 어떻게 연관되어 있는지 관계를 분석해주세요.
```

### 13-3. 시계열 변화 추적
```
교통 관련 법령들이 지난 10년간 어떻게 변화해왔는지 시계열로 추적해주세요.
```

---

## ✅ 완전 테스트 체크리스트

다음 모든 도구들을 테스트했는지 확인하세요:

### 🔍 기본 법령 도구들 (law_tools.py)
- [ ] search_law_unified - 통합 법령 검색
- [ ] search_law - 정밀 법령 검색  
- [ ] get_law_summary - 법령 요약 (최우선)
- [ ] get_law_detail_unified - 법령 상세 조회
- [ ] get_law_article_by_key - 특정 조문 조회
- [ ] get_law_articles_range - 연속 조문 조회
- [ ] search_law_articles - 조문 목록 검색
- [ ] search_law_articles_semantic - 의미 기반 조문 검색
- [ ] get_current_law_articles - 현행법 조문 조회
- [ ] compare_law_versions - 법령 버전 비교

### 🌍 영문 법령 도구들
- [ ] search_english_law - 영문 법령 검색
- [ ] get_english_law_detail - 영문 법령 상세
- [ ] get_english_law_summary - 영문 법령 요약 (최우선)
- [ ] search_english_law_articles_semantic - 영문 조문 검색

### ⏰ 시행일 법령 도구들
- [ ] search_effective_law - 시행일 법령 검색
- [ ] get_effective_law_detail - 시행일 법령 상세
- [ ] get_effective_law_articles - 시행일 법령 조문

### 📚 법령 연혁 도구들
- [ ] search_law_history - 법령 연혁 검색
- [ ] get_law_history_detail - 연혁 상세 조회
- [ ] search_law_change_history - 변경 이력 검색
- [ ] search_daily_article_revision - 일자별 조문 개정
- [ ] search_article_change_history - 조문별 변경 이력

### 🗂️ 법령 구조 도구들
- [ ] search_law_system_diagram - 법령 체계도 검색
- [ ] get_law_system_diagram_detail - 체계도 상세
- [ ] get_delegated_law - 위임법령 조회
- [ ] search_one_view - 한눈보기 검색
- [ ] search_related_law - 관련법령 검색

### 🔗 연계 정보 도구들
- [ ] search_law_ordinance_link - 법령-자치법규 연계
- [ ] get_law_ordinance_connection - 연계 상세
- [ ] search_ordinance_law_link - 자치법규-법령 연계

### 📋 별표서식 도구들
- [ ] search_law_appendix - 법령 별표서식 검색
- [ ] get_law_appendix_detail - 별표서식 상세

### ⚖️ 비교 도구들
- [ ] search_old_and_new_law - 신구법 비교
- [ ] search_three_way_comparison - 3단 비교

### 🎯 맞춤형 도구들 (custom_tools.py)
- [ ] search_custom_law - 맞춤형 법령 검색
- [ ] search_custom_law_articles - 맞춤형 법령 조문
- [ ] search_custom_ordinance - 맞춤형 자치법규
- [ ] search_custom_ordinance_articles - 맞춤형 자치법규 조문
- [ ] search_custom_precedent - 맞춤형 판례

### 🏷️ 기타 유용한 도구들
- [ ] search_law_nickname - 법령 약칭 검색
- [ ] search_deleted_law_data - 삭제된 법령 데이터
- [ ] search_deleted_history - 삭제 이력

### 🧠 AI 기반 도구들
- [ ] search_legal_ai - AI 기반 종합 법률 검색
- [ ] search_all_legal_documents - 통합 법적 문서 검색

### 📚 판례 도구들 (precedent_tools.py)
- [ ] search_precedent - 대법원 판례 검색
- [ ] get_precedent_detail - 판례 상세 조회
- [ ] search_interpretation - 해석례 검색
- [ ] get_interpretation_detail - 해석례 상세

### 🏛️ 위원회 결정문 도구들 (committee_tools.py)
- [ ] search_privacy_committee + get_privacy_committee_detail
- [ ] search_financial_committee + get_financial_committee_detail
- [ ] search_monopoly_committee + get_monopoly_committee_detail
- [ ] search_anticorruption_committee + get_anticorruption_committee_detail
- [ ] search_labor_committee + get_labor_committee_detail
- [ ] search_environment_committee + get_environment_committee_detail
- [ ] search_securities_committee + get_securities_committee_detail
- [ ] search_human_rights_committee + get_human_rights_committee_detail
- [ ] search_broadcasting_committee + get_broadcasting_committee_detail
- [ ] search_industrial_accident_committee + get_industrial_accident_committee_detail
- [ ] search_land_tribunal + get_land_tribunal_detail
- [ ] search_employment_insurance_committee + get_employment_insurance_committee_detail

### 🏢 부처별 해석례 도구들 (ministry_interpretation_tools.py)
- [ ] search_moef_interpretation + get_moef_interpretation_detail (기획재정부)
- [ ] search_molit_interpretation (국토교통부)
- [ ] search_moel_interpretation (고용노동부)
- [ ] search_mof_interpretation (해양수산부)
- [ ] search_mohw_interpretation (보건복지부)
- [ ] search_moe_interpretation (교육부)
- [ ] search_korea_interpretation (한국)
- [ ] search_mssp_interpretation (보훈처)
- [ ] search_mote_interpretation (산업통상자원부)
- [ ] search_maf_interpretation (농림축산식품부)
- [ ] search_moms_interpretation (국방부)
- [ ] search_sme_interpretation (중소벤처기업부)
- [ ] search_nfa_interpretation (산림청)
- [ ] search_korail_interpretation (한국철도공사)
- [ ] search_nts_interpretation + get_nts_interpretation_detail (국세청)
- [ ] search_kcs_interpretation + get_kcs_interpretation_detail (관세청)

### 🔗 법령용어 도구들 (legal_term_tools.py)
- [ ] search_legal_term + get_legal_term_detail
- [ ] search_legal_term_ai
- [ ] search_daily_legal_term_link
- [ ] search_legal_term_article_link
- [ ] search_article_legal_term_link

### 🔗 연계 도구들 (linkage_tools.py)
- [ ] search_daily_term
- [ ] search_legal_daily_term_link

### 🏛️ 행정규칙 도구들 (administrative_rule_tools.py)
- [ ] search_administrative_rule + get_administrative_rule_detail
- [ ] search_administrative_rule_comparison + get_administrative_rule_comparison_detail
- [ ] search_local_ordinance + get_local_ordinance_detail
- [ ] search_ordinance_appendix + get_ordinance_appendix_detail
- [ ] search_linked_ordinance

### 🌐 전문화 도구들 (specialized_tools.py)
- [ ] search_treaty + get_treaty_detail
- [ ] search_university_regulation

### 📞 추가 서비스 도구들 (additional_service_tools.py)
- [ ] search_knowledge_base
- [ ] search_faq
- [ ] search_qna
- [ ] search_counsel
- [ ] search_precedent_counsel
- [ ] search_civil_petition

### 🔧 기타 도구들 (misc_tools.py)
- [ ] get_ordinance_detail
- [ ] get_treaty_detail
- [ ] get_ordinance_appendix_detail

---

## 💡 디버깅 및 분석 가이드

### �� 각 단계별 체크포인트
1. **도구 호출 성공 여부** - MCP 도구가 정상적으로 호출되었는가?
2. **응답 데이터 품질** - 반환된 데이터가 완전하고 정확한가?
3. **오류 처리** - 오류 발생 시 적절한 메시지가 표시되는가?
4. **응답 시간** - 합리적인 시간 내에 응답이 오는가?
5. **데이터 일관성** - 관련 도구들 간 데이터가 일치하는가?
6. **워크플로우 연결성** - 단계별 작업이 자연스럽게 연결되는가?

### ⚠️ 주의 깊게 평가할 부분
- 검색 결과가 없거나 불완전한 경우
- 도구 간 데이터 불일치
- 예상과 다른 검색 결과
- 응답 시간이 과도하게 긴 경우
- 오류 메시지가 불친절하거나 부정확한 경우
- 실무에서 활용하기 어려운 데이터 구조

### 📊 종합 평가 기준
1. **기능적 완성도** (30%) - 모든 도구가 정상 작동하는가?
2. **데이터 품질** (25%) - 제공되는 정보가 정확하고 유용한가?
3. **사용자 경험** (20%) - 일반인도 쉽게 사용할 수 있는가?
4. **실무 활용성** (15%) - 실제 업무에서 도움이 되는가?
5. **시스템 성능** (10%) - 응답 속도와 안정성은 적절한가?

이 완전한 테스트 가이드를 통해 한국 법제처의 모든 법령 관련 도구를 체험하고, 시스템의 강점과 개선점을 정확히 파악해보세요! 🎉 
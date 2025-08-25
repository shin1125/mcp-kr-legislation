# 한국 법제처 OPEN API 상세 가이드

> 총 125개의 API 문서화 (모바일 API 제외 후 105개)
> 생성일: 2025. 7. 22.
> 업데이트: 2025. 1. 15. - API 구조 분석 추가
> 모든 Request/Response 정보 포함

## API 구조 패턴

### 핵심 URL 패턴
| 기능 | URL 패턴 | 설명 | 예시 |
|------|-----------|------|------|
| **목록 조회** | `lawSearch.do?target={value}` | 검색/목록 반환 | `lawSearch.do?target=law` |
| **본문 조회** | `lawService.do?target={value}` | 상세 내용 반환 | `lawService.do?target=law` |

### target 파라미터가 기능 결정
- 동일한 URL에서 `target` 값만으로 API 카테고리 구분
- 총 **50개 이상**의 고유한 target 값 존재
- 목록/본문 조회는 URL로, 카테고리는 target으로 결정

## API 카테고리별 구분표

| 대분류 | 중분류 | 목록 조회 API | target | 본문 조회 API | target | 목록 조회 도구 | 본문/상세 조회 도구 |
|--------|--------|---------------|--------|---------------|--------|------------|---------------|
| **법령** | **본문** | 현행법령 목록 조회 | `law` | 현행법령 본문 조회 | `law` | `search_law` | `get_law_detail` (통합) |
| | | 시행일 법령 목록 조회 | `eflaw` | 시행일 법령 본문 조회 | `eflaw` | `search_effective_law` | `get_effective_law_detail` |
| | **통합검색** | 범용 법령 통합 검색 | `다중` | - | - | `search_law_unified` | - |
| | **조항호목** | - | - | 현행법령 본문 조항호목 조회 | `lawjosub` | - | `get_current_law_articles`, `search_law_articles` |
| | | - | - | 시행일 법령 본문 조항호목 조회 | `eflawjosub` | - | `get_effective_law_articles` |
| | **영문법령** | 영문 법령 목록 조회 | `elaw` | 영문 법령 본문 조회 | `elaw` | `search_english_law` | `get_english_law_detail` |
| | **이력** | 법령 변경이력 목록 조회 | `lsHstInf` | - | - | `search_law_change_history` | - |
| | | 일자별 조문 개정 이력 목록 조회 | `lsJoHstInf` | - | - | `search_daily_article_revision` | - |
| | | 조문별 변경 이력 목록 조회 | `lsJoHstInf` | - | - | `search_article_change_history` | - |
| | **연계** | 법령 기준 자치법규 연계 관련 목록 조회 | `lnkLs` | - | - | `search_law_ordinance_link` | - |
| | | - | - | 위임법령 조회 | `lsDelegated` | - | `get_delegated_law` |
| | **부가서비스** | 법령 체계도 목록 조회 | `lsStmd` | 법령 체계도 본문 조회 | `lsStmd` | `search_law_system_diagram` | `get_law_system_diagram_detail` |
| | | 신구법 목록 조회 | `oldAndNew` | 신구법 본문 조회 | `oldAndNew` | `search_old_and_new_law` | `get_old_and_new_law_detail` |
| | | 3단 비교 목록 조회 | `thdCmp` | 3단 비교 본문 조회 | `thdCmp` | `search_three_way_comparison` | `get_three_way_comparison_detail` |
| | | 법률명 약칭 조회 | `lsAbrv` | - | - | `search_law_nickname` | - |
| | | 삭제 데이터 목록 조회 | `datDel` | - | - | `search_deleted_law_data` | - |
| | | 한눈보기 목록 조회 | `oneview` | 한눈보기 본문 조회 | `oneview` | `search_one_view` | `get_one_view_detail` |
| | | 별표·서식 목록 조회 | `licbyl` | - | - | `search_law_appendix` | `get_law_appendix_detail` |
| **행정규칙** | **본문** | 행정규칙 목록 조회 | `admrul` | 행정규칙 본문 조회 | `admrul` | `search_administrative_rule` | `get_administrative_rule_detail` |
| | **부가서비스** | 행정규칙 신구법 비교 목록 조회 | `admrulOldAndNew` | 행정규칙 신구법 비교 본문 조회 | `admrulOldAndNew` | `search_administrative_rule_comparison` | `get_administrative_rule_comparison_detail` |
| | | 별표·서식 목록 조회 | `admbyl` | - | - | `search_administrative_rule_appendix` | `get_administrative_rule_appendix_detail` |
| **자치법규** | **본문** | 자치법규 목록 조회 | `ordinfd` | 자치법규 본문 조회 | `ordin` | `search_local_ordinance` | `get_local_ordinance_detail`, `get_ordinance_detail` |
| | **연계** | 자치법규 기준 법령 연계 관련 목록 조회 | `lnkOrd` | - | - | `search_linked_ordinance` | - |
| | | 별표·서식 목록 조회 | `ordinbyl` | - | - | `search_ordinance_appendix` | `get_ordinance_appendix_detail` |
| **판례관련** | **판례** | 판례 목록 조회 | `prec` | 판례 본문 조회 | `prec` | `search_precedent` | `get_precedent_detail` |
| | **헌재결정례** | 헌재결정례 목록 조회 | `detc` | 헌재결정례 본문 조회 | `detc` | `search_constitutional_court` | `get_constitutional_court_detail` |
| | **법령해석례** | 법령해석례 목록 조회 | `expc` | 법령해석례 본문 조회 | `expc` | `search_legal_interpretation` | `get_legal_interpretation_detail` |
| | **행정심판례** | 행정심판례 목록 조회 | `decc` | 행정심판례 본문 조회 | `decc` | `search_administrative_trial` | `get_administrative_trial_detail` |
| **위원회결정문** | **개인정보보호위원회** | 개인정보보호위원회 결정문 목록 조회 | `ppc` | 개인정보보호위원회 결정문 본문 조회 | `ppc` | `search_privacy_committee` | `get_privacy_committee_detail` |
| | **고용보험심사위원회** | 고용보험심사위원회 결정문 목록 조회 | `eiac` | 고용보험심사위원회 결정문 본문 조회 | `eiac` | `search_employment_insurance_committee` | `get_employment_insurance_committee_detail` |
| | **공정거래위원회** | 공정거래위원회 결정문 목록 조회 | `ftc` | 공정거래위원회 결정문 본문 조회 | `ftc` | `search_monopoly_committee` | `get_monopoly_committee_detail` |
| | **국민권익위원회** | 국민권익위원회 결정문 목록 조회 | `acr` | 국민권익위원회 결정문 본문 조회 | `acr` | `search_anticorruption_committee` | `get_anticorruption_committee_detail` |
| | **금융위원회** | 금융위원회 결정문 목록 조회 | `fsc` | 금융위원회 결정문 본문 조회 | `fsc` | `search_financial_committee` | `get_financial_committee_detail` |
| | **노동위원회** | 노동위원회 결정문 목록 조회 | `nlrc` | 노동위원회 결정문 본문 조회 | `nlrc` | `search_labor_committee` | `get_labor_committee_detail` |
| | **방송통신위원회** | 방송통신위원회 결정문 목록 조회 | `kcc` | 방송통신위원회 결정문 본문 조회 | `kcc` | `search_broadcasting_committee` | `get_broadcasting_committee_detail` |
| | **산업재해보상보험재심사위원회** | 산업재해보상보험재심사위원회 결정문 목록 조회 | `iaciac` | 산업재해보상보험재심사위원회 결정문 본문 조회 | `iaciac` | `search_industrial_accident_committee` | `get_industrial_accident_committee_detail` |
| | **중앙토지수용위원회** | 중앙토지수용위원회 결정문 목록 조회 | `oclt` | 중앙토지수용위원회 결정문 본문 조회 | `oclt` | `search_land_tribunal` | `get_land_tribunal_detail` |
| | **중앙환경분쟁조정위원회** | 중앙환경분쟁조정위원회 결정문 목록 조회 | `ecc` | 중앙환경분쟁조정위원회 결정문 본문 조회 | `ecc` | `search_environment_committee` | `get_environment_committee_detail` |
| | **증권선물위원회** | 증권선물위원회 결정문 목록 조회 | `sfc` | 증권선물위원회 결정문 본문 조회 | `sfc` | `search_securities_committee` | `get_securities_committee_detail` |
| | **국가인권위원회** | 국가인권위원회 결정문 목록 조회 | `nhrck` | 국가인권위원회 결정문 본문 조회 | `nhrck` | `search_human_rights_committee` | `get_human_rights_committee_detail` |
| **조약** | **본문** | 조약 목록 조회 | `trty` | 조약 본문 조회 | `trty` | `search_treaty` | `get_treaty_detail` |
| **학칙·공단·공공기관** | **학칙** | 학칙 목록 조회 | `pi` | 학칙 본문 조회 | `pi` | `search_university_regulation` | `get_university_regulation_detail` |
| | **공단** | 공단 목록 조회 | `pi` | 공단 본문 조회 | `pi` | `search_public_corporation_regulation` | `get_public_corporation_regulation_detail` |
| | **공공기관** | 공공기관 목록 조회 | `pi` | 공공기관 본문 조회 | `pi` | `search_public_institution_regulation` | `get_public_institution_regulation_detail` |
| **법령용어** | **본문** | 법령 용어 목록 조회 | `lstrm` | 법령 용어 본문 조회 | `lstrm` | `search_legal_term` | `get_legal_term_detail` |
| **맞춤형** | **법령** | 맞춤형 법령 목록 조회 | `couseLs` | - | - | `search_custom_law` | - |
| | | 맞춤형 법령 조문 목록 조회 | `couseLs` | - | - | `search_custom_law_articles` | - |
| | **행정규칙** | 맞춤형 행정규칙 목록 조회 | `couseAdmrul` | - | - | `search_custom_administrative_rule` | - |
| | | 맞춤형 행정규칙 조문 목록 조회 | `couseAdmrul` | - | - | `search_custom_administrative_rule_articles` | - |
| | **자치법규** | 맞춤형 자치법규 목록 조회 | `couseOrdin` | - | - | `search_custom_ordinance` | - |
| | | 맞춤형 자치법규 조문 목록 조회 | `couseOrdin` | - | - | `search_custom_ordinance_articles` | - |
| **법령정보 지식베이스** | **용어** | 법령용어 조회 | `lstrmAI` | | | `search_legal_term_ai` | - |
| | | 일상용어 조회 | `dlytrm` | | | `search_daily_term` | - |
| | **용어 간 관계** | 법령용어-일상용어 연계 조회 | `lstrmRlt` | | | `search_legal_daily_term_link` | - |
| | | 일상용어-법령용어 연계 조회 | `dlytrmRlt` | | | `search_daily_legal_term_link` | - |
| | **조문 간 관계** | 법령용어-조문 연계 조회 | `lstrmRltJo` | | | `search_legal_term_article_link` | - |
| | | 조문-법령용어 연계 조회 | `joRltLstrm` | | | `search_article_legal_term_link` | - |
| | **법령 간 관계** | 관련법령 조회 | `lsRlt` | | | `search_related_law` | - |
| **중앙부처 1차 해석** | **고용노동부** | 고용노동부 법령해석 목록 조회 | `moelCgmExpc` | 고용노동부 법령해석 본문 조회 | `moelCgmExpc` | `search_moel_interpretation` | `get_moel_interpretation_detail` |
| | **국토교통부** | 국토교통부 법령해석 목록 조회 | `molitCgmExpc` | 국토교통부 법령해석 본문 조회 | `molitCgmExpc` | `search_molit_interpretation` | `get_molit_interpretation_detail` |
| | **기획재정부** | 기획재정부 법령해석 목록 조회 | `moefCgmExpc` | - | - | `search_moef_interpretation` | `get_moef_interpretation_detail` |
| | **해양수산부** | 해양수산부 법령해석 목록 조회 | `mofCgmExpc` | 해양수산부 법령해석 본문 조회 | `mofCgmExpc` | `search_mof_interpretation` | `get_mof_interpretation_detail` |
| | **행정안전부** | 행정안전부 법령해석 목록 조회 | `moisCgmExpc` | 행정안전부 법령해석 본문 조회 | `moisCgmExpc` | `search_mois_interpretation` | `get_mois_interpretation_detail` |
| | **환경부** | 환경부 법령해석 목록 조회 | `meCgmExpc` | 환경부 법령해석 본문 조회 | `meCgmExpc` | `search_me_interpretation` | `get_me_interpretation_detail` |
| | **관세청** | 관세청 법령해석 목록 조회 | `kcsCgmExpc` | 관세청 법령해석 본문 조회 | `kcsCgmExpc` | `search_kcs_interpretation` | `get_kcs_interpretation_detail` |
| | **국세청** | 국세청 법령해석 목록 조회 | `ntsCgmExpc` | - | - | `search_nts_interpretation` | `get_nts_interpretation_detail` |
| **특별행정심판** | **조세심판원** | 조세심판원 특별행정심판례 목록 조회 | `ttSpecialDecc` | 조세심판원 특별행정심판례 본문 조회 | `ttSpecialDecc` | `search_tax_tribunal` | `get_tax_tribunal_detail` |
| | **해양안전심판원** | 해양안전심판원 특별행정심판례 목록 조회 | `kmstSpecialDecc` | 해양안전심판원 특별행정심판례 본문 조회 | `kmstSpecialDecc` | `search_maritime_safety_tribunal` | `get_maritime_safety_tribunal_detail` |

### 카테고리별 통계

| 대분류 | API 수 | 목록 조회 도구 | 본문/상세 조회 도구 | 총 도구 수 |
|--------|--------|-------------|----------------|---------|
| **법령** | 27개 | 14개 | 13개 | 27개 |
| **행정규칙** | 5개 | 3개 | 3개 | 6개 |
| **자치법규** | 4개 | 3개 | 3개 | 6개 |
| **판례관련** | 8개 | 4개 | 4개 | 8개 |
| **위원회결정문** | 24개 | 12개 | 12개 | 24개 |
| **조약** | 2개 | 1개 | 1개 | 2개 |
| **학칙·공단·공공기관** | 2개 | 3개 | 3개 | 6개 |
| **법령용어** | 2개 | 1개 | 1개 | 2개 |
| **맞춤형** | 6개 | 6개 | 0개 | 6개 |
| **법령정보 지식베이스** | 7개 | 7개 | 0개 | 7개 |
| **중앙부처 1차 해석** | 14개 | 8개 | 8개 | 16개 |
| **특별행정심판** | 4개 | 2개 | 2개 | 4개 |

**총 105개 API → 114개 도구** (일부 API는 여러 도구로 분할 구현)

### 추가 도구 분류

| 분류 | 도구명 | 목적 | 파일 위치 |
|------|--------|------|----------|
| **최적화 도구** | `get_law_summary` | 법령 요약 조회 (캐싱 최적화) | optimized_law_tools.py |
| | `get_law_articles_summary` | 법령 조문 요약 (성능 최적화) | optimized_law_tools.py |
| | `get_law_article_detail` | 단일 조문 상세 조회 | optimized_law_tools.py |
| | `search_law_with_cache` | 캐시 기반 법령 검색 | optimized_law_tools.py |
| **AI/스마트 도구** | `search_legal_ai` | AI 기반 법령 검색 | ai_tools.py |
| | `search_law_articles_semantic` | 의미론적 조문 검색 | law_tools.py |
| | `search_english_law_articles_semantic` | 영문법령 의미론적 검색 | law_tools.py |
| **부가 서비스** | `search_knowledge_base` | 법령 지식베이스 검색 | additional_service_tools.py |
| | `search_faq` | 자주묻는질문 검색 | additional_service_tools.py |
| | `search_qna` | 질의응답 검색 | additional_service_tools.py |
| | `search_counsel` | 법령상담 검색 | additional_service_tools.py |
| | `search_precedent_counsel` | 판례상담 검색 | additional_service_tools.py |
| | `search_civil_petition` | 민원사례 검색 | additional_service_tools.py |
| ** 분석/비교 도구** | `compare_law_versions` | 법령 버전 비교 분석 | law_tools.py |
| | `compare_article_before_after` | 조문 개정 전후 비교 | law_tools.py |
| **🏢 실무 가이드** | `get_practical_law_guide` | 실무 가이드 제공 | law_tools.py |
| | `search_financial_laws` | 금융법령 통합 검색 | law_tools.py |
| | `search_tax_laws` | 세법 통합 검색 | law_tools.py |
| | `search_privacy_laws` | 개인정보보호법령 통합 검색 | law_tools.py |
| ** 통합 검색** | `search_all_legal_documents` | 전체 법령문서 통합 검색 | legislation_tools.py |

**총 134개 도구** = 114개 (API 매핑) + 20개 (추가 기능)

#### ** 추가 도구 사용 시나리오**

** 최적화 도구 활용**
```
# 성능이 중요한 경우
get_law_summary(law_id) - 캐시된 요약 정보로 빠른 조회
search_law_with_cache(query) - 반복 검색 시 성능 향상
```

**AI/스마트 도구 활용**
```
# 자연어 기반 검색
search_legal_ai(query="계약 해지 조건은?")
search_law_articles_semantic(query="부당해고 관련 조문")
```

**부가 서비스 활용**
```
# 실무 지원
search_counsel(query="계약서 작성") - 법령상담 사례
search_faq(query="개인정보처리방침") - 자주묻는질문
search_civil_petition(query="소비자분쟁") - 민원처리 사례
```

** 분석/비교 도구 활용**
```
# 법령 변화 추적
compare_law_versions(law_name="개인정보보호법")
compare_article_before_after(law_name="근로기준법", article_no="25")
```

**🏢 실무 가이드 활용**
```
# 분야별 통합 조회
search_financial_laws(query="가상화폐") - 금융 관련 법령 통합
search_privacy_laws(query="CCTV") - 개인정보 관련 법령 통합
get_practical_law_guide(law_name="전자상거래법") - 실무 가이드
```

###  **연결된 도구 워크플로우**

#### **기본 2단계 워크플로우**
```
1️⃣ 목록 조회 (search_*) → 2️⃣ 상세 조회 (get_*_detail)
```

#### **주요 워크플로우 예시**

** 법령 검색 플로우**
```
search_law(query="민법") 
→ 결과에서 ID 선택 
→ get_law_detail(law_id) 또는 get_current_law_articles(law_id)
```

** 판례 검색 플로우**
```
search_precedent(query="계약") 
→ 결과에서 사건번호 선택 
→ get_precedent_detail(case_id)
```

** 위원회결정문 검색 플로우**
```
search_privacy_committee(query="개인정보") 
→ 결과에서 결정문번호 선택 
→ get_privacy_committee_detail(decision_id)
```

** 영문법령 검색 플로우**
```
search_english_law(query="Civil Act") 
→ 결과에서 법령ID 선택 
→ get_english_law_detail(law_id)
```

#### **특수 워크플로우**

** 연계 조회 플로우**
```
search_law_ordinance_link() → get_local_ordinance_detail(ordinance_id)
```

** 비교 분석 플로우**
```
search_old_and_new_law() → get_old_and_new_law_detail(comparison_id)
search_three_way_comparison() → get_three_way_comparison_detail(comparison_id)
```

**별표서식 플로우**
```
search_law_appendix() → get_law_appendix_detail(appendix_id)
search_ordinance_appendix() → get_ordinance_appendix_detail(appendix_id)
```

###  **도구 사용 가이드라인**

#### ** 목록 조회 도구 (`search_*`) 사용법**
- **목적**: 여러 건의 결과를 빠르게 검색
- **반환**: 목록 형태의 요약 정보 (제목, ID, 요약 등)
- **다음 단계**: 관심 있는 항목의 ID를 사용해 상세 조회

#### **🔍 상세 조회 도구 (`get_*_detail`) 사용법**
- **목적**: 특정 문서의 전체 내용 조회
- **입력**: 목록 조회에서 얻은 ID
- **반환**: 해당 문서의 한 내용

#### **⚡ 성능 최적화 팁**
1. **단계적 접근**: 목록 조회 → 필요한 것만 상세 조회
2. **적절한 페이징**: `display`와 `page` 파라미터 활용
3. **구체적 검색어**: 너무 일반적인 용어보다는 구체적인 키워드 사용

#### ** 도구 선택 가이드**

**법령 관련 작업**
- 현행법령: `search_law` → `get_law_detail`
- 시행일별 법령: `search_effective_law` → `get_effective_law_detail`
- 영문법령: `search_english_law` → `get_english_law_detail`
- 법령 조문: `get_current_law_articles` (직접 조회)

**판례 관련 작업**
- 일반 판례: `search_precedent` → `get_precedent_detail`
- 헌법재판소: `search_constitutional_court` → `get_constitutional_court_detail`
- 행정심판: `search_administrative_trial` → `get_administrative_trial_detail`

**위원회 결정문**
- 각 위원회별 전용 도구 사용 (총 12개 위원회)
- 예: `search_privacy_committee` → `get_privacy_committee_detail`

**부처별 해석**
- 각 부처별 전용 도구 사용 (총 8개 부처)
- 예: `search_moel_interpretation` → `get_moel_interpretation_detail`

###  **중요한 발견사항**

1. **한 도구 생태계 구축**: 
   - **134개 도구** = 105개 API  매핑 + 29개 추가 기능
   - API 외 도구들로 실무 활용도 대폭 향상

2. **계층화된 도구 구조**:
   - **기본 레이어**: API 직접 매핑 (114개)
   - **최적화 레이어**: 성능/캐싱 도구 (4개)
   - **지능화 레이어**: AI/스마트 검색 (3개)
   - **실무 레이어**: 분석/가이드 도구 (13개)

3. **API-도구 매핑 성**: 
   - 105개 API → 114개 도구로  매핑
   - 일부 API는 여러 도구로 분할 구현 (예: 학칙·공단·공공기관)
   - 목록 조회와 상세 조회의 명확한 분리

4. **다양한 사용자 요구 대응**:
   - **개발자**: API 직접 매핑 도구
   - **연구자**: AI/의미론적 검색 도구  
   - **실무자**: 분야별 통합 검색, 실무 가이드
   - **일반인**: FAQ, 상담사례, 민원사례

5. **API 구조의 일관성**:
   - 모든 API가 동일한 URL 패턴 사용
   - `target` 파라미터만으로 기능 구분
   - 총 **50개 이상**의 고유한 target 값

6. **성능 최적화 전략**:
   - 캐싱 시스템 적용 (`search_law_with_cache`)
   - 요약 정보 우선 제공 (`get_law_summary`)
   - 단계적 상세 조회 패턴

7. **실무 중심 설계**:
   - 분야별 통합 검색 (금융법, 세법, 개인정보법)
   - 비교/분석 도구 (법령 버전 비교, 조문 변화 추적)
   - 실무 가이드 제공 (체크리스트, 절차 안내)

###  **개선 계획**

#### **Phase 1: 법령 카테고리 우선 개선**
-  현행법령 - 목록/본문 분리
-  시행일법령 - 목록/본문 분리  
-  법령연혁 - 목록/본문 분리
-  영문법령 - 목록/본문 분리

#### **Phase 2: 통합 함수 도입**
```python
# 기존: 4개 개별 함수
def search_law(query): # target=law
def search_effective_law(query): # target=eflaw
def search_english_law(query): # target=elaw

# 신규: 1개 통합 함수
def search_legislation(target, query, **params):
    """통합 법령 검색 함수"""
    return _make_legislation_request("lawSearch.do", target, query, **params)
```

#### **Phase 3: 단계별 확장**
1. **법령 → 행정규칙 → 자치법규**
2. **판례관련 4개 카테고리 통합**
3. **위원회결정문 12개 위원회 통합**
4. **중앙부처해석 8개 부처 통합**

## 📑 목차

- [법령](#법령)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [부가서비스](#부가서비스)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [행정규칙](#행정규칙)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [자치법규](#자치법규)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [판례관련](#판례관련)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [위원회결정문](#위원회결정문)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [조약](#조약)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [별표서식](#별표서식)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [학칙공단](#학칙공단)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [법령용어](#법령용어)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [맞춤형](#맞춤형)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [지식베이스](#지식베이스)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [기타](#기타)
  - [OPEN API 활용가이드](#open-api-활용가이드)
- [중앙부처해석](#중앙부처해석)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)
  - [OPEN API 활용가이드](#open-api-활용가이드)

---

## 법령

### OPEN API 활용가이드

**API ID**: `lsNwListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&query=%EC%9E%90%EB%8F%99%EC%B0%A8%EA%B4%80%EB%A6%AC%EB%B2%95`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : law(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령명) 2 : 본문검색 |
| query | string | 법령명에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 법령의 공포일자 검색 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| lsChapNo | string | 법령분류 (01-제1편 / 02-제2편 / 03-제3편... 44-제44편) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 법령 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : law(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령명) 2 : 본문검색 |
| query | string | 법령명에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 법령의 공포일자 검색 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| lsChapNo | string | 법령분류 (01-제1편 / 02-제2편 / 03-제3편... 44-제44편) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 현행법령 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML |
| 2. 현행법령 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=HTML |
| 3. 법령 검색 : 자동차관리법 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&query=자동차관리법 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 법령일련번호 | int | 법령일련번호 |
| 현행연혁코드 | string | 현행연혁코드 |
| 법령명한글 | string | 법령명한글 |
| 법령약칭명 | string | 법령약칭명 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | int | 소관부처코드 |
| 법령구분명 | string | 법령구분명 |
| 공동부령구분 | string | 공동부령구분 |
| 공포번호 | string | 공포번호(공동부령의 공포번호) |
| 시행일자 | int | 시행일자 |
| 자법타법여부 | string | 자법타법여부 |
| 법령상세링크 | string | 법령상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=law 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsNwInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=152338&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=152033&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=152338&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : law(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 -  법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| JO | int | 조번호 생략(기본값) : 모든 조를 표시함 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |
| LANG | char | 원문/한글 여부 생략(기본값) : 한글 (KO : 한글, ORI : 원문) |



[TABLE_0]
####  상세 내용


##### 범용 법령 통합 검색 도구 (search_law_unified)

**도구 개요**: 모든 법령 검색의 시작점 - 범용 통합 검색 도구

**주요 용도**:
- 일반적인 키워드로 관련 법령 탐색 (예: "부동산", "교통", "개인정보")
- 법령명을 정확히 모를 때 검색
- 다양한 종류의 법령을 한 번에 검색
- 법령의 역사, 영문판, 시행일 등 다양한 관점에서 검색

**매개변수**:
- `query`: 검색어 (필수) - 법령명, 키워드, 주제 등 자유롭게 입력
- `target`: 검색 대상 (기본값: "law")
  - `law`: 현행법령
  - `eflaw`: 시행일법령  
  - `lsHistory`: 법령연혁
  - `elaw`: 영문법령
  - 기타 20여개 타겟 지원
- `display`: 결과 개수 (최대 100)
- `page`: 페이지 번호
- `search`: 검색범위 (1=법령명, 2=본문검색)

**반환정보**: 법령명, 법령ID, 법령일련번호(MST), 공포일자, 시행일자, 소관부처

**권장 사용 순서**:
1. `search_law_unified("금융")` → 관련 법령 목록 파악
2. 구체적인 법령명 확인 후 → `search_law("은행법")`로 정밀 검색

**사용 예시**:
- `search_law_unified("금융")` # 금융 관련 모든 법령 검색
- `search_law_unified("세무", search=2)` # 본문에 세무 포함된 법령
- `search_law_unified("개인정보", target="law")` # 개인정보 관련 법령 검색
- `search_law_unified("Income Tax Act", target="elaw")` # 영문 소득세법 검색

**API 구현**: 내부적으로 `lawSearch.do` API를 사용하며, `target` 파라미터에 따라 다양한 법령 데이터베이스를 검색

---

##### 법령 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : law(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 -  법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| JO | int | 조번호 생략(기본값) : 모든 조를 표시함 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |
| LANG | char | 원문/한글 여부 생략(기본값) : 한글 (KO : 한글, ORI : 원문) |


| 샘플 URL |
| --- |
| 1. 법령 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=152338&type=HTML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=152033&type=HTML |
| 2. 법령 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=152338&type=XML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=152033&type=XML |


| 필드 | 값 | 설명 | 법령ID | int | 법령ID |
| --- | --- | --- | --- | --- | --- |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 언어 | string | 언어종류 |
| 법종구분 | string | 법종류의 구분 |
| 법종구분코드 | string | 법종구분코드 |
| 법령명_한글 | string | 한글법령명 |
| 법령명_한자 | string | 법령명_한자 |
| 법령명약칭 | string | 법령명약칭 |
| 제명변경여부 | string | 제명변경여부 |
| 한글법령여부 | string | 한글법령여부 |
| 편장절관 | int | 편장절관 일련번호 |
| 소관부처코드 | int | 소관부처코드 |
| 소관부처 | string | 소관부처명 |
| 전화번호 | string | 전화번호 |
| 시행일자 | int | 시행일자 |
| 제개정구분 | string | 제개정구분 |
| 별표편집여부 | string | 별표편집여부 |
| 공포법령여부 | string | 공포법령여부 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | int | 소관부처코드 |
| 부서명 | string | 연락부서명 |
| 부서연락처 | string | 연락부서 전화번호 |
| 공동부령구분 | string | 공동부령의 구분 |
| 구분코드 | string | 구분코드(공동부령구분 구분코드) |
| 공포번호 | string | 공포번호(공동부령의 공포번호) |
| 조문번호 | int | 조문번호 |
| 조문가지번호 | int | 조문가지번호 |
| 조문여부 | string | 조문여부 |
| 조문제목 | string | 조문제목 |
| 조문시행일자 | int | 조문시행일자 |
| 조문제개정유형 | string | 조문제개정유형 |
| 조문이동이전 | int | 조문이동이전 |
| 조문이동이후 | int | 조문이동이후 |
| 조문변경여부 | string | 조문변경여부(Y값이 있으면 해당 조문내에 변경 내용 있음 ) |
| 조문내용 | string | 조문내용 |
| 항번호 | int | 항번호 |
| 항제개정유형 | string | 항제개정유형 |
| 항제개정일자문자열 | string | 항제개정일자문자열 |
| 항내용 | string | 항내용 |
| 호번호 | int | 호번호 |
| 호내용 | string | 호내용 |
| 조문참고자료 | string | 조문참고자료 |
| 부칙공포일자 | int | 부칙공포일자 |
| 부칙공포번호 | int | 부칙공포번호 |
| 부칙내용 | string | 부칙내용 |
| 별표번호 | int | 별표번호 |
| 별표가지번호 | int | 별표가지번호 |
| 별표구분 | string | 별표구분 |
| 별표제목 | string | 별표제목 |
| 별표서식파일링크 | string | 별표서식파일링크 |
| 별표HWP파일명 | string | 별표 HWP 파일명 |
| 별표서식PDF파일링크 | string | 별표서식PDF파일링크 |
| 별표PDF파일명 | string | 별표 PDF 파일명 |
| 별표이미지파일명 | string | 별표 이미지 파일명 |
| 별표내용 | string | 별표내용 |
| 개정문내용 | string | 개정문내용 |
| 제개정이유내용 | string | 제개정이유내용 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=law 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsEfYdListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&query=%EC%9E%90%EB%8F%99%EC%B0%A8%EA%B4%80%EB%A6%AC%EB%B2%95`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : eflaw(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON 생략시 기본값: XML |
| search | int | 검색범위 (기본 : 1 법령명) 2 : 본문검색 |
| query | string | 법령명에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| nw | int | 1: 연혁, 2: 시행예정, 3: 현행 (기본값: 전체) 연혁+예정 : nw=1,2 예정+현행 : nw=2,3 연혁+현행 : nw=1,3 연혁+예정+현행 : nw=1,2,3 |
| LID | string | 법령ID (LID=830) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| date | string | 공포일자 검색 |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 시행일 법령 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : eflaw(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON 생략시 기본값: XML |
| search | int | 검색범위 (기본 : 1 법령명) 2 : 본문검색 |
| query | string | 법령명에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| nw | int | 1: 연혁, 2: 시행예정, 3: 현행 (기본값: 전체) 연혁+예정 : nw=1,2 예정+현행 : nw=2,3 연혁+현행 : nw=1,3 연혁+예정+현행 : nw=1,2,3 |
| LID | string | 법령ID (LID=830) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| date | string | 공포일자 검색 |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 시행일 법령 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=XML |
| 2. 시행일 법령 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=HTML |
| 3. 법령 검색 : 자동차관리법 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&query=자동차관리법 |
| 4. 법령 공포일자 내림차순 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=XML&sort=ddes |
| 5. 소관부처가 국토교통부인 법령 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=XML&org=1613000 |
| 6. '도서관법'을 법령 ID(830)로 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eflaw&type=XML&LID=830 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 법령일련번호 | int | 법령일련번호 |
| 현행연혁코드 | string | 현행연혁코드 |
| 법령명한글 | string | 법령명한글 |
| 법령약칭명 | string | 법령약칭명 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처코드 | string | 소관부처명 |
| 소관부처명 | string | 소관부처명 |
| 법령구분명 | string | 법령구분명 |
| 공동부령구분 | string | 공동부령구분 |
| 공포번호 | string | 공포번호(공동부령의 공포번호) |
| 시행일자 | int | 시행일자 |
| 자법타법여부 | string | 자법타법여부 |
| 법령상세링크 | string | 법령상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=eflaw 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsEfYdInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&ID=1747&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&MST=166520&efYd=20151007&type=XML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&MST=166520&efYd=20151007&JO=000300&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : eflaw(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON  생략시 기본값 : XML |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력,ID로 검색하면 그 법령의 현행 법령 본문 조회) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| efYd | int(필수) | 법령의 시행일자  (ID 입력시에는 무시하는 값으로 입력하지 않음) |
| JO | int | 조번호 생략(기본값) : 모든 조를 표시함 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |
| chrClsCd | char | 원문/한글 여부 생략(기본값) : 한글 (010202 : 한글, 010201 : 원문) |



[TABLE_0]
####  상세 내용


##### 시행일 법령 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : eflaw(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON  생략시 기본값 : XML |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력,ID로 검색하면 그 법령의 현행 법령 본문 조회) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| efYd | int(필수) | 법령의 시행일자  (ID 입력시에는 무시하는 값으로 입력하지 않음) |
| JO | int | 조번호 생략(기본값) : 모든 조를 표시함 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |
| chrClsCd | char | 원문/한글 여부 생략(기본값) : 한글 (010202 : 한글, 010201 : 원문) |


| 샘플 URL |
| --- |
| 1. 자동차관리법 ID HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&ID=1747&type=HTML |
| 2. 자동차관리법 법령 Seq XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&MST=166520&efYd=20151007&type=XML |
| 3. 자동차관리법 3조 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflaw&MST=166520&efYd=20151007&JO=000300&type=XML |


| 필드 | 값 | 설명 | 법령ID | int | 법령ID |
| --- | --- | --- | --- | --- | --- |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 언어 | string | 언어종류 |
| 법종구분 | string | 법종류의 구분 |
| 법종구분코드 | string | 법종구분코드 |
| 법령명_한글 | string | 한글법령명 |
| 법령명_한자 | string | 법령명_한자 |
| 법령명약칭 | string | 법령명약칭 |
| 편장절관 | int | 편장절관 일련번호 |
| 소관부처코드 | int | 소관부처코드 |
| 소관부처 | string | 소관부처명 |
| 전화번호 | string | 전화번호 |
| 시행일자 | int | 시행일자 |
| 제개정구분 | string | 제개정구분 |
| 조문시행일자문자열 | string | 조문시행일자문자열 |
| 별표시행일자문자열 | string | 별표시행일자문자열 |
| 별표편집여부 | string | 별표편집여부 |
| 공포법령여부 | string | 공포법령여부 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | int | 소관부처코드 |
| 부서명 | string | 연락부서명 |
| 부서연락처 | string | 연락부서 전화번호 |
| 공동부령구분 | string | 공동부령의 구분 |
| 구분코드 | string | 구분코드(공동부령구분 구분코드) |
| 공포번호 | string | 공포번호(공동부령의 공포번호) |
| 조문번호 | int | 조문번호 |
| 조문가지번호 | int | 조문가지번호 |
| 조문여부 | string | 조문여부 |
| 조문제목 | string | 조문제목 |
| 조문시행일자 | int | 조문시행일자 |
| 조문제개정유형 | string | 조문제개정유형 |
| 조문이동이전 | int | 조문이동이전 |
| 조문이동이후 | int | 조문이동이후 |
| 조문변경여부 | string | 조문변경여부(Y값이 있으면 해당 조문내에 변경 내용 있음 ) |
| 조문내용 | string | 조문내용 |
| 항번호 | int | 항번호 |
| 항제개정유형 | string | 항제개정유형 |
| 항제개정일자문자열 | string | 항제개정일자문자열 |
| 항내용 | string | 항내용 |
| 호번호 | int | 호번호 |
| 호내용 | string | 호내용 |
| 조문참고자료 | string | 조문참고자료 |
| 부칙공포일자 | int | 부칙공포일자 |
| 부칙공포번호 | int | 부칙공포번호 |
| 부칙내용 | string | 부칙내용 |
| 별표번호 | int | 별표번호 |
| 별표가지번호 | int | 별표가지번호 |
| 별표구분 | string | 별표구분 |
| 별표제목 | string | 별표제목 |
| 별표제목문자열 | string | 별표제목문자열 |
| 별표시행일자 | int | 별표시행일자 |
| 별표서식파일링크 | string | 별표서식파일링크 |
| 별표HWP파일명 | string | 별표 HWP 파일명 |
| 별표서식PDF파일링크 | string | 별표서식PDF파일링크 |
| 별표PDF파일명 | string | 별표 PDF 파일명 |
| 별표이미지파일명 | string | 별표 이미지 파일명 |
| 별표내용 | string | 별표내용 |
| 개정문내용 | string | 개정문내용 |
| 제개정이유내용 | string | 제개정이유내용 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=eflaw 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsHstListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsHistory&type=HTML&query=%EC%9E%90%EB%8F%99%EC%B0%A8%EA%B4%80%EB%A6%AC%EB%B2%95`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsHistory&type=HTML&org=1741000`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsHistory&type=HTML&query=자동차관리법`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsHistory(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML |
| query | string | 법령명에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| date | string | 공포일자 검색 |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| lsChapNo | string | 법령분류 (01-제1편 / 02-제2편 / 03-제3편... 44-제44편) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 법령 연혁 목록 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsHistory(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML |
| query | string | 법령명에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| date | string | 공포일자 검색 |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| lsChapNo | string | 법령분류 (01-제1편 / 02-제2편 / 03-제3편... 44-제44편) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 자동차관리법 법령연혁 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsHistory&type=HTML&query=자동차관리법 |
| 2. 소관부처별(행정안전부 : 1741000) 법령연혁 HTML조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsHistory&type=HTML&org=1741000 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lsHistory 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `lsHstInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lsHistory&MST=9094&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lsHistory&MST=166500&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsHistory&MST=9094&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsHistory(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| chrClsCd | char | 원문/한글 여부 생략(기본값) : 한글 (010202 : 한글, 010201 : 원문) |



[TABLE_0]
####  상세 내용


##### 법령 연혁 본문 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsHistory(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| chrClsCd | char | 원문/한글 여부 생략(기본값) : 한글 (010202 : 한글, 010201 : 원문) |


| 샘플 URL |
| --- |
| 1. 법령연혁 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsHistory&MST=9094&type=HTML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsHistory&MST=166500&type=HTML |



[HEADING_0] ※ 체계도 등 부가서비스는 법령서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=lsHistory 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `lsNwJoListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lawjosub&type=XML&ID=001823&JO=000300&HANG=000100&HO=000200&MOK=%EB%8B%A4`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lawjosub&type=HTML&ID=001823&JO=000300&HANG=000100&HO=000200&MOK=%EB%8B%A4`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=lawjosub&type=XML&ID=001823&JO=000300&HANG=000100&HO=000200&MOK=다`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lawjosub(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력)  (ID로 검색하면 그 법령의 현행 법령 본문 조회) |
| MST | char | 법령 마스터 번호 -  법령테이블의 lsi_seq 값을 의미함 |
| JO | char(필수) | 조 번호 6자리숫자  예) 제2조 : 000200, 제10조의2 : 001002 |
| HANG | char | 항 번호 6자리숫자  예) 제2항 : 000200 |
| HO | char | 호 번호 6자리숫자  예) 제2호 : 000200, 제10호의2 : 001002 |
| MOK | char | 목 한자리 문자  예) 가,나,다,라, … 카,타,파,하  한글은 인코딩 하여 사용하여야 정상적으로 사용이가능 URLDecoder.decode("다", "UTF-8") |



[TABLE_0]
####  상세 내용


##### 현행법령 본문 조항호목 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lawjosub(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력)  (ID로 검색하면 그 법령의 현행 법령 본문 조회) |
| MST | char | 법령 마스터 번호 -  법령테이블의 lsi_seq 값을 의미함 |
| JO | char(필수) | 조 번호 6자리숫자  예) 제2조 : 000200, 제10조의2 : 001002 |
| HANG | char | 항 번호 6자리숫자  예) 제2항 : 000200 |
| HO | char | 호 번호 6자리숫자  예) 제2호 : 000200, 제10호의2 : 001002 |
| MOK | char | 목 한자리 문자  예) 가,나,다,라, … 카,타,파,하  한글은 인코딩 하여 사용하여야 정상적으로 사용이가능 URLDecoder.decode("다", "UTF-8") |


| 샘플 URL |
| --- |
| 1. 건축법 제3조제1항제2호다목 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lawjosub&type=XML&ID=001823&JO=000300&HANG=000100&HO=000200&MOK=다 |
| 2. 건축법 제3조제1항제2호다목 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lawjosub&type=HTML&ID=001823&JO=000300&HANG=000100&HO=000200&MOK=다 |


| 필드 | 값 | 설명 | 법령키 | int | 법령키 |
| --- | --- | --- | --- | --- | --- |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 언어 | string | 언어 구분 |
| 법령명_한글 | string | 법령명을 한글로 제공 |
| 법령명_한자 | string | 법령명을 한자로 제공 |
| 법종구분코드 | string | 법종구분코드 |
| 법종구분명 | string | 법종구분명 |
| 제명변경여부 | string | 제명변경여부(Y값이 있으면 해당 법령은 제명 변경임) |
| 한글법령여부 | string | 한글법령여부(Y값이 있으면 해당 법령은 한글법령) |
| 편장절관 | int | 편장절관 |
| 소관부처코드 | int | 소관부처 코드 |
| 소관부처 | string | 소관부처명 |
| 전화번호 | string | 전화번호 |
| 시행일자 | int | 시행일자 |
| 제개정구분 | string | 제개정구분명 |
| 제안구분 | string | 제안구분 |
| 의결구분 | string | 의결구분 |
| 이전법령명 | string | 이전법령명 |
| 조문별시행일자 | string | 조문별시행일자 |
| 조문시행일자문자열 | string | 조문시행일자문자열 |
| 별표시행일자문자열 | string | 별표시행일자문자열 |
| 별표편집여부 | string | 별표편집여부 |
| 공포법령여부 | string | 공포법령여부(Y값이 있으면 해당 법령은 공포법령임) |
| 시행일기준편집여부 | string | 시행일기준편집여부(Y값이 있으면 해당 법령은 시행일 기준 편집됨) |
| 조문번호 | int | 조문번호 |
| 조문여부 | string | 조문여부 |
| 조문제목 | string | 조문제목 |
| 조문시행일자 | string | 조문시행일자 |
| 조문이동이전 | int | 조문이동이전번호 |
| 조문이동이후 | int | 조문이동이후번호 |
| 조문변경여부 | string | 조문변경여부(Y값이 있으면 해당 조문내에 변경 내용 있음 ) |
| 조문내용 | string | 조문내용 |
| 항번호 | int | 항번호 |
| 항내용 | string | 항내용 |
| 호번호 | int | 호번호 |
| 호내용 | string | 호내용 |
| 목번호 | string | 목번호 |
| 목내용 | string | 목내용 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=lawjosub 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsEfYdJoListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=eflawjosub&type=XML&MST=193412&efYd=20171019&JO=000300&HANG=000100&HO=000200&MOK=%EB%8B%A4`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=eflawjosub&type=HTML&MST=193412&efYd=20171019&JO=000300&HANG=000100&HO=000200&MOK=%EB%8B%A4`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflawjosub&type=XML&MST=193412&efYd=20171019&JO=000300&HANG=000100&HO=000200&MOK=다`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : eflawjosub(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 -  법령테이블의 lsi_seq 값을 의미함 |
| efYd | int(필수) | 법령의 시행일자  (ID 입력시에는 무시하는 값으로 입력하지 않음) |
| JO | char(필수) | 조 번호 6자리숫자  예) 제2조 : 000200, 제10조의2 : 001002 |
| HANG | char | 항 번호 6자리숫자  예) 제2항 : 000200 |
| HO | char | 호 번호 6자리숫자  예) 제2호 : 000200, 제10호의2 : 001002 |
| MOK | char | 목 한자리 문자  예) 가,나,다,라, … 카,타,파,하  한글은 인코딩 하여 사용하여야 정상적으로 사용이가능 URLDecoder.decode("다", "UTF-8") |



[TABLE_0]
####  상세 내용


##### 시행일법령 본문 조항호목 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : eflawjosub(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 -  법령테이블의 lsi_seq 값을 의미함 |
| efYd | int(필수) | 법령의 시행일자  (ID 입력시에는 무시하는 값으로 입력하지 않음) |
| JO | char(필수) | 조 번호 6자리숫자  예) 제2조 : 000200, 제10조의2 : 001002 |
| HANG | char | 항 번호 6자리숫자  예) 제2항 : 000200 |
| HO | char | 호 번호 6자리숫자  예) 제2호 : 000200, 제10호의2 : 001002 |
| MOK | char | 목 한자리 문자  예) 가,나,다,라, … 카,타,파,하  한글은 인코딩 하여 사용하여야 정상적으로 사용이가능 URLDecoder.decode("다", "UTF-8") |


| 샘플 URL |
| --- |
| 1. 건축법 제3조제1항제2호다목 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflawjosub&type=XML&MST=193412&efYd=20171019&JO=000300&HANG=000100&HO=000200&MOK=다 |
| 2. 건축법 제3조제1항제2호다목 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=eflawjosub&type=HTML&MST=193412&efYd=20171019&JO=000300&HANG=000100&HO=000200&MOK=다 |


| 필드 | 값 | 설명 | 법령키 | int | 법령키 |
| --- | --- | --- | --- | --- | --- |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 언어 | string | 언어 |
| 법종구분 | string | 법종구분 |
| 법종구분 코드 | string | 법종구분 코드 |
| 법령명_한글 | string | 법령명을 한글로 제공 |
| 법령명_한자 | string | 법령명을 한자로 제공 |
| 법령명_영어 | string | 법령명을 영어로 제공 |
| 편장절관 | int | 편장절관 |
| 소관부처코드 | int | 소관부처 코드 |
| 소관부처 | string | 소관부처명 |
| 전화번호 | string | 전화번호 |
| 시행일자 | int | 시행일자 |
| 제개정구분 | string | 제개정구분명 |
| 제안구분 | string | 제안구분 |
| 의결구분 | string | 의결구분 |
| 적용시작일자 | string | 적용시작일자 |
| 적용종료일자 | string | 적용종료일자 |
| 이전법령명 | string | 이전법령명 |
| 조문시행일자문자열 | string | 조문시행일자문자열 |
| 별표시행일자문자열 | string | 별표시행일자문자열 |
| 별표편집여부 | string | 별표편집여부 |
| 공포법령여부 | string | 공포법령여부(Y값이 있으면 해당 법령은 공포법령임) |
| 조문번호 | int | 조문번호 |
| 조문여부 | string | 조문여부 |
| 조문제목 | string | 조문제목 |
| 조문시행일자 | string | 조문시행일자 |
| 조문이동이전 | int | 조문이동이전번호 |
| 조문이동이후 | int | 조문이동이후번호 |
| 조문변경여부 | string | 조문변경여부(Y값이 있으면 해당 조문내에 변경 내용 있음 ) |
| 조문내용 | string | 조문내용 |
| 항번호 | int | 항번호 |
| 항내용 | string | 항내용 |
| 호번호 | int | 호번호 |
| 호내용 | string | 호내용 |
| 목번호 | string | 목번호 |
| 목내용 | string | 목내용 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=eflawjosub 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsEngListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=elaw&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=elaw&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=elaw&type=XML&query=%EA%B0%80%EC%A0%95%ED%8F%AD%EB%A0%A5%EB%B0%A9%EC%A7%80`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : elaw(필수) | 서비스 대상 |
| search | int | 검색범위 (기본 : 1 법령명) 2 : 본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 법령의 공포일자 검색 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| type | char | 출력 형태 HTML/XML/JSON |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 영문법령 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : elaw(필수) | 서비스 대상 |
| search | int | 검색범위 (기본 : 1 법령명) 2 : 본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 법령의 공포일자 검색 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| type | char | 출력 형태 HTML/XML/JSON |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 영문법령 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=elaw&type=XML |
| 2. 영문법령 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=elaw&type=HTML |
| 3. 영문법령 검색 : 가정폭력방지, insurance |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=elaw&type=XML&query=가정폭력방지 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=elaw&type=XML&query=insurance |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 법령일련번호 | int | 법령일련번호 |
| 현행연혁코드 | string | 현행연혁코드 |
| 법령명한글 | string | 법령명한글 |
| 법령명영문 | string | 법령명영문 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처명 | string | 소관부처명 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 자법타법여부 | string | 자법타법여부 |
| 법령상세링크 | string | 법령상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=elaw 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsEngInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=elaw&ID=000744&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=elaw&MST=127280&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=elaw&ID=000744&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : elaw(필수) | 서비스 대상 |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| type | char | 출력 형태 : HTML/XML/JSON |



[TABLE_0]
####  상세 내용


##### 영문법령 본문 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : elaw(필수) | 서비스 대상 |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| type | char | 출력 형태 : HTML/XML/JSON |


| 샘플 URL |
| --- |
| 1. 표준시에 관한 법률 ID HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=elaw&ID=000744&type=HTML |
| 2. 상호저축은행법 시행령 seq HTML조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=elaw&MST=127280&type=HTML |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=elaw 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `lsChgListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?target=lsHstInf&OC=test&regDt=20170726&type=HTML`
2. `http://www.law.go.kr/DRF/lawSearch.do?target=lsHstInf&OC=test&regDt=20170726&type=HTML`
3. `http://www.law.go.kr/DRF/lawSearch.do?target=lsHstInf`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsHstInf(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| regDt | int(필수) | 법령 변경일 검색(20150101) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 법령 변경이력 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsHstInf(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| regDt | int(필수) | 법령 변경일 검색(20150101) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 법령 변경일이 20170726인 법령 목록 |
| http://www.law.go.kr/DRF/lawSearch.do?target=lsHstInf&OC=test&regDt=20170726&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| totalCnt | int | 검색건수 |
| page | int | 현재 페이지번호 |
| law id | int | 검색 결과 순번 |
| 법령일련번호 | int | 법령일련번호 |
| 현행연혁코드 | string | 현행연혁코드 |
| 법령명한글 | string | 법령명한글 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처코드 | string | 소관부처코드 |
| 소관부처명 | string | 소관부처명 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 자법타법여부 | string | 자법타법여부 |
| 법령상세링크 | string | 법령상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lsHstInf 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsDayJoRvsListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?target=lsJoHstInf&OC=test&regDt=20150211`
2. `//www.law.go.kr/DRF/lawSearch.do?target=lsJoHstInf&OC=test&fromRegDt=20150201`
3. `//www.law.go.kr/DRF/lawSearch.do?target=lsJoHstInf&OC=test&regDt=20150211&org=1270000`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsJoHstInf(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 XML/JSON |
| regDt | int | 조문 개정일, 8자리 (20150101) |
| fromRegDt | int | 조회기간 시작일, 8자리 (20150101) |
| toRegDt | int | 조회기간 종료일, 8자리 (20150101) |
| ID | int | 법령ID |
| JO | int | 조문번호 조문번호 4자리 + 조 가지번호 2자리 (000202 : 제2조의2) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| page | int | 검색 결과 페이지 (default=1) |



[TABLE_0]
####  상세 내용


##### 일자별 조문 개정 이력 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsJoHstInf(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 XML/JSON |
| regDt | int | 조문 개정일, 8자리 (20150101) |
| fromRegDt | int | 조회기간 시작일, 8자리 (20150101) |
| toRegDt | int | 조회기간 종료일, 8자리 (20150101) |
| ID | int | 법령ID |
| JO | int | 조문번호 조문번호 4자리 + 조 가지번호 2자리 (000202 : 제2조의2) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| page | int | 검색 결과 페이지 (default=1) |


| 샘플 URL |
| --- |
| 1. 조문 개정 일자가 20150211인 조문 |
| http://www.law.go.kr/DRF/lawSearch.do?target=lsJoHstInf&OC=test&regDt=20150211 |
| 2. 조문 개정 일자 기간 검색 중 검색 기간 시작일이 20150201인 조문 |
| http://www.law.go.kr/DRF/lawSearch.do?target=lsJoHstInf&OC=test&fromRegDt=20150201 |
| 3. 조문 개정 일자가 20150211이면서 기관이 법무부인 조문 |
| http://www.law.go.kr/DRF/lawSearch.do?target=lsJoHstInf&OC=test&regDt=20150211&org=1270000 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| totalCnt | int | 검색한 기간에 개정 조문이 있는 법령의 건수 |
| law id | int | 결과 번호 |
| 법령일련번호 | int | 법령일련번호 |
| 법령명한글 | string | 법령명한글 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | string | 소관부처코드 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| jo num | string | 조 구분 번호 |
| 조문정보 | string | 조문정보 |
| 조문번호 | string | 조문번호 |
| 변경사유 | string | 변경사유 |
| 조문링크 | string | 조문링크 |
| 조문변경이력상세링크 | string | 조문변경이력상세링크 |
| 조문개정일 | int | 조문제개정일 |
| 조문시행일 | int | 조문시행일 |



[HEADING_0] 이 서비스는 전일 데이터를 기준으로 제공됩니다. 원하시는 날짜의 익일에 서비스를 조회해주시기 바랍니다. (예) 2017년10월1일에 개정된 조문을 조회할 경우, 2017년10월2일에 regDt=20171001으로 조회 - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lsJoHstInf 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsJoChgListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lsJoHstInf&ID=001971&JO=000500&type=XML`
2. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsJoHstInf&ID=001971&JO=000500&type=XML`
3. `http://www.law.go.kr/DRF/lawService.do?target=lsJoHstInf`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsJoHstInf(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : XML/JSON |
| ID | char(필수) | 법령 ID |
| JO | int(필수) | 조번호 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |



[TABLE_0]
####  상세 내용


##### 조문별 변경 이력 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsJoHstInf(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : XML/JSON |
| ID | char(필수) | 법령 ID |
| JO | int(필수) | 조번호 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |


| 샘플 URL |
| --- |
| 1. 법령 ID가 001971 이면서 5조인 법령의 변경이력 목록 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsJoHstInf&ID=001971&JO=000500&type=XML |


| 필드 | 값 | 설명 | 법령ID | int | 법령ID |
| --- | --- | --- | --- | --- | --- |
| 법령명한글 | int | 법령명(한글) |
| 법령일련번호 | int | 법령일련번호 |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | string | 소관부처코드 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 조문번호 | int | 조문번호 |
| 변경사유 | int | 변경사유 |
| 조문링크 | int | 변경사유 |
| 조문변경일 | int | 조문변경일 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=lsJoHstInf 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsOrdinConListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLs&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLs&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLs&type=XML&query=%EC%9E%90%EB%8F%99%EC%B0%A8%EA%B4%80%EB%A6%AC%EB%B2%95`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lnkDep(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 소관부처별 검색(코드별도제공) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 자치법규 오름차순 ddes : 자치법규 내림차순 nasc : 자치법규 공포일자 오름차순 ndes : 자치법규 공포일자 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 법령 자치법규 연계 목록 조회 API


###### 연계 법령별 조례 조문 목록 조회 API


###### 연계 법령 소관부처별 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lnkLs(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 연계 법령 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLs&type=XML |
| 2. 연계 법령 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLs&type=HTML |
| 3. 연계 법령 검색 : 자동차관리법 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLs&type=XML&query=자동차관리법 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 법령일련번호 | int | 법령일련번호 |
| 법령명한글 | string | 법령명한글 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lnkLsOrdJo(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 자치법규 오름차순 ddes : 자치법규 내림차순 nasc : 자치법규 공포일자 오름차순 ndes : 자치법규 공포일자 내림차순 |
| knd | string | 법령종류(코드제공) |
| JO | int | 조번호 생략(기본값) : 모든 조를 표시함 4자리숫자 : 조번호(4자리) (0023 : 23조) |
| JOBR | int | 조가지번호 2자리숫자 : 조가지번호(2자리) (02 : 2) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 연계 법령별 조례 조문 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLsOrdJo&type=XML |
| 2. 연계 법령별 조례 조문 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLsOrdJo&type=HTML |
| 3. 법령별 조례 조문 검색 : 건축법 시행령 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLsOrdJo&type=XML&knd=002118 |
| 4. 법령 조문별 조례 조문 검색 : 건축법 시행령 제20조 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLsOrdJo&type=XML&knd=002118&JO=0020 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 법령명한글 | string | 법령명한글 |
| 법령ID | int | 법령ID |
| 법령조번호 | string | 법령조번호 |
| 자치법규일련번호 | int | 자치법규 일련번호 |
| 자치법규명 | string | 자치법규명 |
| 자치법규조번호 | string | 자치법규 조번호 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | int | 자치법규 공포일자 |
| 공포번호 | int | 자치법규 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 자치법규종류 | string | 자치법규종류 |
| 시행일자 | int | 자치법규 시행일자 |


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lnkDep(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 소관부처별 검색(코드별도제공) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 자치법규 오름차순 ddes : 자치법규 내림차순 nasc : 자치법규 공포일자 오름차순 ndes : 자치법규 공포일자 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 소관부처가 '산림청'인 연계 법령 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkDep&org=1400000&type=XML |
| 2. 소관부처가 '산림청'인 연계 법령 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkDep&org=1400000&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 법령명한글 | string | 법령명한글 |
| 법령ID | int | 법령ID |
| 자치법규일련번호 | int | 자치법규 일련번호 |
| 자치법규명 | string | 자치법규명 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | int | 자치법규 공포일자 |
| 공포번호 | int | 자치법규 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 자치법규종류 | string | 자치법규종류 |
| 시행일자 | int | 자치법규 시행일자 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lnkLs 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [HEADING_1] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lnkLsOrdJo 요청 변수 (request parameter) [TABLE_3] [TABLE_4] 출력 결과 필드(response field) [TABLE_5] [HEADING_2] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lnkDep 요청 변수 (request parameter) [TABLE_6] [TABLE_7] 출력 결과 필드(response field) [TABLE_8]

---

### OPEN API 활용가이드

**API ID**: `lsOrdinConGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=drlaw&type=HTML`
2. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=drlaw&type=HTML`
3. `http://www.law.go.kr/DRF/lawSearch.do?target=drlaw`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : drlaw(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML |



[TABLE_0]
####  상세 내용


##### 법령-자치법규 연계현황 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : drlaw(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML |


| 샘플 URL |
| --- |
| 1. 법령-자치법규 연계현황 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=drlaw&type=HTML |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=drlaw 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `lsDelegated`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lsDelegated&type=XML&ID=000900`
2. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsDelegated&type=XML&ID=000900`
3. `http://www.law.go.kr/DRF/lawService.do?target=lsDelegated`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsDelegated (필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력,ID로 검색하면 그 법령의 현행 법령 본문 조회) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |



[TABLE_0]
####  상세 내용


##### 위임 법령 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsDelegated (필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력,ID로 검색하면 그 법령의 현행 법령 본문 조회) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |


| 샘플 URL |
| --- |
| 1. 초·중등교육법의 위임 법령 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsDelegated&type=XML&ID=000900 |


| 필드 | 값 | 설명 | 법령일련번호 | int | 법령일련번호 |
| --- | --- | --- | --- | --- | --- |
| 법령명 | string | 법령명 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 소관부처코드 | int | 소관부처코드 |
| 전화번호 | string | 전화번호 |
| 시행일자 | int | 시행일자 |
| 조문번호 | string | 조문번호 |
| 조문제목 | string | 조문제목 |
| 위임구분 | string | 위임된 법령의 종류 |
| 위임법령일련번호 | string | 위임된 법령의 일련번호 |
| 위임법령제목 | string | 위임된 법령의 제목 |
| 위임법령조문번호 | string | 위임된 법령의 조문번호 |
| 위임법령조문가지번호 | string | 위임된 법령의 조문 가지번호 |
| 위임법령조문제목 | string | 위임된 법령의 조문 제목 |
| 링크텍스트 | string | 위임된 법령에 대한 링크를 걸어줘야 하는 텍스트 |
| 라인텍스트 | string | 링크텍스트가 포함된 텍스트(조문내용) |
| 조항호목 | string | 링크텍스트와 라인텍스트가 포함된 조항호목 |
| 위임행정규칙일련번호 | string | 위임된 행정규칙의 일련번호 |
| 위임행정규칙제목 | string | 위임된 행정규칙의 제목 |
| 링크텍스트 | string | 위임된 행정규칙에 대한 링크를 걸어줘야 하는 텍스트 |
| 라인텍스트 | string | 링크텍스트가 포함된 텍스트(조문내용) |
| 조항호목 | string | 링크텍스트와 라인텍스트가 포함된 조항호목 |
| 위임자치법규일련번호 | string | 위임된 자치법규의 일련번호 |
| 위임자치법규제목 | string | 위임된 자치법규의 제목 |
| 링크텍스트 | string | 위임된 자치법규에 대한 링크를 걸어줘야 하는 텍스트 |
| 라인텍스트 | string | 링크텍스트가 포함된 텍스트(조문내용) |
| 조항호목 | string | 링크텍스트와 라인텍스트가 포함된 조항호목 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=lsDelegated 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 부가서비스

### OPEN API 활용가이드

**API ID**: `lsStmdListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsStmd&type=HTML&query=%EC%9E%90%EB%8F%99%EC%B0%A8%EA%B4%80%EB%A6%AC%EB%B2%95`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsStmd&type=HTML&gana=ga`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsStmd&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsStmd(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| date | int | 공포일자 검색 |
| nb | int | 공포번호 검색 |
| ancNo | string | 공포번호 범위 검색 (10000~20000) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 법령 체계도 목록 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsStmd(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| date | int | 공포일자 검색 |
| nb | int | 공포번호 검색 |
| ancNo | string | 공포번호 범위 검색 (10000~20000) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 자동차관리법 법령체계도 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsStmd&type=HTML&query=자동차관리법 |
| 2. 'ㄱ'으로 시작하는 법령체계도 HTML조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsStmd&type=HTML&gana=ga |
| 3. 법령체계도 XML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsStmd&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| numOfRows | int | 페이지 당 출력 결과 수 |
| resultCode | int | 조회 여부(성공 : 00 / 실패 : 01) |
| resultMsg | int | 조회 여부(성공 : success / 실패 : fail) |
| law id | int | 검색 결과 순번 |
| 법령 일련번호 | int | 법령 일련번호 |
| 법령명 | string | 법령명 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처코드 | int | 소관부처코드 |
| 소관부처명 | string | 소관부처명 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 본문 상세링크 | string | 본문 상세링크 |



[HEADING_0] ※ 체계도 등 부가서비스는 법령서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lsStmd 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsStmdInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lsStmd&MST=142362&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lsStmd&MST=166519&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lsStmd&MST=142362&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsStmd(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |



[TABLE_0]
####  상세 내용


##### 법령 체계도 본문 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsStmd(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |


| 샘플 URL |
| --- |
| 1. 법령체계도 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsStmd&MST=142362&type=HTML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsStmd&MST=142591&type=HTML |
| 2. 법령체계도 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lsStmd&MST=142362&type=XML |


| 필드 | 값 | 설명 | 기본정보 | string | 기본정보 |
| --- | --- | --- | --- | --- | --- |
| 법령ID | int | 법령ID |
| 법령일련번호 | int | 법령일련번호 |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 법종구분 | string | 법종구분 |
| 법령명 | string | 법령 |
| 시행일자 | int | 시행일자 |
| 제개정구분 | string | 제개정구분 |
| 상하위법 | string | 상하위법 |
| 법률 | string | 법률 |
| 시행령 | string | 시행령 |
| 시행규칙 | string | 시행규칙 |
| 본문 상세링크 | string | 본문 상세링크 |



[HEADING_0] ※ 체계도 등 부가서비스는 법령서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=lsStmd 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `oldAndNewListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=oldAndNew&type=HTML&query=%EC%9E%90%EB%8F%99%EC%B0%A8%EA%B4%80%EB%A6%AC%EB%B2%95`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=oldAndNew&type=HTML&efYd=20150101~20150131`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=oldAndNew&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : oldAndNew(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| date | int | 공포일자 검색 |
| nb | int | 공포번호 검색 |
| ancNo | string | 공포번호 범위 검색 (10000~20000) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 신구법 목록 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : oldAndNew(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| date | int | 공포일자 검색 |
| nb | int | 공포번호 검색 |
| ancNo | string | 공포번호 범위 검색 (10000~20000) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 자동차관리법 신구법 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oldAndNew&type=HTML&query=자동차관리법 |
| 2. 시행일자 범위 신구법 HTML조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oldAndNew&type=HTML&efYd=20150101~20150131 |
| 3. 신구법 XML조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oldAndNew&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| numOfRows | int | 페이지 당 출력 결과 수 |
| resultCode | int | 조회 여부(성공 : 00 / 실패 : 01) |
| resultMsg | int | 조회 여부(성공 : success / 실패 : fail) |
| oldAndNew id | int | 검색 결과 순번 |
| 신구법일련번호 | int | 신구법 일련번호 |
| 현행연혁구분 | string | 현행연혁코드 |
| 신구법명 | string | 신구법명 |
| 신구법ID | int | 신구법ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처코드 | int | 소관부처코드 |
| 소관부처명 | string | 소관부처명 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 신구법상세링크 | string | 신구법 상세링크 |



[HEADING_0] ※ 체계도 등 부가서비스는 법령서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=oldAndNew 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `oldAndNewInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=oldAndNew&ID=000170&MST=122682&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=oldAndNew&MST=136931&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=oldAndNew&MST=122682&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : oldAndNew(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |



[TABLE_0]
####  상세 내용


##### 신구법 본문 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : oldAndNew(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |


| 샘플 URL |
| --- |
| 1. 신구법 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=oldAndNew&ID=000170&MST=122682&type=HTML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=oldAndNew&MST=136931&type=HTML |
| 2. 신구법 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=oldAndNew&MST=122682&type=XML |


| 필드 | 값 | 설명 | 구조문_기본정보 | string | 구조문_기본정보 |
| --- | --- | --- | --- | --- | --- |
| 법령일련번호 | int | 법령일련번호 |
| 법령ID | int | 법령ID |
| 시행일자 | int | 시행일자 |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 현행여부 | string | 현행여부 |
| 제개정구분명 | string | 제개정구분명 |
| 법령명 | string | 법령 |
| 법종구분 | string | 법종구분 |
| 신조문_기본정보 | string | 구조문과 동일한 기본 정보 들어가 있음. |
| 구조문목록 | string | 구조문목록 |
| 조문 | string | 조문 |
| 신조문목록 | string | 신조문목록 |
| 조문 | string | 조문 |
| 신구법존재여부 | string | 신구법이 존재하지 않을 경우 N이 조회. |



[HEADING_0] ※ 체계도 등 부가서비스는 법령서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=oldAndNew 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `thdCmpListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=thdCmp&type=HTML&query=%EC%9E%90%EB%8F%99%EC%B0%A8%EA%B4%80%EB%A6%AC%EB%B2%95`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=thdCmp&type=HTML&rrClsCd=300201`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=thdCmp&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : thdCmp(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| date | int | 공포일자 검색 |
| nb | int | 공포번호 검색 |
| ancNo | string | 공포번호 범위 검색 (10000~20000) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 3단 비교 목록 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : thdCmp(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| date | int | 공포일자 검색 |
| nb | int | 공포번호 검색 |
| ancNo | string | 공포번호 범위 검색 (10000~20000) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300209-타법개정 / 300210-타법폐지 300208-기타) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 법령종류(코드제공) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 자동차관리법 3단비교 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=thdCmp&type=HTML&query=자동차관리법 |
| 2. 법령 제개정 종류(제정) 3단비교 HTML조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=thdCmp&type=HTML&rrClsCd=300201 |
| 3. 3단비교 목록 XML조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=thdCmp&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| numOfRows | int | 페이지 당 출력 결과 수 |
| resultCode | int | 조회 여부(성공 : 00 / 실패 : 01) |
| resultMsg | int | 조회 여부(성공 : success / 실패 : fail) |
| thdCmp id | int | 검색결과 순번 |
| 삼단비교일련번호 | int | 삼단비교 일련번호 |
| 법령명 한글 | string | 법령명 한글 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처코드 | int | 소관부처코드 |
| 소관부처명 | string | 소관부처명 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 인용조문_삼단비교상세링크 | string | 인용조문_삼단비교 상세링크 |
| 위임조문_삼단비교상세링크 | string | 위임조문_삼단비교 상세링크 |



[HEADING_0] ※ 체계도 등 부가서비스는 법령서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=thdCmp 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `thdCmpInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=thdCmp&ID=001372&MST=162662&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=thdCmp&ID=001570&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=thdCmp&MST=236231&knd=1&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : thdCmp(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| knd | int(필수) | 3단비교 종류별 검색 인용조문 : 1 / 위임조문 : 2 |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |



[TABLE_0]
####  상세 내용


##### 3단비교 본문 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : thdCmp(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| knd | int(필수) | 3단비교 종류별 검색 인용조문 : 1 / 위임조문 : 2 |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |


| 샘플 URL |
| --- |
| 1. 3단비교 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=thdCmp&ID=001372&MST=162662&type=HTML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=thdCmp&ID=001570&type=HTML |
| 2. 인용조문 3단비교 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=thdCmp&MST=236231&knd=1&type=XML |
| 2. 위임조문 3단비교 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=thdCmp&MST=222549&knd=2&type=XML |


| 필드 | 값 | 설명 | 기본정보 | string | 인용 삼단비교 기본정보 |
| --- | --- | --- | --- | --- | --- |
| 법령ID | int | 법령 ID |
| 시행령ID | int | 시행령 ID |
| 시행규칙ID | int | 시행규칙 ID |
| 법령명 | string | 법령 명 |
| 시행령명 | string | 법령시행령 명 |
| 시행규칙명 | string | 시행규칙 명 |
| 법령요약정보 | string | 법령 요약정보 |
| 시행령요약정보 | string | 시행령 요약정보 |
| 시행규칙요약정보 | string | 시행규칙 요약정보 |
| 삼단비교기준 | string | 삼단비교 기준 |
| 삼단비교존재여부 | int | 삼단비교 존재하지 않으면 N이 조회. |
| 시행일자 | int | 시행일자 |
| 관련삼단비교목록 | string | 관련 삼단비교 목록 |
| 목록명 | string | 목록명 |
| 삼단비교목록상세링크 | string | 인용조문 삼단비교 목록 상세링크 |
| 인용조문삼단비교 | string | 인용조문 삼단비교 |
| 법률조문 | string | 법률조문 |
| 조번호 | int | 조번호 |
| 조가지번호 | int | 조가지번호 |
| 조제목 | string | 조제목 |
| 조내용 | string | 조내용 |
| 시행령조문목록 | string | 시행령조문목록 |
| 시행령조문 | string | 하위 시행령조문 |
| 시행규칙조문목록 | string | 시행규칙조문목록 |
| 시행규칙조문 | string | 하위 시행규칙조문 |
| 위임행정규칙목록 | string | 위임행정규칙목록 |
| 위임행정규칙 | string | 위임행정규칙 |
| 위임행정규칙명 | string | 위임행정규칙명 |
| 위임행정규칙일련번호 | int | 위임행정규칙일련번호 |
| 위임행정규칙조번호 | int | 위임행정규칙조번호 |
| 위임행정규칙조가지번호 | int | 위임행정규칙조가지번호 |


| 필드 | 값 | 설명 | 기본정보 | string | 위임 삼단비교 기본정보 |
| --- | --- | --- | --- | --- | --- |
| 법령ID | int | 법령 ID |
| 법령일련번호 | int | 법령일련번호 |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 법종구분 | string | 법종 구분 |
| 법령명 | string | 법령 명 |
| 시행일자 | int | 시행일자 |
| 제개정구분 | string | 제개정구분 |
| 삼단비교존재여부 | int | 삼단비교 존재하지 않으면 N이 조회. |
| 기준법법령명 | string | 기준법 법령명 |
| 기준법령목록 | string | 기준 법령 목록 |
| 기준법법령명 | string | 기준법 법령명 |
| 법종구분 | string | 법종 구분 |
| 공포번호 | int | 공포번호 |
| 공포일자 | int | 공포일자 |
| 제개정구분 | string | 제개정구분 |
| 위임3비교상세링크 | string | 위임조문 3비교 목록 상세링크 |
| 위임조문삼단비교 | string | 위임조문 삼단비교 |
| 법률조문 | string | 법률조문 |
| 조번호 | int | 조번호 |
| 조가지번호 | int | 조가지번호 |
| 조제목 | string | 조제목 |
| 조내용 | string | 조내용 |
| 시행령조문 | string | 하위 시행령조문 |
| 시행규칙조문목록 | string | 시행규칙조문목록 |
| 시행규칙조문 | string | 하위 시행규칙조문 |



[HEADING_0] ※ 체계도 등 부가서비스는 법령서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=thdCmp 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 인용조문 출력 결과 필드(response field) [TABLE_2] 위임조문 출력 결과 필드(response field) [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `lsAbrvListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsAbrv`
2. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsAbrv`
3. `http://www.law.go.kr/DRF/lawSearch.do?target=lsAbrv`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsAbrv(필수) | 서비스 대상 |
| type | char | 출력 형태 : XML/JSON |
| stdDt | int | 등록일(검색시작날짜) |
| endDt | int | 등록일(검색종료날짜) |



[TABLE_0]
####  상세 내용


##### 법령명 약칭 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lsAbrv(필수) | 서비스 대상 |
| type | char | 출력 형태 : XML/JSON |
| stdDt | int | 등록일(검색시작날짜) |
| endDt | int | 등록일(검색종료날짜) |


| 샘플 URL |
| --- |
| 1. 법령명 약칭 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsAbrv |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| totalCnt | int | 검색건수 |
| law id | int | 결과 번호 |
| 법령일련번호 | int | 법령일련번호 |
| 현행연혁코드 | string | 현행연혁코드 |
| 법령명한글 | string | 법령명한글 |
| 법령약칭명 | string | 법령약칭명 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | string | 소관부처코드 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 등록일 | int | 등록일 |
| 자법타법여부 | string | 자법타법여부 |
| 법령상세링크 | string | 법령상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lsAbrv 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `datDelHstGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=delHst`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=delHst&knd=13&delDt=20231013`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=delHst&knd=3&frmDt=20231013&toDt=20231016`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 : datDel |
| type | string | 출력 형태 XML/JSON |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| knd | int | 데이터 종류 법령 : 1 행정규칙 : 2 자치법규 : 3 학칙공단 : 13 |
| delDt | int | 데이터 삭제 일자 검색 (YYYYMMDD) |
| frmDttoDt | int | 데이터 삭제 일자 범위 검색 (YYYYMMDD) |



[TABLE_0]
####  상세 내용


##### 삭제 데이터 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 : datDel |
| type | string | 출력 형태 XML/JSON |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| knd | int | 데이터 종류 법령 : 1 행정규칙 : 2 자치법규 : 3 학칙공단 : 13 |
| delDt | int | 데이터 삭제 일자 검색 (YYYYMMDD) |
| frmDttoDt | int | 데이터 삭제 일자 범위 검색 (YYYYMMDD) |


| 샘플 URL |
| --- |
| 1. 삭제데이터 전체 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=delHst |
| 2. 삭제 대학/공공기관규정 날짜 단위(20231013) 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=delHst&knd=13&delDt=20231013 |
| 3. 삭제 자치법규 날짜 범위(20231013~20231016) 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=delHst&knd=3&frmDt=20231013&toDt=20231016 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 일련번호 | int | 데이터 일련번호 |
| 구분명 | string | 데이터 구분명 (법령 / 행정규칙 / 자치법규 등) |
| 삭제일자 | string | 데이터 삭제일자 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=delHst 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `oneViewListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=oneview&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=oneview&type=HTML`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oneview&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : oneview(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |



[TABLE_0]
####  상세 내용


##### 한눈보기 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : oneview(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |


| 샘플 URL |
| --- |
| 1. 한눈보기 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oneview&type=XML |
| 2. 한눈보기 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oneview&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위 |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| 법령 id | int | 검색결과번호 |
| 법령일련번호 | int | 법령일련번호 |
| 법령명 | string | 법령명 |
| 공포일자 | string | 공포일자 |
| 공포번호 | int | 공포번호 |
| 시행일자 | string | 시행일자 |
| 제공건수 | int | 제공건수 |
| 제공일자 | string | 제공일자 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=oneview 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `oneViewInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=oneview&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=oneview&type=XML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=oneview&type=XML&MST=260889&JO=004000`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : oneview(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명 |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| JO | int | 조번호 생략(기본값) : 모든 조를 표시함 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |



[TABLE_0]
####  상세 내용


##### 한눈보기 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : oneview(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| MST | char | 법령 마스터 번호 - 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명 |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| JO | int | 조번호 생략(기본값) : 모든 조를 표시함 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |


| 샘플 URL |
| --- |
| 1. 한눈보기 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=oneview&type=HTML |
| 2. 한눈보기 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=oneview&type=XML |
| 3. 소득세법 시행령 40조 XML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=oneview&type=XML&MST=260889&JO=004000 |


| 필드 | 값 | 설명 | 패턴일련번호 | int | 패턴일련번호 |
| --- | --- | --- | --- | --- | --- |
| 법령일련번호 | int | 법령일련번호 |
| 법령명 | string | 법령명 |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 조문시행일자 | int | 조문시행일자 |
| 최초제공일자 | int | 최초제공일자 |
| 조번호 | int | 조번호 |
| 조제목 | string | 조제목 |
| 콘텐츠제목 | string | 콘텐츠제목 |
| 링크텍스트 | string | 링크텍스트 |
| 링크URL | string | 링크URL |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=oneview 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 행정규칙

### OPEN API 활용가이드

**API ID**: `admrulListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=HTML&query=%ED%95%99%EA%B5%90`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&date=20150301&type=HTML`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&query=학교&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrul(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 (기본 : 1 행정규칙명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 소관부처별 검색(코드별도제공) |
| knd | string | 행정규칙 종류별 검색 (1=훈령/2=예규/3=고시 /4=공고/5=지침/6=기타) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 (기본 : lasc 행정규칙명 오른차순) ldes 행정규칙명 내림차순 dasc : 발령일자 오름차순 ddes : 발령일자 내림차순 nasc : 발령번호 오름차순 ndes : 발령번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 행정규칙 발령일자 |
| prmlYd | string | 발령일자 기간검색(20090101~20090130) |
| modYd | string | 수정일자 기간검색(20090101~20090130) |
| nb | int | 행정규칙 발령번호ex)제2023-8호 검색을 원할시 nb=20238 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 행정규칙 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrul(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 (기본 : 1 행정규칙명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 소관부처별 검색(코드별도제공) |
| knd | string | 행정규칙 종류별 검색 (1=훈령/2=예규/3=고시 /4=공고/5=지침/6=기타) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 (기본 : lasc 행정규칙명 오른차순) ldes 행정규칙명 내림차순 dasc : 발령일자 오름차순 ddes : 발령일자 내림차순 nasc : 발령번호 오름차순 ndes : 발령번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 행정규칙 발령일자 |
| prmlYd | string | 발령일자 기간검색(20090101~20090130) |
| modYd | string | 수정일자 기간검색(20090101~20090130) |
| nb | int | 행정규칙 발령번호ex)제2023-8호 검색을 원할시 nb=20238 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 행정규칙 HTML 목록 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&query=학교&type=HTML |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&date=20150301&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| admrul id | int | 결과 번호 |
| 행정규칙일련번호 | int | 행정규칙일련번호 |
| 행정규칙명 | string | 행정규칙명 |
| 행정규칙종류 | string | 행정규칙종류 |
| 발령일자 | int | 발령일자 |
| 발령번호 | int | 발령번호 |
| 소관부처명 | string | 소관부처명 |
| 현행연혁구분 | string | 현행연혁구분 |
| 제개정구분코드 | string | 제개정구분코드 |
| 제개정구분명 | string | 제개정구분명 |
| 행정규칙ID | int | 행정규칙 |
| 행정규칙상세링크 | string | 행정규칙상세링크 |
| 시행일자 | int | 시행일자 |
| 생성일자 | int | 생성일자 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=admrul 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `admrulInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=62505&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=10000005747&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=62505&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrul(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 행정규칙 일련번호 |
| LID | char | 행정규칙 ID |
| LM | string | 행정규칙명 조회하고자 하는 정확한 행정규칙명을 입력 |



[TABLE_0]
####  상세 내용


##### 행정규칙 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrul(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 행정규칙 일련번호 |
| LID | char | 행정규칙 ID |
| LM | string | 행정규칙명 조회하고자 하는 정확한 행정규칙명을 입력 |


| 샘플 URL |
| --- |
| 1. 행정규칙 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=62505&type=HTML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=10000005747&type=HTML |


| 필드 | 값 | 설명 | 행정규칙일련번호 | int | 행정규칙일련번호 |
| --- | --- | --- | --- | --- | --- |
| 행정규칙명 | string | 행정규칙명 |
| 행정규칙종류 | string | 행정규칙종류 |
| 행정규칙종류코드 | string | 행정규칙종류코드 |
| 발령일자 | int | 발령일자 |
| 발령번호 | string | 발령번호 |
| 제개정구분명 | string | 제개정구분명 |
| 제개정구분코드 | string | 제개정구분코드 |
| 조문형식여부 | string | 조문형식여부 |
| 행정규칙ID | int | 행정규칙 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | string | 소관부처코드 |
| 상위부처명 | string | 상위부처명 |
| 담당부서기관코드 | string | 담당부서기관코드 |
| 담당부서기관명 | string | 담당부서기관명 |
| 담당자명 | string | 담당자명 |
| 전화번호 | string | 전화번호 |
| 현행여부 | string | 현행여부 |
| 시행일자 | string | 시행일자 |
| 생성일자 | string | 생성일자 |
| 조문내용 | string | 조문내용 |
| 부칙 | string | 부칙 |
| 부칙공포일자 | int | 부칙공포일자 |
| 부칙공포번호 | int | 부칙공포번호 |
| 부칙내용 | string | 부칙내용 |
| 별표 | string | 별표 |
| 별표번호 | int | 별표번호 |
| 별표가지번호 | int | 별표가지번호 |
| 별표구분 | string | 별표구분 |
| 별표제목 | string | 별표제목 |
| 별표서식파일링크 | string | 별표서식파일링크 |
| 별표서식PDF파일링크 | string | 별표서식PDF파일링크 |
| 별표내용 | string | 별표내용 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=admrul 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `admrulOldAndNewListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrulOldAndNew&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrulOldAndNew&type=XML&query=119%ED%95%AD%EA%B3%B5%EB%8C%80%20%EC%9A%B4%EC%98%81%20%EA%B7%9C%EC%A0%95`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrulOldAndNew&type=JSON&query=119%ED%95%AD%EA%B3%B5%EB%8C%80%20%EC%9A%B4%EC%98%81%20%EA%B7%9C%EC%A0%95`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrulOldAndNew(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 행정규칙 종류별 검색 (1=훈령/2=예규/3=고시 /4=공고/5=지침/6=기타) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 발령일자 오름차순 ddes : 발령일자 내림차순 nasc : 발령번호 오름차순 ndes : 발령번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | string | 행정규칙 발령일자 |
| prmlYd | string | 발령일자 기간검색(20090101~20090130) |
| nb | int | 행정규칙 발령번호 ex)제2023-8호 검색을 원할시 nb=20238 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 행정규칙 신구법비교 목록 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrulOldAndNew(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 행정규칙 종류별 검색 (1=훈령/2=예규/3=고시 /4=공고/5=지침/6=기타) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션(기본 : lasc 법령오름차순) ldes : 법령내림차순 dasc : 발령일자 오름차순 ddes : 발령일자 내림차순 nasc : 발령번호 오름차순 ndes : 발령번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | string | 행정규칙 발령일자 |
| prmlYd | string | 발령일자 기간검색(20090101~20090130) |
| nb | int | 행정규칙 발령번호 ex)제2023-8호 검색을 원할시 nb=20238 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 행정규칙 신구법비교 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrulOldAndNew&type=HTML |
| 2. 119항공대 운영 규정 신구법비교 XML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrulOldAndNew&type=XML&query=119항공대 운영 규정 |
| 3. 119항공대 운영 규정 신구법비교 JSON 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrulOldAndNew&type=JSON&query=119항공대 운영 규정 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| numOfRows | int | 페이지 당 출력 결과 수 |
| resultCode | int | 조회 여부(성공 : 00 / 실패 : 01) |
| resultMsg | int | 조회 여부(성공 : success / 실패 : fail) |
| oldAndNew id | int | 검색 결과 순번 |
| 신구법일련번호 | int | 신구법 일련번호 |
| 현행연혁구분 | string | 현행연혁코드 |
| 신구법명 | string | 신구법명 |
| 신구법ID | int | 신구법ID |
| 발령일자 | int | 발령일자 |
| 발령번호 | int | 발령번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처코드 | int | 소관부처코드 |
| 소관부처명 | string | 소관부처명 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 신구법상세링크 | string | 신구법 상세링크 |



[HEADING_0] ※ 부가서비스는 행정규칙 서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=admrulOldAndNew 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `admrulOldAndNewInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `http://law.go.kr/DRF/lawService.do?OC=test&target=admrulOldAndNew&ID=2100000248758&type=HTML`
2. `http://law.go.kr/DRF/lawService.do?OC=test&target=admrulOldAndNew&ID=2100000248758&type=XML`
3. `http://law.go.kr/DRF/lawService.do?OC=test&target=admrulOldAndNew&ID=2100000248758&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrulOldAndNew(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 행정규칙 일련번호 (ID 또는 LID 중 하나는 반드시 입력) |
| LID | char | 행정규칙 ID (ID 또는 LID 중 하나는 반드시 입력) |
| LM | string | 행정규칙명 조회하고자 하는 정확한 행정규칙명을 입력 |



[TABLE_0]
####  상세 내용


##### 행정규칙 신구법 본문 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrulOldAndNew(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 행정규칙 일련번호 (ID 또는 LID 중 하나는 반드시 입력) |
| LID | char | 행정규칙 ID (ID 또는 LID 중 하나는 반드시 입력) |
| LM | string | 행정규칙명 조회하고자 하는 정확한 행정규칙명을 입력 |


| 샘플 URL |
| --- |
| 1. 119항공대 운영 규정 신구법비교 HTML 조회 |
| http://law.go.kr/DRF/lawService.do?OC=test&target=admrulOldAndNew&ID=2100000248758&type=HTML |
| 2. 119항공대 운영 규정 신구법비교 XML 조회 |
| http://law.go.kr/DRF/lawService.do?OC=test&target=admrulOldAndNew&ID=2100000248758&type=XML |
| 3. 119항공대 운영 규정 신구법비교 JSON 조회 |
| http://law.go.kr/DRF/lawService.do?OC=test&target=admrulOldAndNew&ID=2100000248758&type=JSON |


| 필드 | 값 | 설명 | 구조문_기본정보 | string | 구조문_기본정보 |
| --- | --- | --- | --- | --- | --- |
| 행정규칙일련번호 | int | 행정규칙일련번호 |
| 행정규칙ID | int | 행정규칙ID |
| 시행일자 | int | 시행일자 |
| 발령일자 | int | 발령일자 |
| 발령번호 | int | 발령번호 |
| 현행여부 | string | 현행여부 |
| 제개정구분명 | string | 제개정구분명 |
| 행정규칙명 | string | 행정규칙명 |
| 행정규칙종류 | string | 행정규칙종류 |
| 신조문_기본정보 | string | 구조문과 동일한 기본 정보 들어가 있음. |
| 구조문목록 | string | 구조문목록 |
| 조문 | string | 조문 |
| 신조문목록 | string | 신조문목록 |
| 조문 | string | 조문 |
| 신구법존재여부 | string | 신구법이 존재하지 않을 경우 N이 조회. |



[HEADING_0] ※ 부가서비스는 행정규칙 서비스 신청을 하면 추가신청 없이 이용가능합니다. - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=admrulOldAndNew 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `admrulBylListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=XML&org=1543000`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admbyl(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 별표서식명) 2 : 해당법령검색 3 : 별표본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별지 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 별표서식 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admbyl(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 별표서식명) 2 : 해당법령검색 3 : 별표본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별지 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 행정규칙 별표서식 목록 XML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=XML |
| 2. 행정규칙 별표서식 목록 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=HTML |
| 3. 농림축산식품부 행정규칙 별표서식 목록 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=XML&org=1543000 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| admrulbyl id | int | 결과번호 |
| 별표일련번호 | int | 별표일련번호 |
| 관련행정규칙일련번호 | int | 관련행정규칙일련번호 |
| 별표명 | string | 별표명ID |
| 관련행정규칙명 | string | 관련행정규칙명 |
| 별표번호 | int | 별표번호 |
| 별표종류 | string | 별표종류 |
| 소관부처명 | string | 소관부처명 |
| 발령일자 | int | 발령일자 |
| 발령번호 | int | 발령번호 |
| 관련법령ID | int | 관련법령ID |
| 행정규칙종류 | string | 행정규칙종류 |
| 별표서식파일링크 | string | 별표서식파일링크 |
| 별표행정규칙상세링크 | string | 별표행정규칙상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=admbyl 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 자치법규

### OPEN API 활용가이드

**API ID**: `ordinListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&query=%EC%B2%AD%EC%86%8C%EB%85%84&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordinfd(필수) | 서비스 대상 |
| org | stinrg(필수) | 기관코드값(예:서울시-6110000) |



[TABLE_0]
####  상세 내용


##### 자치법규 목록 조회 API


###### 분야/분류


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordin(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 (기본 : 1 자치법규명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(defalut=*) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 자치법규오름차순) ldes 자치법규 내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 자치법규 공포일자 검색 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 지자체별 도·특별시·광역시 검색(지자체코드 제공) (ex. 서울특별시에 대한 검색-> org=6110000) |
| sborg | string | 지자체별 시·군·구 검색(지자체코드 제공) (필수값 : org, ex.서울특별시 구로구에 대한 검색-> org=6110000&sborg=3160000) |
| knd | string | 법령종류 (30001-조례 /30002-규칙 /30003-훈령  /30004-예규/30006-기타/30010-고시 /30011-의회규칙) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300208-타법개정 / 300209-타법폐지 300214-기타) |
| ordinFd | int | 분류코드별 검색. 분류코드는 지자체 분야코드 openAPI 참조 |
| lsChapNo | string | 법령분야별 검색(법령분야코드제공) (ex. 제1편 검색 lsChapNo=01000000 / 제1편2장,제1편2장1절 lsChapNo=01020000,01020100) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 자치법규 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&type=XML |
| 2. 자치법규 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&type=HTML |
| 3. 자치법규명에 '청소년'이 포함된 자치법규 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&query=청소년&type=HTML |


| 필드 | 값 | 설명 | 자치법규일련번호 | int | 자치법규일련번호 |
| --- | --- | --- | --- | --- | --- |
| 자치법규명 | string | 자치법규명 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | string | 공포일자 |
| 공포번호 | string | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 지자체기관명 | string | 지자체기관명 |
| 자치법규종류 | string | 자치법규종류 |
| 시행일자 | string | 시행일자 |
| 자치법규상세링크 | string | 자치법규상세링크 |
| 자치법규분야명 | string | 자치법규분야명 |
| 참조데이터구분 | string | 참조데이터구분 |


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordinfd(필수) | 서비스 대상 |
| org | stinrg(필수) | 기관코드값(예:서울시-6110000) |


| 샘플 URL |
| --- |
| 1. 자치법규 분야 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinfd&org=6110000&type=XML |


| 필드 | 값 | 설명 | 기관코드 | string | 기관코드 |
| --- | --- | --- | --- | --- | --- |
| 기관별분류유형CNT | string | 기관별 분류유형 갯수 |
| 분류seq | int | 분류일련번호 |
| 분류명 | string | 분류명 |
| 해당자치법규갯수 | int | 해당자치법규갯수 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=ordin 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [HEADING_1] 요청 변수 (request parameter) [TABLE_3] [TABLE_4] 출력 결과 필드(response field) [TABLE_5] [TABLE_6]

---

### OPEN API 활용가이드

**API ID**: `ordinInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&MST=1316146&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&type=HTML&ID=2026666`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&MST=1316146&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| target | string : ordin(필수) | 서비스 대상 |
| ID | char | 자치법규ID |
| MST | string | 자치법규 일련번호 |



[TABLE_0]
####  상세 내용


##### 자치법규 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| target | string : ordin(필수) | 서비스 대상 |
| ID | char | 자치법규ID |
| MST | string | 자치법규 일련번호 |


| 샘플 URL |
| --- |
| 1. 자치법규 MST 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&MST=1316146&type=HTML |
| 2. 자치법규 ID 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&ID=2026666&type=HTML |


| 필드 | 값 | 설명 | 자치법규ID | int | 자치법규ID |
| --- | --- | --- | --- | --- | --- |
| 자치법규일련번호 | string | 자치법규일련번호 |
| 공포일자 | string | 공포일자 |
| 공포번호 | string | 공포번호 |
| 자치법규명 | string | 자치법규명 |
| 시행일자 | string | 시행일자 |
| 자치법규종류 | string | 자치법규종류 (C0001-조례 /C0002-규칙 /C0003-훈령  /C0004-예규/C0006-기타/C0010-고시 /C0011-의회규칙) |
| 지자체기관명 | string | 지자체기관명 |
| 담당부서명 | string | 담당부서명 |
| 전화번호 | string | 전화번호 |
| 제개정정보 | string | 제개정정보 |
| 조문번호 | string | 조문번호 |
| 조문여부 | string | 해당 조문이 조일때 Y,그 외 편,장,절,관 일때는 N |
| 조제목 | string | 조제목 |
| 조내용 | string | 조내용 |
| 부칙공포일자 | int | 부칙공포일자 |
| 부칙공포번호 | int | 부칙공포번호 |
| 부칙내용 | string | 부칙내용 |
| 부칙내용 | string | 부칙내용 |
| 별표 | string | 별표 (자치법규 별표는 서울시교육청과 본청만 제공합니다.) |
| 별표번호 | int | 별표번호 |
| 별표가지번호 | int | 별표가지번호 |
| 별표구분 | string | 별표구분 |
| 별표제목 | string | 별표제목 |
| 별표첨부파일명 | string | 별표첨부파일명 |
| 별표내용 | string | 별표내용 |
| 개정문내용 | string | 개정문내용 |
| 제개정이유내용 | string | 제개정이유내용 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=ordin 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `ordinLsConListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkOrd&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkOrd&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkOrd&type=XML&query=%EC%B2%AD%EC%86%8C%EB%85%84`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lnkOrg(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 지자체 기관코드 (지자체코드 제공) |
| sort | string | (기본 : lasc 자치법규오름차순) ldes 자치법규 내림차순 dasc : 공포일자 오름차순  ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 자치법규 법령 연계 목록 조회 API


###### 연계 조례 목록 조회 API


###### 연계 법령별 조례 목록 조회 API


###### 연계 조례 지자체별 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lnkOrd(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 법규명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 자치법규오름차순) ldes 자치법규 내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 연계 조례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkOrd&type=XML |
| 2. 연계 조례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkOrd&type=HTML |
| 3. 연계 조례 검색 : 청소년 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkOrd&type=XML&query=청소년 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 자치법규일련번호 | int | 자치법규 일련번호 |
| 자치법규명 | string | 자치법규명 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 자치법규종류 | string | 자치법규종류 |
| 시행일자 | int | 시행일자 |


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lnkLsOrd(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | (기본 : lasc 자치법규오름차순) ldes 자치법규 내림차순 dasc : 공포일자 오름차순  ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 |
| knd | string | 법령종류(코드제공)법령ID 사용함 |


| 샘플 URL |
| --- |
| 1. 법령이 '건축법 시행령'인 연계 조례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLsOrd&knd=002118&type=XML |
| 2. 법령이 '건축법 시행령'인 연계 조례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkLsOrd&knd=002118&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 자치법규일련번호 | int | 자치법규 일련번호 |
| 자치법규명 | string | 자치법규명 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 자치법규종류 | string | 자치법규종류 |
| 시행일자 | int | 시행일자 |


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lnkOrg(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 지자체 기관코드 (지자체코드 제공) |
| sort | string | (기본 : lasc 자치법규오름차순) ldes 자치법규 내림차순 dasc : 공포일자 오름차순  ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 지자체가 '부산광역시 동구'인 연계 조례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkOrg&org=3270000&type=XML |
| 2. 지자체가 '부산광역시 동구'인 연계 조례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lnkOrg&org=3270000&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 자치법규일련번호 | int | 자치법규 일련번호 |
| 자치법규명 | string | 자치법규명 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 자치법규종류 | string | 자치법규종류 |
| 시행일자 | int | 시행일자 |
| 법령명한글 | string | 법령명한글 |
| 법령ID | int | 법령ID |



[HEADING_0] [HEADING_1] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lnkOrd 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [HEADING_2] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lnkLsOrd 요청 변수 (request parameter) [TABLE_3] [TABLE_4] 출력 결과 필드(response field) [TABLE_5] [HEADING_3] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lnkOrg 요청 변수 (request parameter) [TABLE_6] [TABLE_7] 출력 결과 필드(response field) [TABLE_8]

---

### OPEN API 활용가이드

**API ID**: `ordinBylListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=HTML`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordinbyl(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| search | int | 검색범위(기본 : 1 별표서식명) 2 : 해당자치법규명검색 3 : 별표본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| sborg | string | 지자체별 시·군·구 검색(지자체코드 제공) (필수값 : org, ex.서울특별시 구로구에 대한 검색-> org=6110000&sborg=3160000) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별도 4 : 별지 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 별표서식 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordinbyl(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| search | int | 검색범위(기본 : 1 별표서식명) 2 : 해당자치법규명검색 3 : 별표본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| sborg | string | 지자체별 시·군·구 검색(지자체코드 제공) (필수값 : org, ex.서울특별시 구로구에 대한 검색-> org=6110000&sborg=3160000) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별도 4 : 별지 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 자치법규 별표서식 목록 XML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=XML |
| 2. 자치법규 별표서식 목록 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 현재 페이지번호 |
| ordinbyl id | int | 검색 결과 순번 |
| 별표일련번호 | string | 별표일련번호 |
| 관련자치법규일련번호 | string | 관련자치법규일련번호 |
| 별표명 | string | 별표명 |
| 관련자치법규명 | string | 관련자치법규명 |
| 별표번호 | string | 별표번호 |
| 별표종류 | string | 별표종류 |
| 지자체기관명 | string | 지자체기관명 |
| 전체기관명 | string | 전체기관명 |
| 자치법규시행일자 | string | 자치법규시행일자 |
| 공포일자 | string | 공포일자 |
| 공포번호 | string | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 별표서식파일링크 | string | 별표서식파일링크 |
| 별표자치법규상세링크 | string | 별표자치법규상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=ordinbyl 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 판례관련

### OPEN API 활용가이드

**API ID**: `precListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=XML&query=%EB%8B%B4%EB%B3%B4%EA%B6%8C`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=HTML&query=%EB%8B%B4%EB%B3%B4%EA%B6%8C&curt=%EB%8C%80%EB%B2%95%EC%9B%90`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=HTML&nb=2009%EB%8A%90%ED%95%A9133,2010%EB%8A%90%ED%95%A921`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : prec(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 판례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 법원종류 (대법원:400201, 하위법원:400202) |
| curt | string | 법원명 (대법원, 서울고등법원, 광주지법, 인천지방법원) |
| JO | string | 참조법령명(형법, 민법 등) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 ldes : 사건명 내림차순 dasc : 선고일자 오름차순 ddes : 선고일자 내림차순(생략시 기본) nasc : 법원명 오름차순 ndes : 법원명 내림차순 |
| date | int | 판례 선고일자 |
| prncYd | string | 선고일자 검색(20090101~20090130) |
| nb | string | 판례 사건번호 |
| datSrcNm | string | 데이터출처명(국세법령정보시스템, 근로복지공단산재판례, 대법원) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 판례 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : prec(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 판례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 법원종류 (대법원:400201, 하위법원:400202) |
| curt | string | 법원명 (대법원, 서울고등법원, 광주지법, 인천지방법원) |
| JO | string | 참조법령명(형법, 민법 등) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 ldes : 사건명 내림차순 dasc : 선고일자 오름차순 ddes : 선고일자 내림차순(생략시 기본) nasc : 법원명 오름차순 ndes : 법원명 내림차순 |
| date | int | 판례 선고일자 |
| prncYd | string | 선고일자 검색(20090101~20090130) |
| nb | string | 판례 사건번호 |
| datSrcNm | string | 데이터출처명(국세법령정보시스템, 근로복지공단산재판례, 대법원) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 사건명에 '담보권'이 들어가는 판례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=XML&query=담보권 |
| 2. 사건명에 '담보권'이 들어가고 법원이 '대법원'인 판례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=HTML&query=담보권&curt=대법원 |
| 3. 사건번호가 '2009느합133,2010느합21' 인 판례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=HTML&nb=2009느합133,2010느합21 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 공포번호 | string | 공포번호 |
| 키워드 | string | 검색어 |
| section | string | 검색범위(EvtNm:판례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| prec id | int | 검색결과번호 |
| 판례일련번호 | int | 판례일련번호 |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 선고일자 | string | 선고일자 |
| 법원명 | string | 법원명 |
| 법원종류코드 | int | 법원종류코드(대법원:400201, 하위법원:400202) |
| 사건종류명 | string | 사건종류명 |
| 사건종류코드 | int | 사건종류코드 |
| 판결유형 | string | 판결유형 |
| 선고 | string | 선고 |
| 데이터출처명 | string | 데이터출처명 |
| 판례상세링크 | string | 판례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=prec 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `precInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=prec&ID=228541&type=HTML`
2. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=prec&ID=228541&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?target=prec`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : prec(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON *국세청 판례 본문 조회는 HTML만 가능합니다 |
| ID | char(필수) | 판례 일련번호 |
| LM | string | 판례명 |



[TABLE_0]
####  상세 내용


##### 판례 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : prec(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON *국세청 판례 본문 조회는 HTML만 가능합니다 |
| ID | char(필수) | 판례 일련번호 |
| LM | string | 판례명 |


| 샘플 URL |
| --- |
| 1. 판례일련번호가 228541인 판례 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=prec&ID=228541&type=HTML |


| 필드 | 값 | 설명 | 판례정보일련번호 | int | 판례정보일련번호 |
| --- | --- | --- | --- | --- | --- |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 선고일자 | int | 선고일자 |
| 선고 | string | 선고 |
| 법원명 | string | 법원명 |
| 법원종류코드 | int | 법원종류코드(대법원:400201, 하위법원:400202) |
| 사건종류명 | string | 사건종류명 |
| 사건종류코드 | int | 사건종류코드 |
| 판결유형 | string | 판결유형 |
| 판시사항 | string | 판시사항 |
| 판결요지 | string | 판결요지 |
| 참조조문 | string | 참조조문 |
| 참조판례 | string | 참조판례 |
| 판례내용 | string | 판례내용 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=prec 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `detcListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML&query=%EB%B2%8C%EA%B8%88`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=HTML&date=20150210`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML&query=%EC%9E%90%EB%8F%99%EC%B0%A8`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : detc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 헌재결정례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 (기본 : lasc 사건명 오름차순) ldes 사건명 내림차순 dasc : 선고일자 오름차순 ddes : 선고일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 efasc : 종국일자 오름차순 efdes : 종국일자 내림차순 |
| date | int | 종국일자 |
| edYd | string | 종국일자 기간 검색 |
| nb | int | 사건번호 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 헌재결정례 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : detc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 헌재결정례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 (기본 : lasc 사건명 오름차순) ldes 사건명 내림차순 dasc : 선고일자 오름차순 ddes : 선고일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 efasc : 종국일자 오름차순 efdes : 종국일자 내림차순 |
| date | int | 종국일자 |
| edYd | string | 종국일자 기간 검색 |
| nb | int | 사건번호 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 사건명에 '벌금'이 들어가는 헌재결정례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML&query=벌금 |
| 2. 종국일자가 '2015년 2월 10일'인 헌재결정례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=HTML&date=20150210 |
| 3. 사건명에 '자동차'가 포함된 헌재결정례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML&query=자동차 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(EvtNm:헌재결정례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| detc id | int | 검색결과번호 |
| 헌재결정례일련번호 | int | 헌재결정례일련번호 |
| 종국일자 | string | 종국일자 |
| 사건번호 | string | 사건번호 |
| 사건명 | string | 사건명 |
| 헌재결정례상세링크 | string | 헌재결정례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=detc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `detcInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=58386&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=127830&LM=자동차관리법제26조등위헌확인등&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=58386&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : detc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 헌재결정례 일련번호 |
| LM | string | 헌재결정례명 |



[TABLE_0]
####  상세 내용


##### 헌재결정례 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : detc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 헌재결정례 일련번호 |
| LM | string | 헌재결정례명 |


| 샘플 URL |
| --- |
| 1. 헌재결정례 일련번호가 58386인 헌재결정례 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=58386&type=HTML |
| 2. 자동차관리법제26조등위헌확인등 헌재결정례 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=127830&LM=자동차관리법제26조등위헌확인등&type=HTML |


| 필드 | 값 | 설명 | 헌재결정례일련번호 | int | 헌재결정례일련번호 |
| --- | --- | --- | --- | --- | --- |
| 종국일자 | int | 종국일자 |
| 사건번호 | string | 사건번호 |
| 사건명 | string | 사건명 |
| 사건종류명 | string | 사건종류명 |
| 사건종류코드 | int | 사건종류코드 |
| 재판부구분코드 | int | 재판부구분코드(전원재판부:430201, 지정재판부:430202) |
| 판시사항 | string | 판시사항 |
| 결정요지 | string | 결정요지 |
| 전문 | string | 전문 |
| 참조조문 | string | 참조조문 |
| 참조판례 | string | 참조판례 |
| 심판대상조문 | string | 심판대상조문 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=detc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `expcListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=XML&query=%EC%9E%84%EC%B0%A8`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=HTML&query=%EC%A3%BC%EC%B0%A8`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=XML&query=%EC%9E%90%EB%8F%99%EC%B0%A8`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : expc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | inq | 질의기관 |
| rpl | int | 회신기관 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호13-0217 검색을 원할시 itmno=130217 |
| regYd | string | 등록일자 검색(20090101~20090130) |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석례명 오름차순) ldes 법령해석례명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 법령해석례 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : expc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | inq | 질의기관 |
| rpl | int | 회신기관 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호13-0217 검색을 원할시 itmno=130217 |
| regYd | string | 등록일자 검색(20090101~20090130) |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석례명 오름차순) ldes 법령해석례명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 안건명에 '임차'가 들어가는 법령해석례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=XML&query=임차 |
| 2. 안건명에 '주차'가 들어가는 법령해석례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=HTML&주차 |
| 3. 안건명에 '자동차'가 들어가는 법령해석례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=XML&query=자동차 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| expc id | int | 검색결과번호 |
| 법령해석례일련번호 | int | 법령해석례일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 회신기관코드 | string | 회신기관코드 |
| 회신기관명 | string | 회신기관명 |
| 회신일자 | string | 회신일자 |
| 법령해석례상세링크 | string | 법령해석례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=expc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `expcInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=334617&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=315191&LM=%EC%97%AC%EC%84%B1%EA%B0%80%EC%A1%B1%EB%B6%80%20-%20%EA%B1%B4%EA%B0%95%EA%B0%80%EC%A0%95%EA%B8%B0%EB%B3%B8%EB%B2%95%20%EC%A0%9C35%EC%A1%B0%20%EC%A0%9C2%ED%95%AD%20%EA%B4%80%EB%A0%A8&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=334617&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : expc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석례 일련번호 |
| LM | string | 법령해석례명 |



[TABLE_0]
####  상세 내용


##### 법령해석례 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : expc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석례 일련번호 |
| LM | string | 법령해석례명 |


| 샘플 URL |
| --- |
| 1. 법령해석례일련번호가 333827인 해석례 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=334617&type=HTML |
| 2. 여성가족부 - 건강가정기본법 제35조 제2항 관련 법령해석례 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=315191&LM=여성가족부 - 건강가정기본법 제35조 제2항 관련&type=HTML |


| 필드 | 값 | 설명 | 법령해석례일련번호 | int | 법령해석례일련번호 |
| --- | --- | --- | --- | --- | --- |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 해석일자 | int | 해석일자 |
| 해석기관코드 | int | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 관리기관코드 | int | 관리기관코드 |
| 등록일시 | int | 등록일시 |
| 질의요지 | string | 질의요지 |
| 회답 | string | 회답 |
| 이유 | string | 이유 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=expc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `deccListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=decc&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=decc&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=decc&type=XML&gana=ga`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : decc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 행정심판례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| cls | string | 재결례유형(출력 결과 필드에 있는 재결구분코드) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| date | int | 의결일자 |
| dpaYd | string | 처분일자 검색(20090101~20090130) |
| rslYd | string | 의결일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 재결례명 오름차순) ldes 재결례명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 행정심판례 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : decc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 행정심판례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| cls | string | 재결례유형(출력 결과 필드에 있는 재결구분코드) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| date | int | 의결일자 |
| dpaYd | string | 처분일자 검색(20090101~20090130) |
| rslYd | string | 의결일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 재결례명 오름차순) ldes 재결례명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 행정심판재결례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=decc&type=XML |
| 2. 행정심판재결례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=decc&type=HTML |
| 3. 행정심판재결례 목록 중 ‘ㄱ’으로 시작하는 재결례 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=decc&type=XML&gana=ga |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(EvtNm:재결례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| decc id | int | 검색결과번호 |
| 행정심판재결례일련번호 | int | 행정심판재결례일련번호 |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 처분일자 | string | 처분일자 |
| 의결일자 | string | 의결일자 |
| 처분청 | string | 처분청 |
| 재결청 | int | 재결청 |
| 재결구분명 | string | 재결구분명 |
| 재결구분코드 | string | 재결구분코드 |
| 행정심판례상세링크 | string | 행정심판례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=decc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `deccInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=decc&ID=243263&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=decc&ID=245011&LM=과징금 부과처분 취소청구&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=decc&ID=243263&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : decc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 행정심판례 일련번호 |
| LM | string | 행정심판례명 |



[TABLE_0]
####  상세 내용


##### 행정심판례 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : decc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 행정심판례 일련번호 |
| LM | string | 행정심판례명 |


| 샘플 URL |
| --- |
| 1. 행정심판례 일련번호가 243263인 행정심판례 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=decc&ID=243263&type=HTML |
| 2. 감리업무정지처분취소청구 행정심판례 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=decc&ID=245011&LM=과징금 부과처분 취소청구&type=HTML |


| 필드 | 값 | 설명 | 행정심판례일련번호 | int | 행정심판례일련번호 |
| --- | --- | --- | --- | --- | --- |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 처분일자 | int | 처분일자 |
| 의결일자 | int | 의결일자 |
| 처분청 | string | 처분청 |
| 재결청 | string | 재결청 |
| 재결례유형명 | string | 재결례유형명 |
| 재결례유형코드 | int | 재결례유형코드 |
| 주문 | string | 주문 |
| 청구취지 | string | 청구취지 |
| 이유 | string | 이유 |
| 재결요지 | string | 재결요지 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=decc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

## 위원회결정문

### OPEN API 활용가이드

**API ID**: `ppcListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ppc&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ppc&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ppc&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (개인정보보호위원회 : ppc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 안건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 안건명 오름차순 (default) ldes : 안건명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 의안번호 오름차순 ndes : 의안번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 개인정보보호위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (개인정보보호위원회 : ppc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 안건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 안건명 오름차순 (default) ldes : 안건명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 의안번호 오름차순 ndes : 의안번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 개인정보보호위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ppc&type=HTML |
| 2. 개인정보보호위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ppc&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| ppc id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 안건명 | string | 안건명 |
| 의안번호 | string | 의안번호 |
| 회의종류 | string | 회의종류 |
| 결정구분 | string | 결정구분 |
| 의결일 | string | 의결일 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=ppc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `ppcInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ppc&ID=5&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ppc&ID=3&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=ppc&ID=5&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (개인정보보호위원회 : ppc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 개인정보보호위원회 위원회 결정문 본문 조회 API


###### 개인정보보호위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (개인정보보호위원회 : ppc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 개인정보보호위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=ppc&ID=5&type=HTML |
| 2. 개인정보보호위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=ppc&ID=3&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 기관명 | string | 기관명 |
| 결정 | string | 결정 |
| 회의종류 | string | 회의종류 |
| 안건번호 | string | 안건번호 |
| 안건명 | string | 안건명 |
| 신청인 | string | 신청인 |
| 의결연월일 | string | 의결연월일 |
| 주문 | string | 주문 |
| 이유 | string | 이유 |
| 배경 | string | 배경 |
| 이의제기방법및기간 | string | 이의제기방법및기간 |
| 주요내용 | string | 주요내용 |
| 의결일자 | string | 의결일자 |
| 위원서명 | string | 위원서명 |
| 별지 | string | 별지 |
| 결정요지 | string | 결정요지 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=ppc [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `eiacListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=eiac&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=eiac&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eiac&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (고용보험심사위원회 : eiac) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 (default) ldes : 사건명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 고용보험심사위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (고용보험심사위원회 : eiac) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 (default) ldes : 사건명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 고용보험심사위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eiac&type=HTML |
| 2. 고용보험심사위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=eiac&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| eiac id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 의결일자 | string | 의결일자 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=eiac 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `eiacInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=eiac&ID=11347&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=eiac&ID=11327&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=eiac&ID=11347&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (고용보험심사위원회 : eiac) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 고용보험심사위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (고용보험심사위원회 : eiac) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 고용보험심사위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=eiac&ID=11347&type=HTML |
| 2. 고용보험심사위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=eiac&ID=11327&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 사건의분류 | string | 사건의 분류 |
| 의결서종류 | string | 의결서 종류 |
| 개요 | string | 개요 |
| 사건번호 | string | 사건번호 |
| 사건명 | string | 사건명 |
| 청구인 | string | 청구인 |
| 대리인 | string | 대리인 |
| 피청구인 | string | 피청구인 |
| 이해관계인 | string | 이해관계인 |
| 심사결정심사관 | string | 심사결정심사관 |
| 주문 | string | 주문 |
| 청구취지 | string | 청구취지 |
| 이유 | string | 이유 |
| 의결일자 | string | 의결일자 |
| 기관명 | string | 기관명 |
| 별지 | string | 별지 |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=eiac 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(의결서, response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `ftcListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ftc&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ftc&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ftc&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (공정거래위원회 : ftc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 (default) ldes : 사건명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 공정거래위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (공정거래위원회 : ftc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 (default) ldes : 사건명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 공정거래위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ftc&type=HTML |
| 2. 공정거래위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ftc&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| ftc id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 문서유형 | string | 문서유형 |
| 회의종류 | string | 회의종류 |
| 결정번호 | string | 결정번호 |
| 결정일자 | string | 결정일자 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=ftc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `ftcInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ftc&ID=331&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ftc&ID=335&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=ftc&ID=331&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (공정거래위원회 : ftc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 공정거래위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (공정거래위원회 : ftc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 공정거래위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=ftc&ID=331&type=HTML |
| 2. 공정거래위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=ftc&ID=335&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 문서유형 | string | 출력 형태 : 의결서 / 시정권고서 |
| 사건번호 | string | 사건번호 |
| 사건명 | string | 사건명 |
| 피심정보명 | string | 피심정보명 |
| 피심정보내용 | string | 피심정보내용 |
| 회의종류 | string | 회의종류 |
| 결정번호 | string | 결정번호 |
| 결정일자 | string | 결정일자 |
| 원심결 | string | 원심결 |
| 재산정심결 | string | 재산정심결 |
| 후속심결 | string | 후속심결 |
| 심의정보명 | string | 심의정보명 |
| 심의정보내용 | string | 심의정보내용 |
| 의결문 | string | 의결문 |
| 주문 | string | 주문 |
| 신청취지 | string | 신청취지 |
| 이유 | string | 이유 |
| 의결일자 | string | 의결일자 |
| 위원정보 | string | 위원정보 |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |
| 별지 | string | 별지 |
| 결정요지 | string | 결정요지 |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 문서유형 | string | 출력 형태 : 의결서 / 시정권고서 |
| 사건번호 | string | 사건번호 |
| 사건명 | string | 사건명 |
| 피심정보명 | string | 피심정보명 |
| 피심정보내용 | string | 피심정보내용 |
| 의결서종류 | string | 의결서종류 |
| 시정권고참조법률 | string | 시정권고참조법률 |
| 시정권고사항 | string | 시정권고사항 |
| 시정권고이유 | string | 시정권고이유 |
| 법위반내용 | string | 법위반내용 |
| 적용법조 | string | 적용법조 |
| 법령의적용 | string | 법령의적용 |
| 시정기한 | string | 시정기한 |
| 수락여부통지기간 | string | 수락여부통지기간 |
| 수락여부통지기한 | string | 수락여부통지기한 |
| 수락거부시의조치 | string | 수락거부시의조치 |
| 수락거부시조치방침 | string | 수락거부시조치방침 |
| 별지 | string | 별지 |
| 결정요지 | string | 결정요지 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=ftc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(의결서, response field) [TABLE_2] 출력 결과 필드(시정권고서, response field) [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `acrListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=acr&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=acr&type=XML`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=acr&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (국민권익위원회 : acr) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 민원표시 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 민원표시 오름차순 (default) ldes : 민원표시 내림차순 dasc : 의결일 오름차순 ddes : 의결일 내림차순 nasc : 의안번호 오름차순 ndes : 의안번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 국민권익위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (국민권익위원회 : acr) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 민원표시 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 민원표시 오름차순 (default) ldes : 민원표시 내림차순 dasc : 의결일 오름차순 ddes : 의결일 내림차순 nasc : 의안번호 오름차순 ndes : 의안번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 국민권익위원회 결정문 HTML 목록 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=acr&type=HTML |
| 2. 국민권익위원회 결정문 XML 목록 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=acr&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 기관명 |
| acr id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 제목 | string | 제목 |
| 민원표시명 | string | 민원표시명 |
| 의안번호 | string | 의안번호 |
| 회의종류 | string | 회의종류 |
| 결정구분 | string | 결정구분 |
| 의결일 | string | 의결일 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=acr 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `acrInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=acr&ID=53&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=acr&ID=89&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=acr&ID=53&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (국민권익위원회 : acr) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 국민권익위원회 결정문 본문 조회 API


###### 국민권익위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (국민권익위원회 : acr) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 국민권익위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=acr&ID=53&type=HTML |
| 2. 국민권익위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=acr&ID=89&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 기관명 | string | 기관명 |
| 회의종류 | string | 회의종류 |
| 결정구분 | string | 결정구분 |
| 의안번호 | string | 의안번호 |
| 민원표시 | string | 민원표시 |
| 제목 | string | 제목 |
| 신청인 | string | 신청인 |
| 대리인 | string | 대리인 |
| 피신청인 | string | 피신청인 |
| 관계기관 | string | 관계기관 |
| 의결일 | string | 의결일 |
| 주문 | string | 주문 |
| 이유 | string | 이유 |
| 별지 | string | 별지 |
| 의결문 | string | 의결문 |
| 의결일자 | string | 의결일자 |
| 위원정보 | string | 위원정보 |
| 결정요지 | string | 결정요지 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=acr [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `fscListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=fsc&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=fsc&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=fsc&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (금융위원회 : fsc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 안건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 안건명 오름차순 (default) ldes : 안건명 내림차순 nasc : 의결번호 오름차순 ndes : 의결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 금융위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (금융위원회 : fsc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 안건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 안건명 오름차순 (default) ldes : 안건명 내림차순 nasc : 의결번호 오름차순 ndes : 의결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 금융위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=fsc&type=HTML |
| 2. 금융위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=fsc&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| fsc id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 안건명 | string | 안건명 |
| 의결번호 | string | 의결번호 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=fsc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `fscInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=fsc&ID=9211&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=fsc&ID=9169&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=fsc&ID=9211&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (금융위원회 : fsc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 금융위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (금융위원회 : fsc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 금융위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=fsc&ID=9211&type=HTML |
| 2. 금융위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=fsc&ID=13097&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 기관명 | string | 기관명 |
| 의결번호 | string | 의결번호 |
| 안건명 | string | 안건명 |
| 조치대상자의인적사항 | string | 조치대상자의 인적사항 |
| 조치대상 | string | 조치대상 |
| 조치내용 | string | 조치내용 |
| 조치이유 | string | 조치이유 |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=fsc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(의결서, response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `nlrcListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=nlrc&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=nlrc&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=nlrc&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (노동위원회 : nlrc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 제목 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 제목 오름차순 (default) ldes : 제목 내림차순 dasc : 등록일 오름차순 ddes : 등록일 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 노동위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (노동위원회 : nlrc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 제목 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 제목 오름차순 (default) ldes : 제목 내림차순 dasc : 등록일 오름차순 ddes : 등록일 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 노동위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=nlrc&type=HTML |
| 2. 노동위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=nlrc&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| nlrc id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 제목 | string | 제목 |
| 사건번호 | string | 사건번호 |
| 등록일 | string | 등록일 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=nlrc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `nlrcInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=nlrc&ID=55&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=nlrc&ID=71&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=nlrc&ID=55&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (노동위원회 : nlrc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 노동위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (노동위원회 : nlrc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 노동위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=nlrc&ID=55&type=HTML |
| 2. 노동위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=nlrc&ID=71&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 기관명 | string | 기관명 |
| 사건번호 | string | 사건번호 |
| 자료구분 | string | 자료구분 |
| 담당부서 | string | 담당부서 |
| 등록일 | string | 등록일 |
| 제목 | string | 제목 |
| 내용 | string | 내용 |
| 판정사항 | string | 판정사항 |
| 판정요지 | string | 판정요지 |
| 판정결과 | string | 판정결과 |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=nlrc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `kccListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcc&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcc&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcc&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (방송통신위원회 : kcc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 안건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 안건명 오름차순 (default) ldes : 안건명 내림차순 dasc : 의결연월일 오름차순 ddes : 의결연월일 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 방송통신위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (방송통신위원회 : kcc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 안건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 안건명 오름차순 (default) ldes : 안건명 내림차순 dasc : 의결연월일 오름차순 ddes : 의결연월일 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 방송통신위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcc&type=HTML |
| 2. 방송통신위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcc&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| kcc id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 의결일자 | string | 의결일자 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=kcc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `kccInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=kcc&ID=12549&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=kcc&ID=12547&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=kcc&ID=12549&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (방송통신위원회 : kcc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 방송통신위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (방송통신위원회 : kcc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 방송통신위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=kcc&ID=12549&type=HTML |
| 2. 방송통신위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=kcc&ID=12547&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 기관명 | string | 기관명 |
| 의결서유형 | string | 의결서 유형 |
| 안건번호 | string | 안건번호 |
| 사건번호 | string | 사건번호 |
| 안건명 | string | 안건명 |
| 사건명 | string | 사건명 |
| 피심인 | string | 피심인 |
| 피심의인 | string | 피심의인 |
| 청구인 | string | 청구인 |
| 참고인 | string | 참고인 |
| 원심결정 | string | 원심결정 |
| 의결일자 | string | 의결일자 |
| 주문 | string | 주문 |
| 이유 | string | 이유 |
| 별지 | string | 별지 |
| 문서제공구분 | string | 문서제공구분(데이터 개방|이유하단 이미지개방) |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=kcc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `iaciacListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=iaciac&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=iaciac&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=iaciac&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (산업재해보상보험재심사위원회 : iaciac) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건 오름차순 (default) ldes : 사건 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 산업재해보상보험재심사위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (산업재해보상보험재심사위원회 : iaciac) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건 오름차순 (default) ldes : 사건 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 산업재해보상보험재심사위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=iaciac&type=HTML |
| 2. 산업재해보상보험재심사위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=iaciac&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| iaciac id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 사건 | string | 시건 |
| 사건번호 | string | 사건번호 |
| 의결일자 | string | 의결일자 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=iaciac 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `iaciacInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=iaciac&ID=7515&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=iaciac&ID=7513&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=iaciac&ID=7515&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (산업재해보상보험재심사위원회 : iaciac) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 산업재해보상보험재심사위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (산업재해보상보험재심사위원회 : iaciac) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 산업재해보상보험재심사위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=iaciac&ID=7515&type=HTML |
| 2. 산업재해보상보험재심사위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=iaciac&ID=7513&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 사건대분류 | string | 사건 대분류 |
| 사건중분류 | string | 사건 중분류 |
| 사건소분류 | string | 사건 소분류 |
| 쟁점 | string | 쟁점 |
| 사건번호 | string | 사건번호 |
| 의결일자 | string | 의결일자 |
| 사건 | string | 사건 |
| 청구인 | string | 청구인 |
| 재해근로자 | string | 재해근로자 |
| 재해자 | string | 재해자 |
| 피재근로자 | string | 피재근로자/피재자성명/피재자/피재자(망인) |
| 진폐근로자 | string | 진폐근로자 |
| 수진자 | string | 수진자 |
| 원처분기관 | string | 원처분기관 |
| 주문 | string | 주문 |
| 청구취지 | string | 청구취지 |
| 이유 | string | 이유 |
| 별지 | string | 별지 |
| 문서제공구분 | string | 문서제공구분(데이터 개방|이유하단 이미지개방) |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=iaciac 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(의결서, response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `ocltListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=oclt&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=oclt&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oclt&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (중앙토지수용위원회 : oclt) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 제목 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 제목 오름차순 (default) ldes : 제목 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 중앙토지수용위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (중앙토지수용위원회 : oclt) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 제목 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 제목 오름차순 (default) ldes : 제목 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 중앙토지수용위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oclt&type=HTML |
| 2. 중앙토지수용위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=oclt&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| oclt id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 제목 | string | 제목 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=oclt 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `ocltInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=oclt&ID=4973&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=oclt&ID=4965&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=oclt&ID=4973&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (중앙토지수용위원회 : oclt) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 중앙토지수용위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (중앙토지수용위원회 : oclt) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 중앙토지수용위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=oclt&ID=4973&type=HTML |
| 2. 중앙토지수용위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=oclt&ID=4965&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 제목 | string | 제목 |
| 관련법리 | string | 관련 법리 |
| 관련규정 | string | 관련 규정 |
| 판단 | string | 판단 |
| 근거 | string | 근거 |
| 주해 | string | 주해 |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=oclt 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(의결서, response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `eccListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ecc&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ecc&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ecc&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (중앙환경분쟁조정위원회 : ecc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 (default) ldes : 사건명 내림차순 nasc : 의결번호 오름차순 ndes : 의결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 중앙환경분쟁조정위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (중앙환경분쟁조정위원회 : ecc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 (default) ldes : 사건명 내림차순 nasc : 의결번호 오름차순 ndes : 의결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 중앙환경분쟁조정위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ecc&type=HTML |
| 2. 중앙환경분쟁조정위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ecc&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| ecc id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 사건명 | string | 사건명 |
| 의결번호 | string | 의결번호 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=ecc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `eccInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ecc&ID=5883&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ecc&ID=5877&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=ecc&ID=5883&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (중앙환경분쟁조정위원회 : ecc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 중앙환경분쟁조정위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (중앙환경분쟁조정위원회 : ecc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 중앙환경분쟁조정위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=ecc&ID=5883&type=HTML |
| 2. 중앙환경분쟁조정위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=ecc&ID=5877&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 의결번호 | string | 의결번호 |
| 사건명 | string | 사건명 |
| 사건의개요 | string | 사건의 개요 |
| 신청인 | string | 신청인 |
| 피신청인 | string | 피신청인 |
| 분쟁의경과 | string | 분쟁의 경과 |
| 당사자주장 | string | 당사자 주장 |
| 사실조사결과 | string | 사실조사 결과 |
| 평가의견 | string | 평가의견 |
| 주문 | string | 주문 |
| 이유 | string | 이유 |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=ecc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(의결서, response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `sfcListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=sfc&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=sfc&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=sfc&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (증권선물위원회 : sfc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 안건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 안건명 오름차순 (default) ldes : 안건명 내림차순 nasc : 의결번호 오름차순 ndes : 의결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 증권선물위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (증권선물위원회 : sfc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 안건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 안건명 오름차순 (default) ldes : 안건명 내림차순 nasc : 의결번호 오름차순 ndes : 의결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 증권선물위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=sfc&type=HTML |
| 2. 증권선물위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=sfc&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| sfc id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문 일련번호 |
| 안건명 | string | 안건명 |
| 의결번호 | string | 의결번호 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=sfc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `sfcInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=sfc&ID=7919&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=sfc&ID=7929&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=sfc&ID=7919&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (증권선물위원회 : sfc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |



[TABLE_0]
####  상세 내용


##### 증권선물위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (증권선물위원회 : sfc) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |


| 샘플 URL |
| --- |
| 1. 증권선물위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=sfc&ID=7919&type=HTML |
| 2. 증권선물위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=sfc&ID=7929&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 기관명 | string | 기관명 |
| 의결번호 | string | 의결번호 |
| 안건명 | string | 안건명 |
| 조치대상자의인적사항 | string | 조치대상자의 인적사항 |
| 조치대상 | string | 조치대상 |
| 조치내용 | string | 조치내용 |
| 조치이유 | string | 조치이유 |
| 각주번호 | int | 각주번호 |
| 각주내용 | string | 각주내용 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=sfc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(의결서, response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `nhrckListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=nhrck&type=HTML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=nhrck&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=nhrck&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (국가인권위원회 : nhrck) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 (default) ldes : 사건명 내림차순 nasc : 의결번호 오름차순 ndes : 의결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(사건명, 사건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 국가인권위원회 결정문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (국가인권위원회 : nhrck) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 1 : 사건명 (default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (IE 조회시 UTF-8 인코딩 필수) |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 (default) ldes : 사건명 내림차순 nasc : 의결번호 오름차순 ndes : 의결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(사건명, 사건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 국가인권위원회 결정문 HTML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=nhrck&type=HTML |
| 2. 국가인권위원회 결정문 XML 목록 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=nhrck&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색결과갯수 |
| page | int | 현재 페이지번호 |
| 기관명 | string | 위원회명 |
| nhrck id | int | 검색 결과 순번 |
| 결정문일련번호 | int | 결정문일련번호 |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 의결일자 | string | 의결일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 결정문상세링크 | string | 결정문 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=nhrck 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `nhrckInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=nhrck&ID=331&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=nhrck&ID=335&type=XML`
3. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=nhrck&ID=331&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (국가인권위원회 : nhrck) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |
| LM | char | 결정문명 |
| fields | string | 응답항목 옵션(사건명, 사건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 국가인권위원회 결정문 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (국가인권위원회 : nhrck) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 결정문 일련번호 |
| LM | char | 결정문명 |
| fields | string | 응답항목 옵션(사건명, 사건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 국가인권위원회 결정문 HTML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=nhrck&ID=331&type=HTML |
| 2. 국가인권위원회 결정문 XML 상세조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=nhrck&ID=335&type=XML |


| 필드 | 값 | 설명 | 결정문일련번호 | int | 결정문일련번호 |
| --- | --- | --- | --- | --- | --- |
| 기관명 | string | 기관명 |
| 위원회명 | string | 위원회명 |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 의결일자 | string | 의결일자 |
| 주문 | string | 주문 |
| 이유 | string | 이유 |
| 위원정보 | string | 위원정보 |
| 별지 | string | 별지 |
| 결정요지 | string | 결정요지 |
| 판단요지 | string | 판단요지 |
| 주문요지 | string | 주문요지 |
| 분류명 | string | 분류명 |
| 결정유형 | string | 결정유형 |
| 신청인 | string | 신청인 |
| 피신청인 | string | 피신청인 |
| 피해자 | string | 피해자 |
| 피조사자 | string | 피조사자 |
| 원본다운로드URL | string | 원본다운로드URL |
| 바로보기URL | string | 바로보기URL |
| 결정례전문 | string | 결정례전문 |
| 데이터기준일시 | string | 데이터기준일시 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=nhrck 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(의결서, response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `specialDeccTtListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ttSpecialDecc&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ttSpecialDecc&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ttSpecialDecc&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ttSpecialDecc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 특별행정심판재결례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| cls | string | 재결례유형(출력 결과 필드에 있는 재결구분코드) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| date | int | 의결일자 |
| dpaYd | string | 처분일자 검색(20090101~20090130) |
| rslYd | string | 의결일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 재결례명 오름차순) ldes 재결례명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 청구번호 오름차순 ndes : 청구번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(사건명, 청구번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 조세심판원 특별행정심판재결례 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ttSpecialDecc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 특별행정심판재결례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| cls | string | 재결례유형(출력 결과 필드에 있는 재결구분코드) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| date | int | 의결일자 |
| dpaYd | string | 처분일자 검색(20090101~20090130) |
| rslYd | string | 의결일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 재결례명 오름차순) ldes 재결례명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 청구번호 오름차순 ndes : 청구번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(사건명, 청구번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 특별행정심판재결례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ttSpecialDecc&type=XML |
| 2. 특별행정심판재결례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ttSpecialDecc&type=HTML |
| 3. 특별행정심판재결례 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ttSpecialDecc&type=JSON |
| 4. 특별행정심판재결례 목록 중 ‘ㄱ’으로 시작하는 재결례 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ttSpecialDecc&type=XML&gana=ga |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(EvtNm:재결례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| decc id | int | 검색결과번호 |
| 특별행정심판재결례일련번호 | int | 특별행정심판재결례일련번호 |
| 사건명 | string | 사건명 |
| 청구번호 | string | 청구번호 |
| 처분일자 | string | 처분일자 |
| 의결일자 | string | 의결일자 |
| 처분청 | string | 처분청 |
| 재결청 | int | 재결청 |
| 재결구분명 | string | 재결구분명 |
| 재결구분코드 | string | 재결구분코드 |
| 데이터기준일시 | string | 데이터기준일시 |
| 행정심판재결례상세링크 | string | 행정심판재결례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=ttSpecialDecc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `specialDeccTtInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ttSpecialDecc&ID=1018160&type=XML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ttSpecialDecc&ID=1018160&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ttSpecialDecc&ID=1018160&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ttSpecialDecc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 특별행정심판재결례일련번호 |
| LM | string | 특별행정심판재결례명 |
| fields | string | 응답항목 옵션(사건명, 사건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 조세심판원 특별행정심판재결례 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ttSpecialDecc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 특별행정심판재결례일련번호 |
| LM | string | 특별행정심판재결례명 |
| fields | string | 응답항목 옵션(사건명, 사건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 특별행정심판재결례일련번호가 1018160인 특별행정심판재결례 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=ttSpecialDecc&ID=1018160&type=XML |
| 2. 특별행정심판재결례일련번호가 1018160인 특별행정심판재결례 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=ttSpecialDecc&ID=1018160&type=HTML |
| 3. 특별행정심판재결례일련번호가 1018160인 특별행정심판재결례 JSON 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=ttSpecialDecc&ID=1018160&type=JSON |


| 필드 | 값 | 설명 | 특별행정심판재결례일련번호 | int | 특별행정심판재결례일련번호 |
| --- | --- | --- | --- | --- | --- |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 청구번호 | string | 청구번호 |
| 처분일자 | int | 처분일자 |
| 의결일자 | int | 의결일자 |
| 처분청 | string | 처분청 |
| 재결청 | string | 재결청 |
| 재결례유형명 | string | 재결례유형명 |
| 재결례유형코드 | int | 재결례유형코드 |
| 세목 | string | 세목 |
| 재결요지 | string | 재결요지 |
| 따른결정 | string | 따른결정 |
| 참조결정 | string | 참조결정 |
| 주문 | string | 주문 |
| 청구취지 | string | 청구취지 |
| 이유 | string | 이유 |
| 관련법령 | string | 관련법령 |
| 데이터기준일시 | string | 데이터기준일시 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=ttSpecialDecc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `specialDeccKmstListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=kmstSpecialDecc&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=kmstSpecialDecc&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=kmstSpecialDecc&type=XML&gana=ga`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : kmstSpecialDecc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 특별행정심판재결례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| cls | string | 재결례유형(출력 결과 필드에 있는 재결구분코드) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| date | int | 의결일자 |
| dpaYd | string | 처분일자 검색(20090101~20090130) |
| rslYd | string | 의결일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 재결례명 오름차순) ldes 재결례명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 재결번호 오름차순 ndes : 재결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(사건명, 재결번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 해양안전심판원 특별행정심판재결례 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : kmstSpecialDecc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 특별행정심판재결례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| cls | string | 재결례유형(출력 결과 필드에 있는 재결구분코드) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| date | int | 의결일자 |
| dpaYd | string | 처분일자 검색(20090101~20090130) |
| rslYd | string | 의결일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 재결례명 오름차순) ldes 재결례명 내림차순 dasc : 의결일자 오름차순 ddes : 의결일자 내림차순 nasc : 재결번호 오름차순 ndes : 재결번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(사건명, 재결번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 특별행정심판재결례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kmstSpecialDecc&type=XML |
| 2. 특별행정심판재결례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kmstSpecialDecc&type=HTML |
| 3. 특별행정심판재결례 목록 중 ‘ㄱ’으로 시작하는 재결례 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kmstSpecialDecc&type=XML&gana=ga |
| 4. 특별행정심판재결례 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kmstSpecialDecc&type=JSON |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(EvtNm:재결례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| decc id | int | 검색결과번호 |
| 특별행정심판재결례일련번호 | int | 특별행정심판재결례일련번호 |
| 사건명 | string | 사건명 |
| 재결번호 | string | 재결번호 |
| 처분일자 | string | 처분일자 |
| 의결일자 | string | 의결일자 |
| 처분청 | string | 처분청 |
| 재결청 | int | 재결청 |
| 재결구분명 | string | 재결구분명 |
| 재결구분코드 | string | 재결구분코드 |
| 데이터기준일시 | string | 데이터기준일시 |
| 행정심판재결례상세링크 | string | 행정심판재결례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=kmstSpecialDecc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `specialDeccKmstInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=kmstSpecialDecc&ID=2&type=XML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=kmstSpecialDecc&ID=2&LM=기선 제12금영호 침몰사건&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=kmstSpecialDecc&ID=2&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : kmstSpecialDecc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 특별행정심판재결례일련번호 |
| LM | string | 특별행정심판재결례명 |
| fields | string | 응답항목 옵션(사건명, 사건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 해양안전심판원 특별행정심판재결례 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : kmstSpecialDecc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char(필수) | 특별행정심판재결례일련번호 |
| LM | string | 특별행정심판재결례명 |
| fields | string | 응답항목 옵션(사건명, 사건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 특별행정심판재결례일련번호가 2인 특별행정심판재결례 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=kmstSpecialDecc&ID=2&type=XML |
| 2. '기선 제12금영호 침몰사건' 특별행정심판재결례 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=kmstSpecialDecc&ID=2&LM=기선 제12금영호 침몰사건&type=HTML |
| 3. 특별행정심판재결례일련번호가 2인 특별행정심판재결례 JSON 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=kmstSpecialDecc&ID=2&type=JSON |


| 필드 | 값 | 설명 | 특별행정심판재결례일련번호 | int | 특별행정심판재결례일련번호 |
| --- | --- | --- | --- | --- | --- |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 처분일자 | int | 처분일자 |
| 의결일자 | int | 의결일자 |
| 처분청 | string | 처분청 |
| 재결청 | string | 재결청 |
| 재결례유형명 | string | 재결례유형명 |
| 재결례유형코드 | int | 재결례유형코드 |
| 재결번호 | int | 재결번호 |
| 주문 | string | 주문 |
| 청구취지 | string | 청구취지 |
| 이유 | string | 이유 |
| 해양사고관련자 | string | 해양사고관련자 |
| 심판관 | string | 심판관 |
| 사고유형 | string | 사고유형 |
| 선박유형 | string | 선박유형 |
| 해심위치 | string | 해심위치 |
| 재심청구안내 | string | 재심청구안내 |
| 별지 | string | 별지 |
| 의결종류 | string | 의결종류 |
| 재결위원회 | string | 재결위원회 |
| 데이터기준일시 | string | 데이터기준일시 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=kmstSpecialDecc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

## 조약

### OPEN API 활용가이드

**API ID**: `trtyListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&ID=284&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&type=XML&cls=2`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : trty(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 조약명) 2 : 조약본문 |
| query | string | 검색범위에서 검색을 원하는 질의 (검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| eftYd | string | 발효일자 검색(20090101~20090130) |
| concYd | string | 체결일자 검색(20090101~20090130) |
| cls | int | 1 : 양자조약 2 : 다자조약 |
| natCd | int | 국가코드 |
| sort | string | 정렬옵션 (기본 : lasc 조약명오름차순) ldes 조약명내림차순 dasc : 발효일자 오름차순 ddes : 발효일자 내림차순 nasc : 조약번호 오름차순 ndes : 조약번호 내림차순 rasc : 관보게재일 오름차순 rdes : 관보게재일 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 조약 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : trty(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 조약명) 2 : 조약본문 |
| query | string | 검색범위에서 검색을 원하는 질의 (검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| eftYd | string | 발효일자 검색(20090101~20090130) |
| concYd | string | 체결일자 검색(20090101~20090130) |
| cls | int | 1 : 양자조약 2 : 다자조약 |
| natCd | int | 국가코드 |
| sort | string | 정렬옵션 (기본 : lasc 조약명오름차순) ldes 조약명내림차순 dasc : 발효일자 오름차순 ddes : 발효일자 내림차순 nasc : 조약번호 오름차순 ndes : 조약번호 내림차순 rasc : 관보게재일 오름차순 rdes : 관보게재일 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 조약 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&type=XML |
| 2. 조약 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&ID=284&type=HTML |
| 3. 다자조약 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&type=XML&cls=2 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(TrtyNm:조약명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| trty id | int | 검색결과번호 |
| 조약일련번호 | int | 조약일련번호 |
| 조약명 | string | 조약명 |
| 조약구분코드 | string | 조약구분코드 |
| 조약구분명 | string | 조약구분명 |
| 발효일자 | string | 발효일자 |
| 서명일자 | string | 서명일자 |
| 관보게제일자 | string | 관보게제일자 |
| 조약번호 | int | 조약번호 |
| 국가번호 | int | 국가번호 |
| 조약상세링크 | string | 조약상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=trty 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `trtyInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=trty&ID=983&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=trty&ID=2120&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=trty&ID=983&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : trty(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| ID | char | 조약 ID |
| chrClsCd | char | 한글/영문 : 010202(한글)/ 010203(영문) (default = 010202) |



[TABLE_0]
####  상세 내용


##### 조약 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : trty(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| ID | char | 조약 ID |
| chrClsCd | char | 한글/영문 : 010202(한글)/ 010203(영문) (default = 010202) |


| 샘플 URL |
| --- |
| 1. 조약 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=trty&ID=983&type=HTML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=trty&ID=2120&type=HTML |


| 필드 | 값 | 설명 | 조약일련번호 | int | 조약일련번호 |
| --- | --- | --- | --- | --- | --- |
| 조약명_한글 | string | 조약명한글 |
| 조약명_영문 | string | 조약명영문 |
| 조약구분코드 | int | 조약구분코드(양자조약:440101, 다자조약:440102) |
| 대통령재가일자 | int | 대통령재가일자 |
| 발효일자 | int | 발효일자 |
| 조약번호 | int | 조약번호 |
| 관보게재일자 | int | 관보게재일자 |
| 국무회의심의일자 | int | 국무회의심의일자 |
| 국무회의심의회차 | int | 국무회의심의회차 |
| 국회비준동의여부 | string | 국회비준동의여부 |
| 국회비준동의일자 | string | 국회비준동의일자 |
| 서명일자 | int | 서명일자 |
| 서명장소 | string | 서명장소 |
| 비고 | string | 비고 |
| 추가정보 | string | 추가정보 |
| 체결대상국가 | string | 체결대상국가 |
| 체결대상국가한글 | string | 체결대상국가한글 |
| 우리측국내절차완료통보 | int | 우리측국내절차완료통보일 |
| 상대국측국내절차완료통보 | int | 상대국측국내절차완료통보일 |
| 양자조약분야코드 | int | 양자조약분야코드 |
| 양자조약분야명 | string | 양자조약분야명 |
| 제2외국어종류 | string | 제2외국어종류 |
| 국가코드 | string | 국가코드 |
| 조약내용 | string | 조약내용 |
| 체결일자 | string | 체결일자 |
| 체결장소 | string | 체결장소 |
| 기탁처 | string | 기탁처 |
| 다자조약분야코드 | string | 다자조약분야코드 |
| 다자조약분야명 | string | 다자조약분야명 |
| 수락서기탁일자 | string | 수락서기탁일자 |
| 국내발효일자 | string | 국내발효일자 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=trty 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 별표서식

### OPEN API 활용가이드

**API ID**: `lsBylListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=XML&org=1320000`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : licbyl(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 별표서식명) 2 : 해당법령검색 3 : 별표본문검색 |
| query | string | 검색을 원하는 질의(default=*) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순), ldes(별표서식명 내림차순) |
| org | string | 소관부처별 검색(소관부처코드 제공) 소관부처 2개이상 검색 가능(","로 구분) |
| mulOrg | string | 소관부처 2개이상 검색 조건 OR : OR검색 (default) AND : AND검색 |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별지 4 : 별도 5 : 부록 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 별표서식 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : licbyl(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 별표서식명) 2 : 해당법령검색 3 : 별표본문검색 |
| query | string | 검색을 원하는 질의(default=*) (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순), ldes(별표서식명 내림차순) |
| org | string | 소관부처별 검색(소관부처코드 제공) 소관부처 2개이상 검색 가능(","로 구분) |
| mulOrg | string | 소관부처 2개이상 검색 조건 OR : OR검색 (default) AND : AND검색 |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별지 4 : 별도 5 : 부록 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 법령 별표서식 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=XML |
| 2. 법령 별표서식 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=HTML |
| 3. 경찰청 법령 별표서식 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=XML&org=1320000 |
| 4. 소관부처 2개이상(경찰청, 행정안전부) 입력한 별표서식 목록 HTML 검색(OR검색) |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=HTML&org=1320000,1741000 |
| 5. 소관부처 2개이상(경찰청, 행정안전부) 입력한 별표서식 목록 HTML 검색(AND검색) |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=HTML&org=1320000,1741000&mulOrg=AND |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| licbyl id | int | 결과번호 |
| 별표일련번호 | int | 별표일련번호 |
| 관련법령일련번호 | int | 관련법령일련번호 |
| 관련법령ID | int | 관련법령ID |
| 별표명 | string | 별표명ID |
| 관련법령명 | string | 관련법령명 |
| 별표번호 | int | 별표번호 |
| 별표종류 | string | 별표종류 |
| 소관부처명 | string | 소관부처명 |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 법령종류 | string | 법령종류 |
| 별표서식파일링크 | string | 별표서식파일링크 |
| 별표서식PDF파일링크 | string | 별표서식PDF파일링크 |
| 별표법령상세링크 | string | 별표법령상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=licbyl 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `mobLsBylListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=XML&org=1320000`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : licbyl(필수) | 서비스 대상 |
| type | char | 출력 형태 HTML/XML/JSON |
| search | int | "검색범위 (기본 : 1 별표서식명) 2 : 해당법령검색 3 : 별표본문검색" |
| query | string | 법령명에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | "정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순" |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별지 4 : 별도 5 : 부록 |
| gana | string | 사전식 검색(ga,na,da…,etc) |



[TABLE_0]
####  상세 내용





| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : licbyl(필수) | 서비스 대상 |
| type | char | 출력 형태 HTML/XML/JSON |
| search | int | "검색범위 (기본 : 1 별표서식명) 2 : 해당법령검색 3 : 별표본문검색" |
| query | string | 법령명에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | "정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순" |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별지 4 : 별도 5 : 부록 |
| gana | string | 사전식 검색(ga,na,da…,etc) |


| 샘플 URL |
| --- |
| 1. 법령 별표서식 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=XML |
| 2. 법령 별표서식 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=HTML |
| 3. 경찰청 법령 별표서식 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=licbyl&type=XML&org=1320000 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=licbyl 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobAdmrulBylListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=XML&org=1543000`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admbyl(필수) | 서비스 대상 |
| search | int | 검색범위 (기본 : 1 별표서식명) 2 : 해당법령검색 3 : 별표본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별지 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| type | char | 출력 형태 HTML/XML/JSON 생략시 기본값 : XML |



[TABLE_0]
####  상세 내용





| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admbyl(필수) | 서비스 대상 |
| search | int | 검색범위 (기본 : 1 별표서식명) 2 : 해당법령검색 3 : 별표본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별지 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| type | char | 출력 형태 HTML/XML/JSON 생략시 기본값 : XML |


| 샘플 URL |
| --- |
| 1. 행정규칙 별표서식 목록 XML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=XML |
| 2. 행정규칙 별표서식 목록 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=HTML |
| 3. 농림축산식품부 행정규칙 별표서식 목록 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admbyl&type=XML&org=1543000 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=admbyl 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobOrdinBylListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=HTML`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=XML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordinbyl(필수) | 서비스 대상 |
| search | int | 검색범위 (기본 : 1 별표서식명) 2 : 해당자치법규명검색 3 : 별표본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별도 4 : 별지 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| type | char | 출력 형태 HTML/XML/JSON 생략시 기본값 : XML |



[TABLE_0]
####  상세 내용





| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordinbyl(필수) | 서비스 대상 |
| search | int | 검색범위 (기본 : 1 별표서식명) 2 : 해당자치법규명검색 3 : 별표본문검색 |
| query | string | 법령명에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 별표서식명 오름차순) ldes 별표서식명 내림차순 |
| org | string | 소관부처별 검색(소관부처코드 제공) |
| knd | string | 별표종류 1 : 별표 2 : 서식 3 : 별도 4 : 별지 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| type | char | 출력 형태 HTML/XML/JSON 생략시 기본값 : XML |


| 샘플 URL |
| --- |
| 1. 자치법규 별표서식 목록 XML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=XML |
| 2. 자치법규 별표서식 목록 HTML 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordinbyl&type=HTML |



--> [HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=ordinbyl 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

## 학칙공단

### OPEN API 활용가이드

**API ID**: `schlPubRulListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=school&type=HTML&query=%ED%95%99%EA%B5%90`
2. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=school&query=학교&type=HTML`
3. `http://www.law.go.kr/DRF/lawSearch.do?target=school(or`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (대학 : school / 지방공사공단 : public / 공공기관 : pi) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 1 : 규정명(default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| knd | string | 학칙공단 종류별 검색 1 : 학칙 / 2 : 학교규정 / 3 : 학교지침 / 4 : 학교시행세칙  / 5 : 공단규정, 공공기관규정 |
| rrClsCd | string | 제정·개정 구분 200401 : 제정 / 200402 : 전부개정 / 200403 : 일부개정 / 200404 : 폐지 200405 : 일괄개정 / 200406 : 일괄폐지 / 200407 : 폐지제정 200408 : 정정 / 200409 : 타법개정 / 200410 : 타법폐지 |
| date | int | 발령일자 검색 |
| prmlYd | string | 발령일자 범위 검색 |
| nb | int | 발령번호 검색 |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 학칙공단명 오름차순(default) ldes : 학칙공단명 내림차순 dasc : 발령일자 오름차순 ddes : 발령일자 내림차순 nasc : 발령번호 오름차순 ndes : 발령번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 학칙공단공공기관 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (대학 : school / 지방공사공단 : public / 공공기관 : pi) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 1 : 규정명(default) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="자동차") |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| knd | string | 학칙공단 종류별 검색 1 : 학칙 / 2 : 학교규정 / 3 : 학교지침 / 4 : 학교시행세칙  / 5 : 공단규정, 공공기관규정 |
| rrClsCd | string | 제정·개정 구분 200401 : 제정 / 200402 : 전부개정 / 200403 : 일부개정 / 200404 : 폐지 200405 : 일괄개정 / 200406 : 일괄폐지 / 200407 : 폐지제정 200408 : 정정 / 200409 : 타법개정 / 200410 : 타법폐지 |
| date | int | 발령일자 검색 |
| prmlYd | string | 발령일자 범위 검색 |
| nb | int | 발령번호 검색 |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 학칙공단명 오름차순(default) ldes : 학칙공단명 내림차순 dasc : 발령일자 오름차순 ddes : 발령일자 내림차순 nasc : 발령번호 오름차순 ndes : 발령번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 학칙공단 HTML 목록 조회 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=school&query=학교&type=HTML |
|  |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| section | string | 검색범위 |
| totalCnt | int | 검색 건수 |
| page | int | 현재 페이지번호 |
| numOfRows | int | 페이지 당 출력 결과 수 |
| resultCode | int | 조회 여부(성공 : 00 / 실패 : 01) |
| resultMsg | int | 조회 여부(성공 : success / 실패 : fail) |
| admrul id | int | 검색 결과 순번 |
| 행정규칙일련번호 | int | 학칙공단 일련번호 |
| 행정규칙명 | string | 학칙공단명 |
| 행정규칙종류 | string | 학칙공단 종류 |
| 발령일자 | int | 발령일자 |
| 발령번호 | int | 발령번호 |
| 소관부처명 | string | 소관부처명 |
| 현행연혁구분 | string | 현행연혁구분 |
| 제개정구분코드 | string | 제개정구분코드 |
| 제개정구분명 | string | 제개정구분명 |
| 법령분류코드 | string | 법령분류코드 |
| 법령분류명 | string | 법령분류명 |
| 행정규칙ID | int | 학칙공단ID |
| 행정규칙상세링크 | string | 학칙공단 상세링크 |
| 시행일자 | int | 시행일자 |
| 생성일자 | int | 생성일자 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=school(or public or pi) 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `schlPubRulInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=school&LID=2055825&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=school&ID=2200000075994&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=school&LID=2055825&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (대학 : school / 지방공사공단 : public / 공공기관 : pi) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 학칙공단 일련번호 |
| LID | char | 학칙공단 ID |
| LM | string | 학칙공단명조회하고자 하는 정확한 학칙공단명을 입력 |



[TABLE_0]
####  상세 내용


##### 학칙공단공공기관 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (대학 : school / 지방공사공단 : public / 공공기관 : pi) |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | char | 학칙공단 일련번호 |
| LID | char | 학칙공단 ID |
| LM | string | 학칙공단명조회하고자 하는 정확한 학칙공단명을 입력 |


| 샘플 URL |
| --- |
| 1. 학칙공단 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=school&LID=2055825&type=HTML |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=school&ID=2200000075994&type=HTML |


| 필드 | 값 | 설명 | 행정규칙일련번호 | int | 학칙공단 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 행정규칙명 | string | 학칙공단명 |
| 행정규칙종류 | string | 학칙공단 종류 |
| 행정규칙종류코드 | string | 학칙공단 종류코드 |
| 발령일자 | int | 발령일자 |
| 발령번호 | string | 발령번호 |
| 제개정구분명 | string | 제개정구분명 |
| 제개정구분코드 | string | 제개정구분코드 |
| 조문형식여부 | string | 조문형식여부 |
| 행정규칙ID | int | 학칙공단ID |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | string | 소관부처코드 |
| 담당부서기관코드 | string | 담당부서기관코드 |
| 담당부서기관명 | string | 담당부서기관명 |
| 담당자명 | string | 담당자명 |
| 전화번호 | string | 전화번호 |
| 현행여부 | string | 현행여부 |
| 생성일자 | string | 생성일자 |
| 조문내용 | string | 조문내용 |
| 부칙공포일자 | string | 부칙 공포일자 |
| 부칙공포번호 | string | 부칙 공포번호 |
| 부칙내용 | string | 부칙내용 |
| 별표단위 별표키 | string | 별표단위 별표키 |
| 별표번호 | string | 별표번호 |
| 별표가지번호 | string | 별표가지번호 |
| 별표구분 | string | 별표구분 |
| 별표제목 | string | 별표제목 |
| 별표서식파일링크 | string | 별표서식 파일링크 |
| 개정문내용 | string | 개정문내용 |
| 제개정이유내용 | string | 제개정이유내용 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=school(or public or pi) 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 법령용어

### OPEN API 활용가이드

**API ID**: `lsTrmListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&gana=ra&type=XML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&query=%EC%9E%90%EB%8F%99%EC%B0%A8&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lstrm(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 법령용어명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령용어명 오름차순) ldes : 법령용어명 내림차순 rasc : 등록일자 오름차순 rdes : 등록일자 내림차순 |
| regDt | string | 등록일자 범위 검색(20090101~20090130) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| dicKndCd | int | 법령 종류 코드 (법령 : 010101, 행정규칙 : 010102) |



[TABLE_0]
####  상세 내용


##### 법령용어 목록 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lstrm(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 법령용어명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령용어명 오름차순) ldes : 법령용어명 내림차순 rasc : 등록일자 오름차순 rdes : 등록일자 내림차순 |
| regDt | string | 등록일자 범위 검색(20090101~20090130) |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| dicKndCd | int | 법령 종류 코드 (법령 : 010101, 행정규칙 : 010102) |


| 샘플 URL |
| --- |
| 1. 법령용어 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&type=XML |
| 2. 'ㄹ'로 시작하는 법령용어 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&gana=ra&type=XML |
| 3. 법령용어 검색 : 자동차 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&query=자동차&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| lstrm id | int | 결과 번호 |
| 법령용어ID | string | 법령용어ID |
| 법령용어명 | string | 법령용어명 |
| 법령용어상세검색 | string | 법령용어상세검색 |
| 사전구분코드 | string | 사전구분코드 (법령용어사전 : 011401, 법령정의사전 : 011402, 법령한영사전 : 011403) |
| 법령용어상세링크 | string | 법령용어상세링크 |
| 법령종류코드 | int | 법령 종류 코드(법령 : 010101, 행정규칙 : 010102) |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lstrm 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsTrmInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lstrm&query=%EC%84%A0%EB%B0%95&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lstrm&query=%EC%84%A0%EB%B0%95&type=XML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=lstrm&query=선박&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lstrm(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 상세조회하고자 하는 법령용어 명 |



[TABLE_0]
####  상세 내용


##### 법령용어 본문 조회 가이드API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lstrm(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| query | string | 상세조회하고자 하는 법령용어 명 |


| 샘플 URL |
| --- |
| 1. 법령용어 선박 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lstrm&query=선박&type=HTML |
| 2. 법령용어 선박 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=lstrm&query=선박&type=XML |


| 필드 | 값 | 설명 | 법령용어 일련번호 | int | 법령용어 일련번호 |
| --- | --- | --- | --- | --- | --- |
| 법령용어명_한글 | string | 법령용어명 한글 |
| 법령용어명_한자 | string | 법령용어명한자 |
| 법령용어코드 | int | 법령용어코드 |
| 법령용어코드명 | string | 법령용어코드명 |
| 출처 | string | 출처 |
| 법령용어정의 | string | 법령용어정의 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=lstrm 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 맞춤형

### OPEN API 활용가이드

**API ID**: `custLsListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=XML&vcode=L0000000003384`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=HTML&vcode=L0000000003384`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=XML&vcode=L0000000003384`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseLs(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string(필수) | 분류코드 법령은 L로 시작하는 14자리 코드(L0000000000001) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 맞춤형 법령 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseLs(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string(필수) | 분류코드 법령은 L로 시작하는 14자리 코드(L0000000000001) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 현행법령 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML |
| 2. 현행법령 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=HTML |
| 3. 법령 검색 : 자동차관리법 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&query=자동차관리법 |
| 4. 법령 공포일자 내림차순 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&sort=ddes |
| 5. 소관부처가 경찰청인 법령 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&org=1320000 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 법령일련번호 | int | 법령일련번호 |
| 현행연혁코드 | string | 현행연혁코드 |
| 법령명한글 | string | 법령명한글 |
| 법령약칭명 | string | 법령약칭명 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | string | 소관부처코드 |
| 법령구분명 | string | 법령구분명 |
| 공동부령구분 | string | 공동부령구분 |
| 공포번호 | string | 공포번호(공동부령의 공포번호) |
| 시행일자 | int | 시행일자 |
| 자법타법여부 | string | 자법타법여부 |
| 법령상세링크 | string | 법령상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=law 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `mobLsInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=law&ID=1747&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=91689&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&ID=1747&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : law(필수) | 서비스 대상 |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| JO | int:6 | 조번호 생략(기본값) : 모든 조를 표시함 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |
| PD | char | 부칙표시 ON일 경우 부칙 목록만 출력 생략할 경우 법령 + 부칙 표시 |
| PN | int | 부칙번호 해당 부칙번호에 해당하는 부칙 보기 |
| BD | char | 별표표시 생략(기본값) : 법령+별표 ON : 모든 별표 표시 |
| BT | int | 별표구분 별표표시가 on일 경우 값을 읽어들임 (별표=1/서식=2/별지=3/별도=4/부록=5) |
| BN | int | 별표번호 별표표시가 on일 경우 값을 읽어들임 |
| BG | int | 별표가지번호 별표표시가 on일 경우 값을 읽어들임 |
| type | char | 출력 형태 : HTML |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : law(필수) | 서비스 대상 |
| ID | char | 법령 ID (ID 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령 마스터 번호 법령테이블의 lsi_seq 값을 의미함 |
| LM | string | 법령의 법령명(법령명 입력시 해당 법령 링크) |
| LD | int | 법령의 공포일자 |
| LN | int | 법령의 공포번호 |
| JO | int:6 | 조번호 생략(기본값) : 모든 조를 표시함 6자리숫자 : 조번호(4자리)+조가지번호(2자리) (000200 : 2조, 001002 : 10조의 2) |
| PD | char | 부칙표시 ON일 경우 부칙 목록만 출력 생략할 경우 법령 + 부칙 표시 |
| PN | int | 부칙번호 해당 부칙번호에 해당하는 부칙 보기 |
| BD | char | 별표표시 생략(기본값) : 법령+별표 ON : 모든 별표 표시 |
| BT | int | 별표구분 별표표시가 on일 경우 값을 읽어들임 (별표=1/서식=2/별지=3/별도=4/부록=5) |
| BN | int | 별표번호 별표표시가 on일 경우 값을 읽어들임 |
| BG | int | 별표가지번호 별표표시가 on일 경우 값을 읽어들임 |
| type | char | 출력 형태 : HTML |


| 샘플 URL |
| --- |
| 1. 자동차관리법 ID HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&ID=1747&type=HTML |
| 2. 자동차관리법 법령 seq HTML조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&MST=91689&type=HTML |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=law 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobAdmrulListguide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=XML&query=%EC%86%8C%EB%B0%A9`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrul(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 (기본 : 1 행정규칙명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 소관부처별 검색 (코드 별도 제공) |
| knd | string | 행정규칙 종류별 검색 (1=훈령/2=예규/3=고시/4=공고/5=지침/6=기타) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 (기본 : lasc 행정규칙명 오른차순) ldes 행정규칙명 내림차순 dasc : 발령일자 오름차순 ddes : 발령일자 내림차순 nasc : 발령번호 오름차순 ndes : 발령번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 행정규칙 발령일자 |
| prmlYd | string | 발령일자 기간검색(20090101~20090130) |
| nb | int | 행정규칙 발령번호 |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrul(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 (기본 : 1 행정규칙명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 소관부처별 검색 (코드 별도 제공) |
| knd | string | 행정규칙 종류별 검색 (1=훈령/2=예규/3=고시/4=공고/5=지침/6=기타) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 (기본 : lasc 행정규칙명 오른차순) ldes 행정규칙명 내림차순 dasc : 발령일자 오름차순 ddes : 발령일자 내림차순 nasc : 발령번호 오름차순 ndes : 발령번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 행정규칙 발령일자 |
| prmlYd | string | 발령일자 기간검색(20090101~20090130) |
| nb | int | 행정규칙 발령번호 |


| 샘플 URL |
| --- |
| 1. 행정규칙 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=XML |
| 2. 행정규칙 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=HTML |
| 3. 행정규칙명에 '소방'이 포함된 행정규칙 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=XML&query=소방 |
| 4. 발령일자가 2015년 3월 1일인 행정규칙 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=XML&date=20150301 |
| 5. 발령번호가 331인 행정규칙 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=admrul&type=XML&nb=331 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색키워드 |
| section | string | 검색범위(AdmRulNm:행정규칙명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| admrul id | int | 검색결과번호 |
| 행정규칙일련번호 | int | 행정규칙일련번호 |
| 행정규칙명 | string | 행정규칙명 |
| 행정규칙종류 | string | 행정규칙종류 |
| 발령일자 | string | 발령일자 |
| 발령번호 | string | 발령번호 |
| 소관부처명 | string | 소관부처명 |
| 현행연혁구분 | string | 현행연혁구분 |
| 제개정구분코드 | string | 제개정구분코드 |
| 제개정구분명 | string | 제개정구분명 |
| 행정규칙ID | string | 행정규칙ID |
| 행정규칙상세링크 | string | 행정규칙상세링크 |
| 시행일자 | string | 시행일자 |
| 생성일자 | string | 생성일자 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=admrul 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `mobAdmrulInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=62505&type=HTML`
2. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=62505&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?target=admrul`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrul(필수) | 서비스 대상 |
| ID | char | 행정규칙 일련번호 |
| LM | Char | 행정규칙명 조회하고자 하는 정확한 행정규칙명을 입력 |
| type | Char | 출력 형태 : HTML |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : admrul(필수) | 서비스 대상 |
| ID | char | 행정규칙 일련번호 |
| LM | Char | 행정규칙명 조회하고자 하는 정확한 행정규칙명을 입력 |
| type | Char | 출력 형태 : HTML |


| 샘플 URL |
| --- |
| 1. 행정규칙 HTML 상세조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=admrul&ID=62505&type=HTML |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=admrul 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobOrdinListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&type=XML `
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&type=HTML `
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&query=서울&type=HTML `

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordin(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 (기본 : 1 자치법규명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 자치법규오름차순) ldes 자치법규 내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 자치법규 공포일자 검색 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 지자체별 도·특별시·광역시 검색(지자체코드 제공) (ex. 서울특별시에 대한 검색-> org=6110000) |
| sborg | string | 지자체별 시·군·구 검색(지자체코드 제공) (필수값 : org, ex.서울특별시 구로구에 대한 검색-> org=6110000&sborg=3160000) |
| knd | string | 법령종류 (30001-조례 /30002-규칙 /30003-훈령  /30004-예규/30006-기타/30010-고시 /30011-의회규칙) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300208-타법개정 / 300209-타법폐지 300214-기타) |
| ordinFd | int | 분류코드별 검색. 분류코드는 지자체 분야코드 openAPI 참조 |
| lsChapNo | string | 법령분야별 검색(법령분야코드제공) (ex. 제1편 검색 lsChapNo=01000000 / 제1편2장,제1편2장1절 lsChapNo=01020000,01020100) |
| gana | string(org 값 필수) | 사전식 검색 (ga,na,da…,etc) |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordin(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 HTML/XML/JSON |
| nw | int | (1: 현행, 2: 연혁, 기본값: 현행) |
| search | int | 검색범위 (기본 : 1 자치법규명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(default=*) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션 (기본 : lasc 자치법규오름차순) ldes 자치법규 내림차순 dasc : 공포일자 오름차순 ddes : 공포일자 내림차순 nasc : 공포번호 오름차순 ndes : 공포번호 내림차순 efasc : 시행일자 오름차순 efdes : 시행일자 내림차순 |
| date | int | 자치법규 공포일자 검색 |
| efYd | string | 시행일자 범위 검색(20090101~20090130) |
| ancYd | string | 공포일자 범위 검색(20090101~20090130) |
| ancNo | string | 공포번호 범위 검색(306~400) |
| nb | int | 법령의 공포번호 검색 |
| org | string | 지자체별 도·특별시·광역시 검색(지자체코드 제공) (ex. 서울특별시에 대한 검색-> org=6110000) |
| sborg | string | 지자체별 시·군·구 검색(지자체코드 제공) (필수값 : org, ex.서울특별시 구로구에 대한 검색-> org=6110000&sborg=3160000) |
| knd | string | 법령종류 (30001-조례 /30002-규칙 /30003-훈령  /30004-예규/30006-기타/30010-고시 /30011-의회규칙) |
| rrClsCd | string | 법령 제개정 종류 (300201-제정 / 300202-일부개정 / 300203-전부개정 300204-폐지 / 300205-폐지제정 / 300206-일괄개정 300207-일괄폐지 / 300208-타법개정 / 300209-타법폐지 300214-기타) |
| ordinFd | int | 분류코드별 검색. 분류코드는 지자체 분야코드 openAPI 참조 |
| lsChapNo | string | 법령분야별 검색(법령분야코드제공) (ex. 제1편 검색 lsChapNo=01000000 / 제1편2장,제1편2장1절 lsChapNo=01020000,01020100) |
| gana | string(org 값 필수) | 사전식 검색 (ga,na,da…,etc) |


| 샘플 URL |
| --- |
| 1. 자치법규 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&type=XML |
| 2. 자치법규 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&type=HTML |
| 3. 자치법규명에 서울이 포함된 자치법규 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ordin&query=서울&type=HTML |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(ordinNm:자치법규명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| law id | int | 검색결과번호 |
| 자치법규일련번호 | int | 자치법규일련번호 |
| 자치법규명 | string | 자치법규명 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | string | 공포일자 |
| 공포번호 | string | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 지자체기관명 | string | 지자체기관명 |
| 자치법규종류 | string | 자치법규종류 |
| 시행일자 | string | 시행일자 |
| 자치법규상세링크 | string | 자치법규상세링크 |
| 자치법규분야명 | string | 자치법규분야명 |
| 참조데이터구분 | string | 참조데이터구분 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=ordin 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `mobOrdinInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&ID=2047729&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&type=HTML&MST=1062134`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&ID=2047729&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordin(필수) | 서비스 대상 |
| ID | char | 자치법규 ID |
| MST | string | 자치법규 마스터 번호 |
| type | char | 출력 형태 : HTML |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ordin(필수) | 서비스 대상 |
| ID | char | 자치법규 ID |
| MST | string | 자치법규 마스터 번호 |
| type | char | 출력 형태 : HTML |


| 샘플 URL |
| --- |
| 1. 자치법규 ID HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&ID=2047729&type=HTML |
| 2. 자치법규 MST HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=ordin&type=HTML&MST=1062134 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=ordin 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobPrecListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=XML&query=%EC%9E%90%EB%8F%99%EC%B0%A8`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : prec(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 판례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 법원종류 (대법원:400201, 하위법원:400202) |
| curt | string | 법원명 (대법원, 서울고등법원, 광주지법, 인천지방법원) |
| JO | string | 참조법령명(형법, 민법 등) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 ldes : 사건명 내림차순 dasc : 선고일자 오름차순 ddes : 선고일자 내림차순(생략시 기본) nasc : 법원명 오름차순 ndes : 법원명 내림차순 |
| date | int | 판례 선고일자 |
| prncYd | string | 선고일자 검색(20090101~20090130) |
| nb | int | 판례 사건번호 |
| datSrcNm | string | 데이터출처명(국세법령정보시스템, 근로복지공단산재판례, 대법원) |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : prec(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 판례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| org | string | 법원종류 (대법원:400201, 하위법원:400202) |
| curt | string | 법원명 (대법원, 서울고등법원, 광주지법, 인천지방법원) |
| JO | string | 참조법령명(형법, 민법 등) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 lasc : 사건명 오름차순 ldes : 사건명 내림차순 dasc : 선고일자 오름차순 ddes : 선고일자 내림차순(생략시 기본) nasc : 법원명 오름차순 ndes : 법원명 내림차순 |
| date | int | 판례 선고일자 |
| prncYd | string | 선고일자 검색(20090101~20090130) |
| nb | int | 판례 사건번호 |
| datSrcNm | string | 데이터출처명(국세법령정보시스템, 근로복지공단산재판례, 대법원) |


| 샘플 URL |
| --- |
| 1. 판례 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=XML |
| 2. 판례 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=HTML |
| 3. 자동차가 포함된 판례 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=XML&query=자동차 |
| 4. 자동차가 포함된 판례 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&query=자동차&type=HTML |
| 5. 선고일자가 2015년 1월 29일인 판례검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=prec&type=XML&date=20150129 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위(EvtNm:판례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| prec id | int | 검색결과번호 |
| 판례일련번호 | int | 판례일련번호 |
| 사건명 | string | 사건명 |
| 사건번호 | string | 사건번호 |
| 선고일자 | string | 선고일자 |
| 법원명 | string | 법원명 |
| 법원종류코드 | int | 법원종류코드(대법원:400201, 하위법원:400202) |
| 사건종류명 | string | 사건종류명 |
| 사건종류코드 | int | 사건종류코드 |
| 판결유형 | string | 판결유형 |
| 선고 | string | 선고 |
| 데이터출처명 | string | 데이터출처명 |
| 판례상세링크 | string | 판례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=prec 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `mobPrecInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=prec&ID=228547&type=HTML`
2. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=prec&ID=228547&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?target=prec`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : prec(필수) | 서비스 대상 |
| ID | char(필수) | 판례 일련번호 |
| LM | string | 판례명 |
| type | string | 출력 형태 : HTML |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : prec(필수) | 서비스 대상 |
| ID | char(필수) | 판례 일련번호 |
| LM | string | 판례명 |
| type | string | 출력 형태 : HTML |


| 샘플 URL |
| --- |
| 1. 판례일련번호가 96538인 판례 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=prec&ID=228547&type=HTML |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=prec 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobDetcListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML&query=%EC%9E%90%EB%8F%99%EC%B0%A8`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : detc(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 헌재결정례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 (기본 : lasc 사건명 오름차순) ldes 사건명 내림차순 dasc : 선고일자 오름차순 ddes : 선고일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 efasc : 종국일자 오름차순 efdes : 종국일자 내림차순 |
| date | int | 종국일자 |
| nb | int | 사건번호 |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : detc(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 헌재결정례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| sort | string | 정렬옵션 (기본 : lasc 사건명 오름차순) ldes 사건명 내림차순 dasc : 선고일자 오름차순 ddes : 선고일자 내림차순 nasc : 사건번호 오름차순 ndes : 사건번호 내림차순 efasc : 종국일자 오름차순 efdes : 종국일자 내림차순 |
| date | int | 종국일자 |
| nb | int | 사건번호 |


| 샘플 URL |
| --- |
| 1. 헌재결정례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML |
| 2. 헌재결정례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=HTML |
| 3. 자동차가 포함된 헌재결정례 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML&query=자동차 |
| 4. 선고일자가 2015년 2월 10일인 헌재결정례검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=detc&type=XML&date=20150210 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(EvtNm:헌재결정례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| detc id | int | 검색결과번호 |
| 헌재결정례일련번호 | int | 헌재결정례일련번호 |
| 종국일자 | string | 종국일자 |
| 사건번호 | string | 사건번호 |
| 사건명 | string | 사건명 |
| 헌재결정례상세링크 | string | 헌재결정례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=detc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `mobDetcInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=58386&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=127830&LM=자동차관리법제26조등위헌확인등&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=58386&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : detc(필수) | 서비스 대상 |
| ID | char(필수) | 헌재결정례 일련번호 |
| LM | string | 헌재결정례명 |
| type | string | 출력 형태 : HTML |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : detc(필수) | 서비스 대상 |
| ID | char(필수) | 헌재결정례 일련번호 |
| LM | string | 헌재결정례명 |
| type | string | 출력 형태 : HTML |


| 샘플 URL |
| --- |
| 1. 헌재결정례 일련번호가 58386인 헌재결정례 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=58386&type=HTML |
| 2. 산림기술자 자격취소처분 취소청구 등 헌재결정례 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=detc&ID=127830&&LM=자동차관리법제26조등위헌확인등&type=HTML |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=detc 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobExpcListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=xml&query=%ED%97%88%EA%B0%80`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : expc(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | inq | 질의기관 |
| rpl | int | 회신기관 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 |
| regYd | string | 등록일자 검색(20090101~20090130) |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석례명 오름차순) ldes 법령해석례명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : expc(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석례명) 2 : 본문검색 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | inq | 질의기관 |
| rpl | int | 회신기관 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 |
| regYd | string | 등록일자 검색(20090101~20090130) |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석례명 오름차순) ldes 법령해석례명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |


| 샘플 URL |
| --- |
| 1. 법령해석례 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=XML |
| 2. 법령해석례 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&&type=HTML |
| 3. 법령해석례명에 '허가'가 포함된 법령해석례 찾기 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=expc&type=XML&query=허가 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석례명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| expc id | int | 검색결과번호 |
| 법령해석례일련번호 | int | 법령해석례일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 회신기관코드 | string | 회신기관코드 |
| 회신기관명 | string | 회신기관명 |
| 회신일자 | string | 회신일자 |
| 법령해석례상세링크 | string | 법령해석례상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=expc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `mobExpcInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=334617&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=315191&LM=%EC%97%AC%EC%84%B1%EA%B0%80%EC%A1%B1%EB%B6%80%20-%20%EA%B1%B4%EA%B0%95%EA%B0%80%EC%A0%95%EA%B8%B0%EB%B3%B8%EB%B2%95%20%EC%A0%9C35%EC%A1%B0%20%EC%A0%9C2%ED%95%AD%20%EA%B4%80%EB%A0%A8&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=334617&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : expc(필수) | 서비스 대상 |
| ID | int | 법령해석례 일련번호 |
| LM | string | 법령해석례명 |
| type | string | 출력 형태 : HTML |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : expc(필수) | 서비스 대상 |
| ID | int | 법령해석례 일련번호 |
| LM | string | 법령해석례명 |
| type | string | 출력 형태 : HTML |


| 샘플 URL |
| --- |
| 1. 법령해석례일련번호가 281909인 해석례 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=334617&type=HTML |
| 2. 여성가족부 - 건강가정기본법 제35조 제2항 관련 법령해석례 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=expc&ID=315191&LM=여성가족부 - 건강가정기본법 제35조 제2항 관련&type=HTML |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=expc 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobTrtyListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&ID=284&type=HTML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&type=XML&cls=2`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : trty(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 조약명 ) 2 : 조약본문 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| eftYd | string | 발효일자 검색(20090101~20090130) |
| concYd | string | 체결일자 검색(20090101~20090130) |
| cls | int | 1 : 양자조약 2 : 다자조약 |
| sort | string | 정렬옵션 (기본 : lasc 조약명오름차순) ldes 조약명내림차순 dasc : 발효일자 오름차순 ddes : 발효일자 내림차순 nasc : 조약번호 오름차순 ndes : 조약번호 내림차순 rasc : 관보게재일 오름차순 rdes : 관보게재일 내림차순 |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : trty(필수) | 서비스 대상 |
| type | char | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 조약명 ) 2 : 조약본문 |
| query | string | 검색범위에서 검색을 원하는 질의(검색 결과 리스트) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| eftYd | string | 발효일자 검색(20090101~20090130) |
| concYd | string | 체결일자 검색(20090101~20090130) |
| cls | int | 1 : 양자조약 2 : 다자조약 |
| sort | string | 정렬옵션 (기본 : lasc 조약명오름차순) ldes 조약명내림차순 dasc : 발효일자 오름차순 ddes : 발효일자 내림차순 nasc : 조약번호 오름차순 ndes : 조약번호 내림차순 rasc : 관보게재일 오름차순 rdes : 관보게재일 내림차순 |


| 샘플 URL |
| --- |
| 1. 조약 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&type=XML |
| 2. 조약 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&ID=284&type=HTML |
| 3. 다자조약 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=trty&type=XML&cls=2 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(TrtyNm:조약명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| trty id | int | 검색결과번호 |
| 조약일련번호 | int | 조약일련번호 |
| 조약명 | string | 조약명 |
| 조약구분코드 | string | 조약구분코드 |
| 조약구분명 | string | 조약구분명 |
| 발효일자 | string | 발효일자 |
| 서명일자 | string | 서명일자 |
| 관보게재일자 | string | 관보게재일자 |
| 조약번호 | int | 조약번호 |
| 조약상세링크 | string | 조약상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=trty 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `mobTrtyInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=trty&ID=983&type=HTML`
2. `http://www.law.go.kr/DRF/lawService.do?OC=test&target=trty&ID=983&type=HTML`
3. `http://www.law.go.kr/DRF/lawService.do?target=trty`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : trty(필수) | 서비스 대상 |
| ID | char | 조약 ID |
| type | char | 출력 형태 : HTML |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : trty(필수) | 서비스 대상 |
| ID | char | 조약 ID |
| type | char | 출력 형태 : HTML |


| 샘플 URL |
| --- |
| 1. 조약 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=trty&ID=983&type=HTML |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=trty 요청 변수 (request parameter) [TABLE_0] [TABLE_1]

---

### OPEN API 활용가이드

**API ID**: `mobLsTrmListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&type=XML`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&gana=ga&type=XML`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&query=%EC%9E%90%EB%8F%99%EC%B0%A8&type=HTML`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lstrm(필수) | 서비스 대상 |
| query | string | 법령용어명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령용어명 오름차순) ldes : 법령용어명 내림차순 |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| type | char | 출력 형태 : HTML/XML/JSON생략시 기본값 : XML |
| dicKndCd | int | 법령 종류 코드 (법령 : 010101, 행정규칙 : 010102) |



[TABLE_0]
####  상세 내용




| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : lstrm(필수) | 서비스 대상 |
| query | string | 법령용어명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| sort | string | 정렬옵션(기본 : lasc 법령용어명 오름차순) ldes : 법령용어명 내림차순 |
| gana | string | 사전식 검색 (ga,na,da…,etc) |
| type | char | 출력 형태 : HTML/XML/JSON생략시 기본값 : XML |
| dicKndCd | int | 법령 종류 코드 (법령 : 010101, 행정규칙 : 010102) |


| 샘플 URL |
| --- |
| 1. 법령용어 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&type=XML |
| 2. 'ㄱ'로 시작하는 법령용어 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&gana=ga&type=XML |
| 3. 법령용어 검색 : 자동차 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&query=자동차&type=HTML |
| 4. 법령용어 검색 : 자동차 XML |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrm&query=자동차&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색어 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| lstrm id | int | 결과 번호 |
| 법령용어ID | string | 법령용어ID |
| 법령용어명 | string | 법령용어명 |
| 법령용어상세검색 | string | 법령용어상세검색 |
| 사전구분코드 | string | 사전구분코드(법령용어사전 : 011401, 법령정의사전 : 011402, 법령한영사전 : 011403) |
| 법령용어상세링크 | string | 법령용어상세링크 |
| 법령종류코드 | int | 법령 종류 코드(법령 : 010101, 행정규칙 : 010102) |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=lstrm 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 맞춤형

### OPEN API 활용가이드

**API ID**: `custLsListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=XML&vcode=L0000000003384`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=HTML&vcode=L0000000003384`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=XML&vcode=L0000000003384`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseLs(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string(필수) | 분류코드 법령은 L로 시작하는 14자리 코드(L0000000000001) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 맞춤형 법령 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseLs(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string(필수) | 분류코드 법령은 L로 시작하는 14자리 코드(L0000000000001) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 분류코드가 L0000000003384인 맞춤형 분류 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=XML&vcode=L0000000003384 |
| 2. 분류코드가 L0000000003384인 맞춤형 분류 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=HTML&vcode=L0000000003384 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| vcode | string | 분류코드 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| law id | int | 결과 번호 |
| 법령일련번호 | int | 법령일련번호 |
| 법령명한글 | string | 법령명한글 |
| 법령ID | int | 법령ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 소관부처명 | string | 소관부처명 |
| 소관부처코드 | string | 소관부처코드 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 법령상세링크 | string | 법령상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=couseLs 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `custLsJoListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=XML&lj=jo&vcode=L0000000003384`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=HTML&lj=jo&vcode=L0000000003384`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=XML&lj=jo&vcode=L0000000003384`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseLs(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string | 분류코드(필수) 법령은 L로 시작하는 14자리 코드(L0000000000001) |
| lj=jo | string(필수) | 조문여부 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 맞춤형 법령 조문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseLs(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string | 분류코드(필수) 법령은 L로 시작하는 14자리 코드(L0000000000001) |
| lj=jo | string(필수) | 조문여부 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 분류코드가 L0000000003384인 맞춤형 법령 분류 조문 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=XML&lj=jo&vcode=L0000000003384 |
| 2. 분류코드가 L0000000003384인 맞춤형 법령 분류 조문 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseLs&type=HTML&lj=jo&vcode=L0000000003384 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| vcode | string | 분류코드 |
| section | string | 검색범위 |
| totalCnt | int | 페이지당 결과 수 |
| page | int | 페이지당 결과 수 |
| 법령 법령키 | int | 법령 법령키 |
| 법령ID | int | 법령ID |
| 법령명한글 | string | 법령명한글 |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 법령구분명 | string | 법령구분명 |
| 시행일자 | int | 시행일자 |
| 조문번호 | int | 조문번호 |
| 조문가지번호 | int | 조문가지번호 |
| 조문제목 | string | 조문제목 |
| 조문시행일자 | int | 조문시행일자 |
| 조문제개정유형 | string | 조문제개정유형 |
| 조문제개정일자문자열 | string | 조문제개정일자문자열 |
| 조문상세링크 | string | 조문상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=couseLs 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `custAdmrulListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=XML&vcode=A0000000000601`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=HTML&vcode=A0000000000601`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=XML&vcode=A0000000000601`

####  상세 내용


##### 맞춤형 행정규칙 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseAdmrul(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string(필수) | 분류코드 행정규칙은 A로 시작하는 14자리 코드(A0000000000001) |
| display | int | 검색된 결과 개  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 분류코드가 A0000000000601인 행정규칙 맞춤형 분류 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=XML&vcode=A0000000000601 |
| 2. 분류코드가 A0000000000601인 행정규칙 맞춤형 분류 HTML 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=HTML&vcode=A0000000000601 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| vcode | string | 분류코드 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| admrul id | int | 검색 결과 순번 |
| 행정규칙일련번호 | int | 행정규칙일련번호 |
| 행정규칙명 | string | 행정규칙명 |
| 행정규칙ID | int | 행정규칙ID |
| 발령일자 | int | 발령일자 |
| 발령번호 | int | 발령번호 |
| 행정규칙구분명 | string | 행정규칙구분명 |
| 소관부처코드 | int | 소관부처코드 |
| 소관부처명 | string | 소관부처명 |
| 제개정구분명 | string | 제개정구분명 |
| 행정규칙상세링크 | string | 행정규칙상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=couseAdmrul [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `custAdmrulJoListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=XML&lj=jo&vcode=A0000000000601`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=HTML&lj=jo&vcode=A0000000000601`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=XML&lj=jo&vcode=A0000000000601`

####  상세 내용


##### 맞춤형 행정규칙 조문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseAdmrul(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string(필수) | 분류코드 행정규칙은 A로 시작하는 14자리 코드(A0000000000001) |
| lj=jo | string(필수) | 조문여부 |
| display | int | 검색된 결과 개  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 분류코드가 A0000000000601인 행정규칙 조문 맞춤형 분류 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=XML&lj=jo&vcode=A0000000000601 |
| 2. 분류코드가 A0000000000601인 행정규칙 조문 맞춤형 분류 HTML 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseAdmrul&type=HTML&lj=jo&vcode=A0000000000601 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| vcode | string | 분류코드 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| 행정규칙일련번호 | int | 행정규칙일련번호 |
| 행정규칙명 | string | 행정규칙명 |
| 행정규칙ID | int | 행정규칙ID |
| 발령일자 | int | 발령일자 |
| 발령번호 | int | 발령번호 |
| 행정규칙구분명 | string | 행정규칙구분명 |
| 소관부처명 | string | 소관부처명 |
| 제개정구분명 | string | 제개정구분명 |
| 담당부서기관코드 | string | 담당부서기관코드 |
| 담당부서기관명 | string | 담당부서기관명 |
| 담당자명 | string | 담당자명 |
| 전화번호 | string | 전화번호 |
| 조문단위 조문키 | string | 조문단위 조문키 |
| 조문번호 | string | 조문번호 |
| 조문가지번호 | string | 조문가지번호 |
| 조문상세링크 | string | 조문상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=couseAdmrul [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `custOrdinListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=XML&vcode=O0000000000602`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=HTML&vcode=O0000000000602`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=XML&vcode=O0000000000602`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseOrdin(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string(필수) | 분류코드 자치법규는 O로 시작하는 14자리 코드(O0000000000001) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 맞춤형 자치법규 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseOrdin(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string(필수) | 분류코드 자치법규는 O로 시작하는 14자리 코드(O0000000000001) |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 분류코드가 O0000000000602인 자치법규 맞춤형 분류 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=XML&vcode=O0000000000602 |
| 2. 분류코드가 O0000000000602인 자치법규 맞춤형 분류 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=HTML&vcode=O0000000000602 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| vcode | string | 분류코드 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| ordin id | int | 결과 번호 |
| 자치법규일련번호 | int | 자치법규일련번호 |
| 자치법규명 | string | 자치법규명 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 자치법규종류 | string | 자치법규종류 |
| 지자체기관명 | string | 지자체기관명 |
| 시행일자 | int | 시행일자 |
| 자치법규분야명 | string | 자치법규분야명 |
| 자치법규상세링크 | string | 자치법규상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=couseOrdin 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `custOrdinJoListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=XML&lj=jo&vcode=O0000000000602`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=HTML&lj=jo&vcode=O0000000000602`
3. `http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=XML&lj=jo&vcode=O0000000000602`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseOrdin(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string | 분류코드(필수) 자치법규는 O로 시작하는 14자리 코드(O0000000000001) |
| lj=jo | string(필수) | 조문여부 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |



[TABLE_0]
####  상세 내용


##### 맞춤형 자치법규 조문 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : couseOrdin(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| vcode | string | 분류코드(필수) 자치법규는 O로 시작하는 14자리 코드(O0000000000001) |
| lj=jo | string(필수) | 조문여부 |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |


| 샘플 URL |
| --- |
| 1. 분류코드가 O0000000000602인 맞춤형 법령 분류 조문 목록 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=XML&lj=jo&vcode=O0000000000602 |
| 2. 분류코드가 O0000000000602인 맞춤형 법령 분류 조문 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=couseOrdin&type=HTML&lj=jo&vcode=O0000000000602 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| vcode | string | 분류코드 |
| section | string | 검색범위 |
| totalCnt | int | 검색건수 |
| page | int | 결과페이지번호 |
| 자치법규일련번호 | int | 자치법규일련번호 |
| 자치법규명 | string | 자치법규명 |
| 자치법규ID | int | 자치법규ID |
| 공포일자 | int | 공포일자 |
| 공포번호 | int | 공포번호 |
| 제개정구분명 | string | 제개정구분명 |
| 자치법규종류 | string | 자치법규종류 |
| 지자체기관명 | string | 지자체기관명 |
| 시행일자 | int | 시행일자 |
| 자치법규분야명 | string | 자치법규분야명 |
| 조문단위 조문키 | int | 조문단위 조문키 |
| 조문번호 | string | 조문번호 |
| 조문가지번호 | string | 조문가지번호 |
| 조문제목 | string | 조문제목 |
| 조문내용 | string | 조문내용 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=couseOrdin 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 지식베이스

### OPEN API 활용가이드

**API ID**: `lstrmAIGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrmAI&type=XML`
2. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrmAI&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?target=lstrmAI`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (법령용어 : lstrmAI) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 법령용어명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| homonymYn | char | 동음이의어 존재여부 (Y/N) |



[TABLE_0]
####  상세 내용


##### 법령정보지식베이스 법령용어 조회 API


###### 법령정보지식베이스 법령용어 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (법령용어 : lstrmAI) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 법령용어명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| homonymYn | char | 동음이의어 존재여부 (Y/N) |


| 샘플 URL |
| --- |
| 1. 법령정보지식베이스 법령용어 XML 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lstrmAI&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| 검색결과개수 | int | 검색 건수 |
| section | string | 검색범위 |
| page | int | 현재 페이지번호 |
| numOfRows | int | 페이지 당 출력 결과 수 |
| 법령용어 id | string | 법령용어 순번 |
| 법령용어명 | string | 법령용어명 |
| 동음이의어존재여부 | string | 동음이의어 존재여부 |
| 비고 | string | 동음이의어 내용 |
| 용어간관계링크 | string | 법령용어-일상용어 연계 정보 상세링크 |
| 조문간관계링크 | string | 법령용어-조문 연계 정보 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=lstrmAI [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `dlytrmGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=dlytrm&type=XML`
2. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=dlytrm&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?target=dlytrm`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (일상용어 : dlytrm) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 일상용어명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |



[TABLE_0]
####  상세 내용


##### 법령정보지식베이스 일상용어 조회 API


###### 법령정보지식베이스 일상용어 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (일상용어 : dlytrm) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 일상용어명에서 검색을 원하는 질의 |
| display | int | 검색된 결과 개수  (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |


| 샘플 URL |
| --- |
| 1. 법령정보지식베이스 일상용어 XML 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=dlytrm&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| 검색결과개수 | int | 검색 건수 |
| section | string | 검색범위 |
| page | int | 현재 페이지번호 |
| numOfRows | int | 페이지 당 출력 결과 수 |
| 일상용어 id | string | 일상용어 순번 |
| 일상용어명 | string | 일상용어명 |
| 출처 | string | 일상용어 출처 |
| 용어간관계링크 | string | 일상용어-법령용어 연계 정보 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=dlytrm [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lstrmRltGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lstrmRlt&type=XML&query=청원`
2. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=lstrmRlt&type=XML&query=청원`
3. `https://www.law.go.kr/DRF/lawService.do?target=lstrmRlt`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (법령용어-일상용어 연계 : lstrmRlt) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 법령용어명에서 검색을 원하는 질의 (query 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령용어명 일련번호 |
| trmRltCd | int | 용어관계 동의어 : 140301 반의어 : 140302 상위어 : 140303 하위어 : 140304 연관어 : 140305 |



[TABLE_0]
####  상세 내용


##### 법령정보지식베이스 법령용어-일상용어 연계 API


###### 법령정보지식베이스 법령용어-일상용어 연계 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (법령용어-일상용어 연계 : lstrmRlt) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 법령용어명에서 검색을 원하는 질의 (query 또는 MST 중 하나는 반드시 입력) |
| MST | char | 법령용어명 일련번호 |
| trmRltCd | int | 용어관계 동의어 : 140301 반의어 : 140302 상위어 : 140303 하위어 : 140304 연관어 : 140305 |


| 샘플 URL |
| --- |
| 1. 법령용어 청원 연계 일상용어 XML 조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=lstrmRlt&type=XML&query=청원 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| 검색결과개수 | int | 검색 건수 |
| 법령용어 id | string | 법령용어 순번 |
| 법령용어명 | string | 법령용어명 |
| 비고 | string | 동음이의어 내용 |
| 연계용어 id | string | 연계용어 순번 |
| 일상용어명 | string | 일상용어명 |
| 용어관계코드 | string | 용어관계코드 |
| 용어관계 | string | 용어관계명 |
| 일상용어조회링크 | string | 일상용어 정보 조회 링크 |
| 용어간관계링크 | string | 일상용어-법령용어 연계 정보 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=lstrmRlt [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `dlytrmRltGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=dlytrmRlt&type=XML&query=민원`
2. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=dlytrmRlt&type=XML&query=민원`
3. `https://www.law.go.kr/DRF/lawService.do?target=dlytrmRlt`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (일상용어-법령용어 연계 : dlytrmRlt) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 일상용어명에서 검색을 원하는 질의 (query 또는 MST 중 하나는 반드시 입력) |
| MST | char | 일상용어명 일련번호 |
| trmRltCd | int | 용어관계 동의어 : 140301 반의어 : 140302 상위어 : 140303 하위어 : 140304 연관어 : 140305 |



[TABLE_0]
####  상세 내용


##### 법령정보지식베이스 일상용어-법령용어 연계 API


###### 법령정보지식베이스 일상용어-법령용어 연계 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (일상용어-법령용어 연계 : dlytrmRlt) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 일상용어명에서 검색을 원하는 질의 (query 또는 MST 중 하나는 반드시 입력) |
| MST | char | 일상용어명 일련번호 |
| trmRltCd | int | 용어관계 동의어 : 140301 반의어 : 140302 상위어 : 140303 하위어 : 140304 연관어 : 140305 |


| 샘플 URL |
| --- |
| 1. 일상용어 민원 연계 법령용어 정보 XML 조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=dlytrmRlt&type=XML&query=민원 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| 검색결과개수 | int | 검색 건수 |
| 일상용어명 | string | 일상용어명 |
| 출처 | string | 일상용어 출처 |
| 연계용어 id | string | 연계용어 순번 |
| 법령용어명 | string | 법령용어명 |
| 비고 | string | 동음이의어 내용 |
| 용어관계코드 | string | 용어관계코드 |
| 용어관계 | string | 용어관계명 |
| 용어간관계링크 | string | 법령용어-일상용어 연계 정보 상세링크 |
| 조문간관계링크 | string | 법령용어-조문 연계 정보 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=dlytrmRlt [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lstrmRltJoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=lstrmRltJo&type=XML&query=민원`
2. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=lstrmRltJo&type=XML&query=민원`
3. `https://www.law.go.kr/DRF/lawService.do?target=lstrmRltJo`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (법령용어-조문 연계 : lstrmRltJo) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string(필수) | 법령용어명에서 검색을 원하는 질의 |



[TABLE_0]
####  상세 내용


##### 법령정보지식베이스 법령용어-조문 연계 API


###### 법령정보지식베이스 법령용어-조문 연계 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (법령용어-조문 연계 : lstrmRltJo) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string(필수) | 법령용어명에서 검색을 원하는 질의 |


| 샘플 URL |
| --- |
| 1. 법령용어 민원 연계 조문 정보 XML 조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=lstrmRltJo&type=XML&query=민원 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| 검색결과개수 | int | 검색 건수 |
| 법령용어 id | string | 법령용어 순번 |
| 법령용어명 | string | 법령용어명 |
| 비고 | string | 동음이의어 내용 |
| 용어간관계링크 | string | 법령용어-일상용어 연계 정보 상세링크 |
| 연계법령 id | string | 연계법령 순번 |
| 법령명 | string | 법령명 |
| 조번호 | int | 조번호 |
| 조가지번호 | int | 조가지번호 |
| 조문내용 | string | 조문내용 |
| 용어구분코드 | string | 용어구분코드 |
| 용어구분 | string | 용어구분명 |
| 조문연계용어링크 | string | 조문-법령용어 연계 정보 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=lstrmRltJo [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `lsRltGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsRlt&type=XML`
2. `https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsRlt&type=XML`
3. `https://www.law.go.kr/DRF/lawSearch.do?target=lsRlt`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (관련법령 : lsRlt) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 기준법령명에서 검색을 원하는 질의 |
| ID | int | 법령 ID |
| lsRltCd | int | 법령 간 관계 코드 |



[TABLE_0]
####  상세 내용


##### 법령정보지식베이스 관련법령 API


###### 법령정보지식베이스 관련법령 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (관련법령 : lsRlt) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 기준법령명에서 검색을 원하는 질의 |
| ID | int | 법령 ID |
| lsRltCd | int | 법령 간 관계 코드 |


| 샘플 URL |
| --- |
| 1. 법령정보지식베이스 관련법령 XML 조회 |
| https://www.law.go.kr/DRF/lawSearch.do?OC=test&target=lsRlt&type=XML |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| 검색결과개수 | int | 검색 건수 |
| 기준법령ID | int | 기준법령 ID |
| 기준법령명 | string | 기준법령명 |
| 기준법령상세링크 | string | 기준법령 본문 조회링크 |
| 관련법령 id | string | 관련법령 순번 |
| 관련법령ID | int | 관련법령 ID |
| 관련법령명 | string | 관련법령명 |
| 법령간관계코드 | string | 법령간관계코드 |
| 법령간관계 | string | 법령간관계 |
| 관련법령상세링크 | string | 관련법령 본문 조회링크 |
| 관련법령조회링크 | string | 해당 관련법령을 기준법령으로 한 관련법령 정보 조회링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawSearch.do?target=lsRlt [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 기타

### OPEN API 활용가이드

**API ID**: `joRltLstrmGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=joRltLstrm&type=XML&query=상법시행법&JO=000400`
2. `https://www.law.go.kr/DRF/lawService.do?OC=test&target=joRltLstrm&type=XML&query=상법시행법&JO=000400`
3. `https://www.law.go.kr/DRF/lawService.do?target=joRltLstrm`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (조문-법령용어 연계 : joRltLstrm) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 (query 또는 ID 중 하나는 반드시 입력) |
| ID | int | 법령 ID |
| JO | int(필수) | 조번호 조번호 4자리 + 조가지번호 2자리 (000200 : 2조, 000202 : 제2조의2) |



[TABLE_0]
####  상세 내용


##### 법령정보지식베이스 조문-법령용어 연계 API


###### 법령정보지식베이스 조문-법령용어 연계 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID (g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string(필수) | 서비스 대상 (조문-법령용어 연계 : joRltLstrm) |
| type | char(필수) | 출력 형태 : XML/JSON |
| query | string | 법령명에서 검색을 원하는 질의 (query 또는 ID 중 하나는 반드시 입력) |
| ID | int | 법령 ID |
| JO | int(필수) | 조번호 조번호 4자리 + 조가지번호 2자리 (000200 : 2조, 000202 : 제2조의2) |


| 샘플 URL |
| --- |
| 1. 상법시행법 제4조 연계 법령용어 정보 XML 조회 |
| https://www.law.go.kr/DRF/lawService.do?OC=test&target=joRltLstrm&type=XML&query=상법시행법&JO=000400 |


| 필드 | 값 | 설명 | target | string | 검색서비스 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 검색 단어 |
| 검색결과개수 | int | 검색 건수 |
| 법령조문 id | string | 법령조문 순번 |
| 법령명 | string | 법령명 |
| 조번호 | int | 조번호 |
| 조가지번호 | int | 조가지번호 |
| 조문내용 | string | 조문내용 |
| 연계용어 id | string | 연계용어 순번 |
| 법령용어명 | string | 법령용어명 |
| 비고 | string | 동음이의어 내용 |
| 용어구분코드 | string | 용어구분코드 |
| 용어구분 | string | 용어구분명 |
| 용어간관계링크 | string | 법령용어-일상용어 연계 정보 상세링크 |
| 용어연계조문링크 | string | 법령용어-조문 연계 정보 상세링크 |



[HEADING_0] - 요청 URL : https://www.law.go.kr/DRF/lawService.do?target=joRltLstrm [HEADING_1] 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

## 중앙부처해석

### OPEN API 활용가이드

**API ID**: `cgmExpcMoelListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moelCgmExpc&type=XML&query=퇴직`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moelCgmExpc&type=HTML&query=월급`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moelCgmExpc&type=JSON&query=연차`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moelCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="퇴직") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 고용노동부 법령해석 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moelCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="퇴직") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 안건명에 '퇴직'이 들어가는 법령해석 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moelCgmExpc&type=XML&query=퇴직 |
| 2. 안건명에 '월급'이 들어가는 법령해석 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moelCgmExpc&type=HTML&query=월급 |
| 3. 안건명에 '연차'가 들어가는 법령해석 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moelCgmExpc&type=JSON&query=연차 |


| 요청변수 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| id | int | 검색결과번호 |
| 법령해석일련번호 | int | 법령해석일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 해석기관코드 | string | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 해석일자 | string | 해석일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 법령해석상세링크 | string | 법령해석상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=moelCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMoelInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=moelCgmExpc&ID=21822&type=XML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=moelCgmExpc&ID=21822&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=moelCgmExpc&ID=21822&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moelCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 고용노동부 법령해석 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moelCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 법령해석일련번호가 21822인 해석 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=moelCgmExpc&ID=21822&type=XML |
| 2. 법령해석일련번호가 21822인 해석 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=moelCgmExpc&ID=21822&type=HTML |
| 3. 법령해석일련번호가 21822인 해석 JSON 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=moelCgmExpc&ID=21822&type=JSON |


| 필드 | 값 | 설명 | 법령해석일련번호 | int | 법령해석일련번호 |
| --- | --- | --- | --- | --- | --- |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 해석일자 | int | 해석일자 |
| 해석기관코드 | int | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 관리기관코드 | int | 관리기관코드 |
| 등록일시 | int | 등록일시 |
| 질의요지 | string | 질의요지 |
| 회답 | string | 회답 |
| 이유 | string | 이유 |
| 관련법령 | string | 관련법령 |
| 데이터기준일시 | string | 데이터기준일시 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=moelCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMolitListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=molitCgmExpc&type=XML&query=도로`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=molitCgmExpc&type=HTML&query=아파트`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=molitCgmExpc&type=JSON&query=상업`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : molitCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="도로") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 국토교통부 법령해석 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : molitCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="도로") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 안건명에 '도로'가 들어가는 법령해석 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=molitCgmExpc&type=XML&query=도로 |
| 2. 안건명에 '아파트'가 들어가는 법령해석 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=molitCgmExpc&type=HTML&query=아파트 |
| 3. 안건명에 '상업'이 들어가는 법령해석 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=molitCgmExpc&type=JSON&query=상업 |


| 요청변수 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| id | int | 검색결과번호 |
| 법령해석일련번호 | int | 법령해석일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 해석기관코드 | string | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 해석일자 | string | 해석일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 법령해석상세링크 | string | 법령해석상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=molitCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMolitInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=molitCgmExpc&ID=315912&type=XML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=molitCgmExpc&ID=315912&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=molitCgmExpc&ID=315912&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : molitCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 국토교통부 법령해석 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : molitCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 법령해석일련번호가 315912인 해석 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=molitCgmExpc&ID=315912&type=XML |
| 2. 법령해석일련번호가 315912인 해석 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=molitCgmExpc&ID=315912&type=HTML |
| 3. 법령해석일련번호가 315912인 해석 JSON 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=molitCgmExpc&ID=315912&type=JSON |


| 필드 | 값 | 설명 | 법령해석일련번호 | int | 법령해석일련번호 |
| --- | --- | --- | --- | --- | --- |
| 대분류 | string | 대분류 |
| 중분류 | string | 중분류 |
| 소분류 | string | 소분류 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 해석일자 | int | 해석일자 |
| 해석기관코드 | int | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 관리기관코드 | int | 관리기관코드 |
| 등록일시 | int | 등록일시 |
| 질의요지 | string | 질의요지 |
| 회답 | string | 회답 |
| 이유 | string | 이유 |
| 관련법령 | string | 관련법령 |
| 데이터기준일시 | string | 데이터기준일시 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=molitCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMoefListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moefCgmExpc&type=XML&query=조합`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moefCgmExpc&type=HTML&query=승계`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moefCgmExpc&type=JSON&query=지분`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moefCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="조합") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 기획재정부 법령해석 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moefCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="조합") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 안건명에 '조합'이 들어가는 법령해석 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moefCgmExpc&type=XML&query=조합 |
| 2. 안건명에 '승계'가 들어가는 법령해석 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moefCgmExpc&type=HTML&query=승계 |
| 3. 안건명에 '지분'이 들어가는 법령해석 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moefCgmExpc&type=JSON&query=지분 |


| 요청변수 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| id | int | 검색결과번호 |
| 법령해석일련번호 | int | 법령해석일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 해석기관코드 | string | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 해석일자 | string | 해석일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 법령해석상세링크 | string | 법령해석상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=moefCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMofListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=mofCgmExpc&type=XML&query=항만`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=mofCgmExpc&type=HTML&query=비관리청`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=mofCgmExpc&type=JSON&query=시설`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : mofCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="폐기물") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 해양수산부 법령해석 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : mofCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="폐기물") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 안건명에 '항만'이 들어가는 법령해석 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=mofCgmExpc&type=XML&query=항만 |
| 2. 안건명에 '비관리청'가 들어가는 법령해석 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=mofCgmExpc&type=HTML&query=비관리청 |
| 3. 안건명에 '시설'가 들어가는 법령해석 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=mofCgmExpc&type=JSON&query=시설 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| id | int | 검색결과번호 |
| 법령해석일련번호 | int | 법령해석일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 해석기관코드 | string | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 해석일자 | string | 해석일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 법령해석상세링크 | string | 법령해석상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=mofCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMofInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=mofCgmExpc&ID=319468&type=XML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=mofCgmExpc&ID=319468&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=mofCgmExpc&ID=319468&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : mofCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 해양수산부 법령해석 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : mofCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 법령해석일련번호가 319468인 해석 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=mofCgmExpc&ID=319468&type=XML |
| 2. 법령해석일련번호가 319468인 해석 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=mofCgmExpc&ID=319468&type=HTML |
| 3. 법령해석일련번호가 319468인 해석 JSON 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=mofCgmExpc&ID=319468&type=JSON |


| 필드 | 값 | 설명 | 법령해석일련번호 | int | 법령해석일련번호 |
| --- | --- | --- | --- | --- | --- |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 해석일자 | int | 해석일자 |
| 해석기관코드 | int | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 관리기관코드 | int | 관리기관코드 |
| 등록일시 | int | 등록일시 |
| 질의요지 | string | 질의요지 |
| 회답 | string | 회답 |
| 이유 | string | 이유 |
| 관련법령 | string | 관련법령 |
| 데이터기준일시 | string | 데이터기준일시 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=mofCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMoisListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moisCgmExpc&type=XML&query=재해`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moisCgmExpc&type=HTML&query=임대`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=moisCgmExpc&type=JSON&query=행정`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moisCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="재해") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 행정안전부 법령해석 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moisCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="재해") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 안건명에 '재해'가 들어가는 법령해석 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moisCgmExpc&type=XML&query=재해 |
| 2. 안건명에 '임대'가 들어가는 법령해석 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moisCgmExpc&type=HTML&query=임대 |
| 3. 안건명에 '행정'이 들어가는 법령해석 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=moisCgmExpc&type=JSON&query=행정 |


| 요청변수 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| id | int | 검색결과번호 |
| 법령해석일련번호 | int | 법령해석일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 해석기관코드 | string | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 해석일자 | string | 해석일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 법령해석상세링크 | string | 법령해석상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=moisCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMoisInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=moisCgmExpc&ID=279110&type=XML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=moisCgmExpc&ID=279110&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=moisCgmExpc&ID=279110&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moisCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 행정안전부 법령해석 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : moisCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 법령해석일련번호가 279110인 해석 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=moisCgmExpc&ID=279110&type=XML |
| 2. 법령해석일련번호가 279110인 해석 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=moisCgmExpc&ID=279110&type=HTML |
| 3. 법령해석일련번호가 279110인 해석 JSON 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=moisCgmExpc&ID=279110&type=JSON |


| 필드 | 값 | 설명 | 법령해석일련번호 | int | 법령해석일련번호 |
| --- | --- | --- | --- | --- | --- |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 해석일자 | int | 해석일자 |
| 해석기관코드 | int | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 관리기관코드 | int | 관리기관코드 |
| 등록일시 | int | 등록일시 |
| 질의요지 | string | 질의요지 |
| 회답 | string | 회답 |
| 이유 | string | 이유 |
| 관련법령 | string | 관련법령 |
| 데이터기준일시 | string | 데이터기준일시 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=moisCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMeListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=meCgmExpc&type=XML&query=폐기물`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=meCgmExpc&type=HTML&query=오염`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=meCgmExpc&type=JSON&query=대기`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : meCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="폐기물") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 환경부 법령해석 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : meCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="폐기물") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 안건명에 '폐기물'이 들어가는 법령해석 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=meCgmExpc&type=XML&query=폐기물 |
| 2. 안건명에 '오염'이 들어가는 법령해석 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=meCgmExpc&type=HTML&query=오염 |
| 3. 안건명에 '대기'가 들어가는 법령해석 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=meCgmExpc&type=JSON&query=대기 |


| 필드 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| id | int | 검색결과번호 |
| 법령해석일련번호 | int | 법령해석일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 해석기관코드 | string | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 해석일자 | string | 해석일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 법령해석상세링크 | string | 법령해석상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=meCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcMeInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=meCgmExpc&ID=9636&type=XML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=meCgmExpc&ID=9636&type=HTML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=meCgmExpc&ID=9636&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : meCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 환경부 법령해석 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : meCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 법령해석일련번호가 9636인 해석 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=meCgmExpc&ID=9636&type=XML |
| 2. 법령해석일련번호가 9636인 해석 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=meCgmExpc&ID=9636&type=HTML |
| 3. 법령해석일련번호가 9636인 해석 JSON 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=meCgmExpc&ID=9636&type=JSON |


| 필드 | 값 | 설명 | 법령해석일련번호 | int | 법령해석일련번호 |
| --- | --- | --- | --- | --- | --- |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 해석일자 | int | 해석일자 |
| 해석기관코드 | int | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 관리기관코드 | int | 관리기관코드 |
| 등록일시 | int | 등록일시 |
| 질의요지 | string | 질의요지 |
| 회답 | string | 회답 |
| 이유 | string | 이유 |
| 관련법령 | string | 관련법령 |
| 데이터기준일시 | string | 데이터기준일시 |





[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=meCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2] [TABLE_3]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcKcsListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcsCgmExpc&type=XML&query=거래명세서`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcsCgmExpc&type=HTML&query=세금`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcsCgmExpc&type=JSON&query=생산`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : kcsCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="거래명세서") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 관세청 법령해석 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : kcsCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="거래명세서") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 안건명에 '거래명세서'가 들어가는 법령해석 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcsCgmExpc&type=XML&query=거래명세서 |
| 2. 안건명에 '세금'이 들어가는 법령해석 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcsCgmExpc&type=HTML&query=세금 |
| 3. 안건명에 '생산'이 들어가는 법령해석 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=kcsCgmExpc&type=JSON&query=생산 |


| 요청변수 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| id | int | 검색결과번호 |
| 법령해석일련번호 | int | 법령해석일련번호 |
| 안건명 | string | 안건명 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 해석기관코드 | string | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 해석일자 | string | 해석일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 법령해석상세링크 | string | 법령해석상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=kcsCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcKcsInfoGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawService.do?OC=test&target=kcsCgmExpc&ID=31584&type=HTML`
2. `//www.law.go.kr/DRF/lawService.do?OC=test&target=kcsCgmExpc&ID=31584&type=XML`
3. `//www.law.go.kr/DRF/lawService.do?OC=test&target=kcsCgmExpc&ID=31584&type=JSON`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : kcsCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 해석일자, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 관세청 법령해석 본문 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : kcsCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| ID | int(필수) | 법령해석일련번호 |
| LM | string | 법령해석명 |
| fields | string | 응답항목 옵션(안건명, 해석일자, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 법령해석일련번호가 31584인 해석 HTML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=kcsCgmExpc&ID=31584&type=HTML |
| 2. 법령해석일련번호가 31584인 해석 XML 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=kcsCgmExpc&ID=31584&type=XML |
| 3. 법령해석일련번호가 31584인 해석 JSON 조회 |
| http://www.law.go.kr/DRF/lawService.do?OC=test&target=kcsCgmExpc&ID=31584&type=JSON |


| 필드 | 값 | 설명 | 법령해석일련번호 | int | 법령해석일련번호 |
| --- | --- | --- | --- | --- | --- |
| 업무분야 | string | 업무분야 |
| 안건명 | string | 안건명 |
| 해석일자 | int | 해석일자 |
| 해석기관코드 | int | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 관리기관코드 | int | 관리기관코드 |
| 등록일시 | int | 등록일시 |
| 질의요지 | string | 질의요지 |
| 회답 | string | 회답 |
| 이유 | string | 이유 |
| 관련법령 | string | 관련법령 |
| 관세법령정보포털원문링크 | string | 관세법령정보포털원문링크 |
| 데이터기준일시 | string | 데이터기준일시 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawService.do?target=kcsCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

### OPEN API 활용가이드

**API ID**: `cgmExpcNtsListGuide`

**상태**:  성공

**샘플 URL**:
1. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ntsCgmExpc&type=XML&query=세금`
2. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ntsCgmExpc&type=HTML&query=증여`
3. `//www.law.go.kr/DRF/lawSearch.do?OC=test&target=ntsCgmExpc&type=JSON&query=재산`

#### 요청 파라미터


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ntsCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="세금") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |



[TABLE_0]
####  상세 내용


##### 국세청 법령해석 목록 조회 API


| 요청변수 | 값 | 설명 | OC | string(필수) | 사용자 이메일의 ID(g4c@korea.kr일경우 OC값=g4c) |
| --- | --- | --- | --- | --- | --- |
| target | string : ntsCgmExpc(필수) | 서비스 대상 |
| type | char(필수) | 출력 형태 : HTML/XML/JSON |
| search | int | 검색범위 (기본 : 1 법령해석명, 2: 본문검색) |
| query | string | 검색범위에서 검색을 원하는 질의 (정확한 검색을 위한 문자열 검색 query="세금") |
| display | int | 검색된 결과 개수 (default=20 max=100) |
| page | int | 검색 결과 페이지 (default=1) |
| inq | int | 질의기관코드 |
| rpl | int | 해석기관코드 |
| gana | string | 사전식 검색(ga,na,da…,etc) |
| itmno | int | 안건번호 * 안건번호 변수 적용 시 query 요청변수는 무시됩니다. |
| explYd | string | 해석일자 검색(20090101~20090130) |
| sort | string | 정렬옵션 (기본 : lasc 법령해석명 오름차순) ldes 법령해석명 내림차순 dasc : 해석일자 오름차순 ddes : 해석일자 내림차순 nasc : 안건번호 오름차순 ndes : 안건번호 내림차순 |
| popYn | string | 상세화면 팝업창 여부(팝업창으로 띄우고 싶을 때만 'popYn=Y') |
| fields | string | 응답항목 옵션(안건명, 안건번호, ...) * 빈 값일 경우 전체 항목 표출 * 출력 형태 HTML일 경우 적용 불가능 |


| 샘플 URL |
| --- |
| 1. 안건명에 '세금'이 들어가는 법령해석 목록 XML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ntsCgmExpc&type=XML&query=세금 |
| 2. 안건명에 '증여'가 들어가는 법령해석 목록 HTML 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ntsCgmExpc&type=HTML&query=증여 |
| 3. 안건명에 '재산'이 들어가는 법령해석 목록 JSON 검색 |
| http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=ntsCgmExpc&type=JSON&query=재산 |


| 요청변수 | 값 | 설명 | target | string | 검색 대상 |
| --- | --- | --- | --- | --- | --- |
| 키워드 | string | 키워드 |
| section | string | 검색범위(lawNm:법령해석명/bdyText:본문) |
| totalCnt | int | 검색결과갯수 |
| page | int | 출력페이지 |
| id | int | 검색결과번호 |
| 법령해석일련번호 | int | 법령해석일련번호 |
| 안건명 | string | 안건명 |
| 안건번호 | string | 안건번호 |
| 질의기관코드 | int | 질의기관코드 |
| 질의기관명 | string | 질의기관명 |
| 해석기관코드 | string | 해석기관코드 |
| 해석기관명 | string | 해석기관명 |
| 해석일자 | string | 해석일자 |
| 데이터기준일시 | string | 데이터기준일시 |
| 법령해석상세링크 | string | 법령해석상세링크 |



[HEADING_0] - 요청 URL : http://www.law.go.kr/DRF/lawSearch.do?target=ntsCgmExpc 요청 변수 (request parameter) [TABLE_0] [TABLE_1] 출력 결과 필드(response field) [TABLE_2]

---

##  수집 통계

- 총 API 수: 121
- 성공: 121
- 실패: 0
- 성공률: 100.0%


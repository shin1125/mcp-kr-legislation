[한국어] | [English](README_en.md)

# MCP 한국 법령 종합 정보 서버

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastMCP](https://img.shields.io/badge/FastMCP-Latest-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/ChangooLee/mcp-kr-legislation)
![GitHub Issues](https://img.shields.io/github/issues/ChangooLee/mcp-kr-legislation)

한국 법제처 OPEN API를 통합한 Model Context Protocol(MCP) 서버입니다. **150개 이상의 포괄적인 도구**를 통해 법령, 부가서비스, 행정규칙, 자치법규, 판례, 위원회결정문, 조약, 별표서식, 학칙공단, 법령용어, 맞춤형, 지식베이스, 특별행정심판, 중앙부처해석 등 **모든 법률 정보에 대한 접근**을 제공합니다.

**GitHub Repository**: https://github.com/ChangooLee/mcp-kr-legislation

---

## 주요 특징

- ** 포괄적 법령 정보**: 현행법부터 판례, 조약, 위원회 결정문까지 모든 법령 정보
- ** 지능형 검색**: 다단계 검색으로 정확한 법령 찾기 + 검색어 자동 정규화
- ** 강력한 검색**: 법령명, 본문 내용, 소관부처별 상세 검색 지원
- ** 다국어 지원**: 한글 원문과 영문 번역본 모두 제공
- **⚡ 실시간 업데이트**: 법제처 실시간 데이터 연동
- ** 직접 API 접근**: 각 응답에 실제 API URL 포함으로 직접 확인 가능
- ** 풍부한 정보**: 법령 조문, 판례 요지, 위원회 결정 이유 등 상세 내용 제공
- **✨ 품질 향상**: 빈 제목 필터링, 관련성 기반 결과 정렬
- ** AI 친화적**: Claude Desktop 등 AI 도구와 완벽 통합

---

## 사용 예시

AI 어시스턴트에게 다음과 같은 요청을 할 수 있습니다:

### 기본 검색 질문들
- ** 법령 검색** - "개인정보보호법의 최신 내용을 찾아주세요"
- ** 판례 조회** - "개인정보보호 관련 최근 판례를 검색해주세요"
- **📖 조약 확인** - "한국이 체결한 FTA 조약을 찾아주세요"
- **🏛️ 자치법규** - "서울시의 개인정보보호 관련 조례를 찾아주세요"
- ** 행정규칙** - "고용노동부의 근로자 보호 관련 규칙을 보여주세요"

### 고급 검색 질문들
- **🔬 종합 분석** - "금융사의 결혼여부 정보 수집에 대한 법적 근거를 체계적으로 조사하여 종합 레포트를 작성해줘"
- **⚖️ 판례 분석** - "개인정보보호법 위반 사건의 최근 5년간 판례 동향을 분석해줘"
- **🏛️ 위원회 결정례** - "개인정보보호위원회의 결혼여부 수집 관련 결정문을 찾아줘"
- ** 법령 비교** - "개인정보보호법과 신용정보법의 개인정보 수집 규정을 비교해줘"

---

## 🛠️ 지원 도구 전체 목록 (카테고리별)

### 1. 법령 관련 도구 (8개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_law` | 현행 법령 검색 | "개인정보보호법을 검색해줘" |
| `get_law_detail` | 특정 법령 상세 조회 | "법령ID 011357의 상세 내용을 보여줘" |
| `search_english_law` | 영문 법령 검색 | "Personal Information Protection Act를 찾아줘" |
| `search_effective_law` | 시행일 법령 검색 | "최근 시행 예정인 개인정보 관련 법령은?" |
| `search_law_nickname` | 법령 약칭 검색 | "개보법이라는 약칭의 정식 법령명은?" |
| `search_deleted_law_data` | 삭제된 법령 데이터 검색 | "폐지된 개인정보 관련 법령을 찾아줘" |
| `search_law_articles` | 법령 조문 검색 | "개인정보보호법의 조문별 내용을 보여줘" |

### 2. 부가서비스 도구 (5개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_old_and_new_law` | 신구법 비교 | "개인정보보호법의 개정 전후 비교를 보여줘" |
| `search_three_way_comparison` | 3단 비교 | "개인정보보호법의 3단계 비교를 보여줘" |
| `search_deleted_history` | 삭제 이력 조회 | "최근 삭제된 법령 데이터는?" |
| `search_one_view` | 한눈보기 | "개인정보보호법의 요약 정보를 보여줘" |
| `search_law_system_diagram` | 법령 체계도 | "개인정보보호법의 법령 체계도를 보여줘" |
| `get_law_system_diagram_detail` | 체계도 상세 조회 | "법령 체계도 상세 내용을 보여줘" |
| `get_delegated_law` | 위임법령 조회 | "개인정보보호법의 위임법령을 보여줘" |

### 3. 행정규칙 도구 (5개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_administrative_rule` | 행정규칙 검색 | "개인정보보호 관련 행정규칙을 찾아줘" |
| `get_administrative_rule_detail` | 행정규칙 상세 조회 | "특정 행정규칙의 본문을 보여줘" |
| `search_administrative_rule_comparison` | 행정규칙 신구법 비교 | "행정규칙의 개정 전후를 비교해줘" |
| `get_administrative_rule_comparison_detail` | 비교 상세 조회 | "행정규칙 비교의 상세 내용을 보여줘" |

### 4. 자치법규 도구 (4개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_local_ordinance` | 자치법규 검색 | "서울시 개인정보보호 조례를 찾아줘" |
| `search_ordinance_appendix` | 자치법규 별표서식 | "조례의 별표와 서식을 보여줘" |
| `search_linked_ordinance` | 연계 자치법규 | "개인정보보호법과 연계된 조례는?" |

### 5. 판례 관련 도구 (5개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_precedent` | 대법원 판례 검색 | "개인정보보호 관련 판례를 찾아줘" |
| `search_constitutional_court` | 헌재 결정례 검색 | "개인정보보호 관련 헌법재판소 결정례는?" |
| `search_legal_interpretation` | 법령해석례 검색 | "개인정보수집 관련 법령해석례를 보여줘" |
| `search_administrative_trial` | 행정심판례 검색 | "개인정보보호 관련 행정심판례는?" |
| `get_administrative_trial_detail` | 행정심판례 상세 조회 | "특정 행정심판례의 상세 내용을 보여줘" |

### 6. 위원회 결정문 도구 (24개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_privacy_committee` | 개인정보보호위원회 | "개인정보보호위원회의 결혼여부 수집 관련 결정문은?" |
| `search_financial_committee` | 금융위원회 | "금융위원회의 개인정보 관련 결정문은?" |
| `search_monopoly_committee` | 공정거래위원회 | "공정거래위원회의 개인정보 관련 결정문은?" |
| `search_anticorruption_committee` | 국민권익위원회 | "국민권익위원회 결정문을 찾아줘" |
| `search_labor_committee` | 노동위원회 | "노동위원회의 개인정보 관련 결정문은?" |
| `search_environment_committee` | 중앙환경분쟁조정위원회 | "환경위원회 결정문을 보여줘" |
| `search_securities_committee` | 증권선물위원회 | "증권위원회의 개인정보 관련 결정문은?" |
| `search_human_rights_committee` | 국가인권위원회 | "인권위원회의 개인정보 관련 결정문은?" |
| `search_broadcasting_committee` | 방송통신위원회 | "방통위원회 결정문을 찾아줘" |
| `search_industrial_accident_committee` | 산재보상보험재심사위원회 | "산재위원회 결정문을 보여줘" |
| `search_land_tribunal` | 중앙토지수용위원회 | "토지수용위원회 결정문을 찾아줘" |
| `search_employment_insurance_committee` | 고용보험심사위원회 | "고용보험심사위원회 결정문을 보여줘" |
| `get_employment_insurance_committee_detail` | 고용보험심사위 상세 조회 | "특정 고용보험 결정문의 상세 내용을 보여줘" |

### 7. 조약 도구 (2개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_treaty` | 조약 검색 | "개인정보보호 관련 국제조약을 찾아줘" |

### 8. 별표서식 도구 (2개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_law_appendix` | 법령 별표서식 검색 | "개인정보보호법의 별표와 서식을 보여줘" |

### 9. 학칙·공단·공공기관 도구 (6개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_university_regulation` | 대학 학칙 검색 | "대학의 개인정보보호 관련 학칙을 찾아줘" |
| `search_public_corporation_regulation` | 지방공사공단 규정 | "공단의 개인정보 관련 규정을 보여줘" |
| `search_public_institution_regulation` | 공공기관 규정 | "공공기관의 개인정보 규정을 찾아줘" |
| `get_university_regulation_detail` | 대학 학칙 상세 조회 | "특정 대학 학칙의 상세 내용을 보여줜" |
| `get_public_corporation_regulation_detail` | 공사공단 규정 상세 | "공단 규정의 상세 내용을 보여줘" |
| `get_public_institution_regulation_detail` | 공공기관 규정 상세 | "공공기관 규정의 상세 내용을 보여줘" |

### 10. 특별행정심판 도구 (4개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_tax_tribunal` | 조세심판원 | "조세심판원의 개인정보 관련 심판례는?" |
| `get_tax_tribunal_detail` | 조세심판원 상세 조회 | "특정 조세심판 사건의 상세 내용을 보여줘" |
| `search_maritime_safety_tribunal` | 해양안전심판원 | "해양안전심판원 심판례를 찾아줘" |
| `get_maritime_safety_tribunal_detail` | 해양안전심판원 상세 | "해양안전심판 사건의 상세 내용을 보여줘" |

### 11. 법령용어 도구 (2개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_legal_term` | 법령용어 검색 | "개인정보의 법령용어 정의를 보여줘" |

| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|

### 12. 맞춤형 서비스 도구 (6개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_custom_law` | 맞춤형 법령 검색 | "분류코드별 맞춤형 법령을 보여줘" |
| `search_custom_law_articles` | 맞춤형 법령 조문 | "맞춤형 법령의 조문별 내용을 찾아줘" |
| `search_custom_ordinance` | 맞춤형 자치법규 | "맞춤형 자치법규를 보여줘" |
| `search_custom_ordinance_articles` | 맞춤형 자치법규 조문 | "맞춤형 자치법규 조문을 찾아줘" |
| `search_custom_precedent` | 맞춤형 판례 | "맞춤형 판례를 보여줘" |

### 14. 지식베이스 도구 (7개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_legal_ai` | 법령 AI 지식베이스 | "AI 기반 개인정보보호 정보를 보여줘" |
| `search_knowledge_base` | 지식베이스 검색 | "개인정보보호 지식베이스를 찾아줘" |
| `search_faq` | 자주 묻는 질문 | "개인정보보호 관련 FAQ를 보여줘" |
| `search_qna` | 질의응답 | "개인정보수집 관련 Q&A를 찾아줘" |
| `search_counsel` | 상담 내용 | "개인정보보호 상담 사례를 보여줘" |
| `search_precedent_counsel` | 판례 상담 | "판례 관련 상담 내용을 찾아줘" |

### 15. 민원 도구 (1개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_civil_petition` | 민원 검색 | "개인정보보호 관련 민원 사례를 보여줘" |

### 16. 중앙부처 해석 도구 (14개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_moef_interpretation` | 기획재정부 해석 | "기획재정부의 개인정보 관련 해석을 보여줘" |
| `search_molit_interpretation` | 국토교통부 해석 | "국토교통부의 법령해석을 찾아줘" |
| `search_moel_interpretation` | 고용노동부 해석 | "고용노동부의 개인정보 관련 해석은?" |
| `search_mof_interpretation` | 해양수산부 해석 | "해양수산부 법령해석을 보여줘" |
| `search_mohw_interpretation` | 보건복지부 해석 | "보건복지부의 개인정보 관련 해석은?" |
| `search_moe_interpretation` | 교육부 해석 | "교육부 법령해석을 찾아줘" |
| `search_korea_interpretation` | 범정부 해석 | "범정부 차원의 법령해석을 보여줘" |
| `search_mssp_interpretation` | 보훈처 해석 | "보훈처 법령해석을 찾아줘" |
| `search_mote_interpretation` | 산업통상자원부 해석 | "산업부 법령해석을 보여줘" |
| `search_maf_interpretation` | 농림축산식품부 해석 | "농림부 법령해석을 찾아줘" |
| `search_moms_interpretation` | 국방부 해석 | "국방부 법령해석을 보여줘" |
| `search_sme_interpretation` | 중소벤처기업부 해석 | "중기부 법령해석을 찾아줘" |
| `search_nfa_interpretation` | 산림청 해석 | "산림청 법령해석을 보여줘" |
| `search_korail_interpretation` | 한국철도공사 해석 | "철도공사 법령해석을 찾아줘" |

### 17. 종합 검색 도구 (1개)
| 도구명 | 설명 | 테스트 질문 |
|--------|------|------------|
| `search_all_legal_documents` | 통합 검색 | "개인정보보호 관련 모든 법률 문서를 종합 검색해줘" |

**총 150개 이상의 포괄적 도구로 한국의 모든 법령 정보에 접근 가능**

---

## 빠른 시작 가이드

### 1. API 키 설정

한국 법제처 API는 **무료**로 제공되며, 이메일 주소만으로 사용 가능합니다:

1. 별도 회원가입이나 신청 절차 불필요
2. 본인의 이메일 주소를 API 키로 사용
3. 즉시 사용 가능

### 2. 설치

```bash
# 저장소 복제
git clone https://github.com/ChangooLee/mcp-kr-legislation.git
cd mcp-kr-legislation

# [중요] Python 3.10 이상 사용 필수. 아래 'Python 3.10+ 설치 안내' 참고

# 가상 환경 생성
python3.10 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -e .
```

### 3. 환경변수 설정

`.env` 파일을 생성하고 다음과 같이 설정하세요:

```bash
# 법제처 API 키 (사용자 이메일 ID) - 필수
LEGISLATION_API_KEY=your_email@example.com

# API 기본 URL (기본값 사용 권장)
LEGISLATION_SEARCH_URL=http://www.law.go.kr/DRF/lawSearch.do
LEGISLATION_SERVICE_URL=http://www.law.go.kr/DRF/lawService.do

# MCP 서버 설정
HOST=0.0.0.0
PORT=8000
TRANSPORT=stdio
LOG_LEVEL=INFO
MCP_SERVER_NAME=kr-legislation-mcp
```

> ** API 키 안내:**
> - 법제처 API는 **무료**로 제공됩니다
> - 별도 회원가입이나 신청 절차 없이 **이메일 주소만**으로 사용 가능
> - `LEGISLATION_API_KEY`에는 본인의 실제 이메일 주소를 입력하세요
> - 예: `LEGISLATION_API_KEY=user@gmail.com`

---

## Python 3.10+ 설치 안내

```bash
# Python 버전 확인 (3.10 이상 필요)
python3 --version
```

만약 Python 버전이 3.10 미만이라면, 아래 안내에 따라 Python 3.10 이상을 설치하세요:

### macOS
```bash
# Homebrew 사용
brew install python@3.10

# 또는 공식 웹사이트에서 설치
# https://www.python.org/downloads/macos/
```

### Windows
- [python.org](https://www.python.org/downloads/windows/)에서 설치
- 설치 시 "Add Python to PATH" 체크 필수

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-distutils
```

### Linux (Fedora/CentOS/RHEL)
```bash
sudo dnf install python3.10
```

---

## Claude Desktop 설정

### Claude Desktop 통합

Claude Desktop에서 사용하려면 설정 파일을 수정해야 합니다:

**macOS 설정 파일 위치:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows 설정 파일 위치:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**설정 예시:**
```json
{
  "mcpServers": {
    "mcp-kr-legislation": {
      "command": "/your/path/mcp-kr-legislation/.venv/bin/mcp-kr-legislation",
      "env": {
        "LEGISLATION_API_KEY": "your_email@example.com",
        "PORT": "8000",
        "TRANSPORT": "stdio", 
        "LOG_LEVEL": "INFO",
        "MCP_SERVER_NAME": "KR Legislation MCP"
      }
    }
  }
}
```

> ** 주의사항:**
> - `command` 경로는 실제 설치된 가상환경 경로로 수정하세요
> - `LEGISLATION_API_KEY`는 본인의 이메일 주소를 입력하세요
> - 법제처 API는 무료이며 별도 신청 없이 이메일만으로 사용 가능합니다

---

## 사용 방법

### MCP 서버 직접 실행

```bash
mcp-kr-legislation
```

### Python에서 직접 사용

```python
from mcp_kr_legislation.apis.client import LegislationClient
from mcp_kr_legislation.config import legislation_config

# 클라이언트 초기화
client = LegislationClient(config=legislation_config)

# 법령 검색
result = client.search("law", {"query": "근로기준법"})
print(result)

# 법령 본문 조회
law_info = client.service("law", {"ID": "012345"})
print(law_info)
```

---

##  실제 사용 예시

### 💼 실무 활용 예시

#### 1. 금융사 개인정보 수집 법률 검토
```
질문: "금융사에서 결혼여부를 수집할 수 있는지 관련 법령, 시행령, 금융위 자료를 검토하고 판례가 있으면 조사하여 종합레포트를 작성해줘"

응답 예시:
 API 호출 URL: http://www.law.go.kr/DRF/lawSearch.do?OC=test&type=JSON&target=law&query=개인정보보호법

 '개인정보보호법' 법령 검색 결과
 총 2건 발견

 상세 법령 정보:

1. 개인정보 보호법
    법령구분: 법률
   🏛️ 소관부처: 개인정보보호위원회
    법령ID: 011357
    공포일자: 2011-03-29
    시행일자: 2011-09-30
    상세조회 URL: http://www.law.go.kr/DRF/lawService.do?OC=test&type=JSON&target=law&ID=011357

 추가 안내:
- 더 많은 결과를 보려면 display 파라미터를 늘려서 검색하세요
- 특정 항목의 상세 내용은 해당 ID로 본문 조회 함수를 사용하세요
- API 응답의 전체 데이터는 위 URL로 직접 확인 가능합니다
```

#### 2. 헌법재판소 결정례 검색
```
질문: "표현의 자유 관련 헌법재판소 결정례를 찾아줘"

응답: 헌법재판소 결정례 목록과 각 사건의 상세 링크, 결정 요지 제공
```

#### 3. 행정심판례 검색
```
질문: "개인정보보호법 위반에 대한 행정심판례는?"

응답: 행정심판례 목록과 재결 내용, 당사자 정보 제공
```

### 🔬 심화 분석 질문들

- "최근 5년간 개인정보보호법 개정 내역을 시계열로 분석해줘"
- "금융위원회와 개인정보보호위원회의 개인정보 관련 결정문 차이점을 비교해줘"
- "대학교 학칙에서 개인정보 처리 규정은 어떻게 되어있어?"
- "조세심판원의 개인정보 관련 특별행정심판례가 있어?"

---

##  주의사항

- 법제처 API는 무료 서비스이므로 과도한 요청은 자제해 주세요
- 법령 해석이나 법률 자문이 필요한 경우 전문가와 상담하세요
- 이 도구는 정보 제공 목적이며, 법적 조언을 대체하지 않습니다
- 각 응답에 포함된 API URL을 통해 직접 원본 데이터를 확인할 수 있습니다

---

## 🆘 문제 해결

### 자주 묻는 질문

**Q: API 키 오류가 발생합니다**
A: `LEGISLATION_API_KEY`에 올바른 이메일 주소를 입력했는지 확인하세요.

**Q: 검색 결과가 나오지 않습니다**
A: 검색어를 좀 더 구체적으로 입력해보세요 (예: "근로기준법" 대신 "근로")

**Q: Claude Desktop에서 도구가 보이지 않습니다**
A: 설정 파일의 경로와 환경변수가 올바른지 확인하고 Claude Desktop을 재시작하세요.

**Q: 응답에 URL이 포함되어 있는데 어떻게 사용하나요?**
A: 응답에 포함된 API URL을 브라우저에서 직접 열면 원본 JSON 데이터를 확인할 수 있습니다.

---

##  지원 및 기여

- **GitHub Issues**: [이슈 페이지](https://github.com/ChangooLee/mcp-kr-legislation/issues)
- **기여 방법**: Pull Request를 통한 기여를 환영합니다
- **라이선스**: MIT License

---

**📖 관련 프로젝트**
- [MCP OpenDART](https://github.com/ChangooLee/mcp-opendart) - 한국 금융감독원 전자공시 MCP 서버
- [MCP Korean Real Estate](https://github.com/ChangooLee/mcp-kr-realestate) - 한국 부동산 정보 MCP 서버 
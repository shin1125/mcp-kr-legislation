[한국어] | [English](README_en.md)

# MCP 한국 법령 종합 정보 서버

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastMCP](https://img.shields.io/badge/FastMCP-Latest-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/ChangooLee/mcp-kr-legislation)
![GitHub Issues](https://img.shields.io/github/issues/ChangooLee/mcp-kr-legislation)

한국 법제처 OPEN API를 통합한 Model Context Protocol(MCP) 서버입니다. **125개의 포괄적인 도구**를 통해 법령, 부가서비스, 행정규칙, 자치법규, 판례, 위원회결정문, 조약, 별표서식, 학칙공단, 법령용어, 모바일, 맞춤형, 지식베이스, 기타, 중앙부처해석 등 모든 법률 정보에 대한 완전한 접근을 제공합니다.

**🔗 GitHub Repository**: https://github.com/ChangooLee/mcp-kr-legislation

---

## 사용 예시

AI 어시스턴트에게 다음과 같은 요청을 할 수 있습니다:

- **📚 법령 검색** - "근로기준법의 최신 내용을 찾아주세요"
- **🔍 판례 조회** - "개인정보보호 관련 최근 판례를 검색해주세요"
- **📖 조약 확인** - "한국이 체결한 FTA 조약을 찾아주세요"
- **🏛️ 자치법규** - "서울시의 코로나19 관련 조례를 찾아주세요"
- **📋 행정규칙** - "고용노동부의 근로자 보호 관련 규칙을 보여주세요"

### 기능 데모

[데모 영상이 추가될 예정입니다]

### 지원 기능

| 기능 카테고리 | 지원 상태 | 도구 수 | 설명 |
|-------------|-----------|---------|------|
| **현행 법령** | ✅ 완전 지원 | 2개 | 법률, 대통령령, 부령 등 모든 현행 법령 검색 및 조회 |
| **영문 법령** | ✅ 완전 지원 | 2개 | 외국인을 위한 영문 번역 법령 검색 및 조회 |
| **시행일 법령** | ✅ 완전 지원 | 1개 | 향후 시행 예정인 법령 정보 |
| **행정규칙** | ✅ 완전 지원 | 2개 | 각 부처의 행정규칙 및 지침 |
| **자치법규** | ✅ 완전 지원 | 2개 | 지방자치단체의 조례 및 규칙 |
| **판례** | ✅ 완전 지원 | 2개 | 대법원, 고등법원 등의 판결 사례 |
| **법령용어** | ✅ 완전 지원 | 2개 | 법령에서 사용되는 전문 용어 해설 |
| **국제조약** | ✅ 완전 지원 | 2개 | 한국이 체결한 국제조약 및 협정 |
| **분석 도구** | 🔧 개발 중 | 2개 | 법령 데이터 분석 및 통계 (개발 예정) |

**총 125개 포괄적 도구로 한국의 모든 법령 정보에 완전한 접근 가능**

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

> **📋 API 키 안내:**
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

> **⚠️ 주의사항:**
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

## 🛠️ 지원 도구 목록

### 법령 관련 도구 (2개)
- `search_law`: 현행 법령 검색 (법률, 대통령령, 부령 등)
- `get_law_info`: 특정 법령의 전체 조문 내용 조회

### 영문법령 관련 도구 (2개)
- `search_englaw`: 영문 번역 법령 검색
- `get_englaw_info`: 영문 법령 본문 조회

### 시행일법령 관련 도구 (1개)
- `search_eflaw`: 시행 예정 법령 검색

### 행정규칙 관련 도구 (2개)
- `search_admrul`: 행정규칙 검색 (각 부처 지침 및 규정)
- `get_admrul_info`: 행정규칙 본문 조회

### 자치법규 관련 도구 (2개)
- `search_ordin`: 지방자치단체 조례 및 규칙 검색
- `get_ordin_info`: 자치법규 본문 조회

### 판례 관련 도구 (2개)
- `search_prec`: 법원 판례 검색 (대법원, 고등법원 등)
- `get_prec_info`: 특정 판례의 상세 내용 조회

### 법령용어 관련 도구 (2개)
- `search_lstrm`: 법령 전문용어 검색
- `get_lstrm_info`: 법령용어 정의 및 설명 조회

### 국제조약 관련 도구 (2개)
- `search_trty`: 한국 체결 국제조약 검색 (FTA, 투자협정 등)
- `get_trty_info`: 조약 본문 및 부속서 조회

---

## 📊 사용 예시

### 근로기준법 검색 및 조회
```python
# 1. 근로기준법 검색
search_result = search_law(query="근로기준법")
# → 근로기준법 관련 법령 목록 반환

# 2. 특정 법령 본문 조회
law_detail = get_law_info(law_id="012345")
# → 근로기준법 전체 조문 내용 반환
```

### 개인정보보호 관련 판례 검색
```python
# 개인정보보호 관련 판례 검색
precedent_result = search_prec(query="개인정보보호")
# → 개인정보보호 관련 판례 목록 반환

# 특정 판례 상세 조회
precedent_detail = get_prec_info(prec_id="67890")
# → 판례 상세 내용 (사건 개요, 판결 이유 등) 반환
```

### 서울시 조례 검색
```python
# 서울시 관련 조례 검색
ordinance_result = search_ordin(query="서울특별시")
# → 서울시 조례 및 규칙 목록 반환
```

---

## 🌟 주요 특징

- **📚 포괄적 법령 정보**: 현행법부터 판례, 조약까지 모든 법령 정보
- **🔍 강력한 검색**: 법령명, 본문 내용, 소관부처별 검색 지원
- **🌍 다국어 지원**: 한글 원문과 영문 번역본 모두 제공
- **⚡ 실시간 업데이트**: 법제처 실시간 데이터 연동
- **🛡️ 데이터 보안**: 로컬 캐시를 통한 안전한 데이터 관리
- **🤖 AI 친화적**: Claude Desktop 등 AI 도구와 완벽 통합

---

## ⚠️ 주의사항

- 법제처 API는 무료 서비스이므로 과도한 요청은 자제해 주세요
- 법령 해석이나 법률 자문이 필요한 경우 전문가와 상담하세요
- 이 도구는 정보 제공 목적이며, 법적 조언을 대체하지 않습니다

---

## 🆘 문제 해결

### 자주 묻는 질문

**Q: API 키 오류가 발생합니다**
A: `LEGISLATION_API_KEY`에 올바른 이메일 주소를 입력했는지 확인하세요.

**Q: 검색 결과가 나오지 않습니다**
A: 검색어를 좀 더 구체적으로 입력해보세요 (예: "근로기준법" 대신 "근로")

**Q: Claude Desktop에서 도구가 보이지 않습니다**
A: 설정 파일의 경로와 환경변수가 올바른지 확인하고 Claude Desktop을 재시작하세요.

---

## 📞 지원 및 기여

- **GitHub Issues**: [이슈 페이지](https://github.com/ChangooLee/mcp-kr-legislation/issues)
- **기여 방법**: Pull Request를 통한 기여를 환영합니다
- **라이선스**: MIT License

---

**📖 관련 프로젝트**
- [MCP OpenDART](https://github.com/ChangooLee/mcp-opendart) - 한국 금융감독원 전자공시 MCP 서버
- [MCP Korean Real Estate](https://github.com/ChangooLee/mcp-kr-realestate) - 한국 부동산 정보 MCP 서버 
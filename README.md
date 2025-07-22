[한국어] | [English](README_en.md)

# MCP 법령 종합 정보 서버

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)

> **⚠️ 본 프로젝트는 비상업적(Non-Commercial) 용도로만 사용 가능합니다.**
> 
> This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). Commercial use is strictly prohibited.

![License](https://img.shields.io/github/license/ChangooLee/mcp-kr-legislation)
![GitHub Stars](https://img.shields.io/github/stars/ChangooLee/mcp-kr-legislation)
![GitHub Issues](https://img.shields.io/github/issues/ChangooLee/mcp-kr-legislation)
![GitHub Last Commit](https://img.shields.io/github/last-commit/ChangooLee/mcp-kr-legislation)

한국 법령 종합 정보 제공을 위한 Model Context Protocol(MCP) 서버입니다. 다양한 공공 API를 통합하여 포괄적인 법령 정보 검색과 분석을 지원합니다.

**🔗 GitHub Repository**: https://github.com/ChangooLee/mcp-kr-legislation

---

## 주요 특징

- **📚 다양한 법령 데이터 지원** - 법률, 대통령령, 부령, 조례 등 모든 법령 유형 지원
- **🔍 실시간 법령 검색** - 법제처 법령 API를 통한 최신 법령 정보 제공
- **🌍 전국 단위 지원** - 중앙정부 법령부터 지방자치단체 조례까지 전국 단위 지원
- **🤖 AI 법령 분석** - (개발 예정) 맞춤형 법령 해석 및 분석 리포트 자동 생성
- **📈 고급 분석** - 법령 개정 이력, 관련 법령 연관 분석 등
- **🛡️ 장애 대응 시스템** - API 장애 시 자동 캐시/대체 데이터 활용

---

## 🔰 빠른 시작 (Quick Start)

### 1. Python 3.10+ 설치

#### macOS
```sh
brew install python@3.10
```
#### Windows
- [python.org](https://www.python.org/downloads/windows/)에서 설치, "Add Python to PATH" 체크
#### Linux (Ubuntu)
```sh
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-distutils
```

### 2. 프로젝트 설치

```sh
git clone https://github.com/ChangooLee/mcp-kr-legislation.git
cd mcp-kr-legislation
python3.10 -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install --upgrade pip
pip install -e .
```

### 3. 환경 변수 설정

`.env` 파일 예시:
```env
LEGISLATION_API_KEY=발급받은_법제처_API키
MOLEG_API_KEY=발급받은_법무부_API키
SEOUL_LAW_API_KEY=서울시_법령_API키
LEGAL_INFO_API_KEY=법령정보_API키
HOST=0.0.0.0
PORT=8000
TRANSPORT=stdio
LOG_LEVEL=INFO
```

---

## 🛠️ 실제 사용 예시

### 1. 법령 검색 및 조회

```python
from mcp_kr_legislation.tools.legislation_tools import search_legislation
from mcp_kr_legislation.tools.analysis_tools import analyze_legislation

# 1. 법령 검색 (근로기준법 관련)
result = search_legislation(keyword="근로기준법")
print(result.text)  # 검색 결과 JSON 파일 경로 반환

# 2. 법령 상세 분석 및 리포트 생성
summary = analyze_legislation(file_path=result.text)
print(summary.text)  # 법령 분석 요약 JSON 반환
```

### 2. 법령 개정 이력 조회

```python
from mcp_kr_legislation.tools.analysis_tools import get_legislation_history, analyze_legislation_changes

# 1. 법령 개정 이력 조회
history_result = get_legislation_history(law_name="근로기준법")
print(history_result.text)  # 개정 이력 JSON 파일 경로

# 2. 개정 내용 분석
params = {
    "law_name": "근로기준법",
    "start_date": "20240101",
    "end_date": "20251231"
}
changes_result = analyze_legislation_changes(params)
print(changes_result.text)  # 개정 분석 결과
```

### 3. 캐시/자동갱신/파일경로 활용

- 모든 데이터는 `/src/mcp_kr_legislation/utils/cache/`에 자동 저장/갱신됨
- 분석 도구는 캐시 파일 경로만 반환 → pandas 등으로 직접 로드 가능

---

## 🧰 주요 도구별 사용법

### 법령 검색 도구

| 도구명 | 설명 | 주요 파라미터 | 반환값 |
|--------|------|---------------|--------|
| search_legislation | 법령명/키워드로 법령 검색 | keyword | 검색 결과 JSON 파일 경로 |
| get_legislation_detail | 법령 상세 정보 조회 | law_id | 상세 정보 JSON 파일 경로 |
| get_legislation_text | 법령 전문 조회 | law_id | 법령 전문 텍스트 파일 경로 |

### 법령 분석 도구

| 도구명 | 설명 | 주요 파라미터 | 반환값 |
|--------|------|---------------|--------|
| analyze_legislation | 법령 상세 분석 | file_path | 분석 요약 JSON |
| get_legislation_history | 법령 개정 이력 조회 | law_name | 개정 이력 JSON 파일 경로 |
| analyze_legislation_changes | 개정 내용 분석 | law_name, start_date, end_date | 개정 분석 결과 |
| find_related_legislation | 관련 법령 찾기 | law_id | 관련 법령 목록 JSON |

---

## 🖥️ 멀티플랫폼/IDE/AI 연동

- macOS, Windows, Linux 모두 지원
- Claude Desktop 등 AI IDE 연동:  
  - `"command": "/your/path/.venv/bin/mcp-kr-legislation"`  
  - 환경변수는 `.env` 또는 config에서 지정

---

## ⚠️ 주의/FAQ

- API 키는 반드시 발급 후 `.env`에 저장
- 캐시 파일은 자동 관리, 직접 삭제/갱신 가능
- 데이터가 없거나 분석 실패시 상세 에러 메시지 반환
- 미구현 기능(AI 법령 해석, 자동 리포트 생성 등)은 "개발 예정"으로 표기

---

## 📝 기여/문의/라이선스

### 라이선스

이 프로젝트는 [CC BY-NC 4.0 (비상업적 이용만 허용)](https://creativecommons.org/licenses/by-nc/4.0/) 라이선스를 따릅니다.

- **비상업적, 개인, 연구/학습, 비영리 목적에 한해 사용 가능합니다.**
- **영리기업, 상업적 서비스, 수익 창출 목적의 사용은 엄격히 금지됩니다.**
- 사용 목적이 불분명할 경우 반드시 저작자(Changoo Lee)에게 문의하시기 바랍니다.
- 자세한 내용은 LICENSE 파일과 위 링크를 참고하세요.

> **English:**
> This project is licensed under CC BY-NC 4.0. Use is permitted only for non-commercial, personal, academic/research, or non-profit purposes. Any use by for-profit companies, commercial services, or in any revenue-generating activity is strictly prohibited. See the LICENSE file for details.

---

**프로젝트 관리자**: 이찬구 (Changoo Lee)  
**연락처**: lchangoo@gmail.com  
**GitHub**: https://github.com/ChangooLee/mcp-kr-legislation  
**블로그**: https://changoo.tech  
**LinkedIn**: https://linkedin.com/in/changoo-lee  

**참고**: 이 프로젝트는 공공 API를 활용한 법령 정보 제공 도구로, 법령 해석에 대한 최종 책임은 사용자에게 있습니다. 실제 법적 문제 시에는 전문가와 상담하시기 바랍니다.

**⚠️ 2025년 주요 변경사항**: 일부 API 서비스의 구조 변경으로 인해 기존 코드 수정이 필요할 수 있습니다. 자세한 내용은 [Change Log](https://github.com/ChangooLee/mcp-kr-legislation/blob/main/CHANGELOG.md)를 참조하세요.
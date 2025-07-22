[English] | [한국어](README.md)

# MCP Korean Legislation Information Server

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)

> **⚠️ This project is for non-commercial use only.**
> 
> This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). Commercial use is strictly prohibited.

![License](https://img.shields.io/github/license/ChangooLee/mcp-kr-legislation)
![GitHub Stars](https://img.shields.io/github/stars/ChangooLee/mcp-kr-legislation)
![GitHub Issues](https://img.shields.io/github/issues/ChangooLee/mcp-kr-legislation)
![GitHub Last Commit](https://img.shields.io/github/last-commit/ChangooLee/mcp-kr-legislation)

A Model Context Protocol (MCP) server for comprehensive Korean legislation information. Integrates various public APIs to support comprehensive legislation search and analysis.

**🔗 GitHub Repository**: https://github.com/ChangooLee/mcp-kr-legislation

---

## Key Features

- **📚 Various Legislation Data Support** - Support for all types of legislation including laws, presidential decrees, ministerial ordinances, and local ordinances
- **🔍 Real-time Legislation Search** - Latest legislation information through Ministry of Government Legislation API
- **🌍 Nationwide Coverage** - Support from central government legislation to local government ordinances nationwide
- **🤖 AI Legislation Analysis** - (Under Development) Automated customized legislation interpretation and analysis reports
- **📈 Advanced Analysis** - Legislation revision history, related legislation association analysis, etc.
- **🛡️ Failure Response System** - Automatic cache/alternative data utilization during API failures

---

## 🔰 Quick Start

### 1. Install Python 3.10+

#### macOS
```sh
brew install python@3.10
```
#### Windows
- Install from [python.org](https://www.python.org/downloads/windows/), check "Add Python to PATH"
#### Linux (Ubuntu)
```sh
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-distutils
```

### 2. Project Installation

```sh
git clone https://github.com/ChangooLee/mcp-kr-legislation.git
cd mcp-kr-legislation
python3.10 -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install --upgrade pip
pip install -e .
```

### 3. Environment Variables Setup

`.env` file example:
```env
LEGISLATION_API_KEY=Your_Ministry_of_Legislation_API_Key
MOLEG_API_KEY=Your_Ministry_of_Justice_API_Key
SEOUL_LAW_API_KEY=Seoul_Legislation_API_Key
LEGAL_INFO_API_KEY=Legal_Information_API_Key
HOST=0.0.0.0
PORT=8000
TRANSPORT=stdio
LOG_LEVEL=INFO
```

---

## 🛠️ Usage Examples

### 1. Legislation Search and Inquiry

```python
from mcp_kr_legislation.tools.legislation_tools import search_legislation
from mcp_kr_legislation.tools.analysis_tools import analyze_legislation

# 1. Search legislation (Labor Standards Act related)
result = search_legislation(keyword="Labor Standards Act")
print(result.text)  # Returns search results JSON file path

# 2. Detailed legislation analysis and report generation
summary = analyze_legislation(file_path=result.text)
print(summary.text)  # Returns legislation analysis summary JSON
```

### 2. Legislation Revision History Inquiry

```python
from mcp_kr_legislation.tools.analysis_tools import get_legislation_history, analyze_legislation_changes

# 1. Legislation revision history inquiry
history_result = get_legislation_history(law_name="Labor Standards Act")
print(history_result.text)  # Revision history JSON file path

# 2. Revision content analysis
params = {
    "law_name": "Labor Standards Act",
    "start_date": "20240101",
    "end_date": "20251231"
}
changes_result = analyze_legislation_changes(params)
print(changes_result.text)  # Revision analysis results
```

---

## 🧰 Main Tools Usage

### Legislation Search Tools

| Tool Name | Description | Main Parameters | Return Value |
|-----------|-------------|----------------|--------------|
| search_legislation | Search legislation by name/keyword | keyword | Search results JSON file path |
| get_legislation_detail | Get detailed legislation information | law_id | Detailed information JSON file path |
| get_legislation_text | Get full text of legislation | law_id | Legislation full text file path |

### Legislation Analysis Tools

| Tool Name | Description | Main Parameters | Return Value |
|-----------|-------------|----------------|--------------|
| analyze_legislation | Detailed legislation analysis | file_path | Analysis summary JSON |
| get_legislation_history | Get legislation revision history | law_name | Revision history JSON file path |
| analyze_legislation_changes | Analyze revision content | law_name, start_date, end_date | Revision analysis results |
| find_related_legislation | Find related legislation | law_id | Related legislation list JSON |

---

## 🖥️ Multi-platform/IDE/AI Integration

- Supports macOS, Windows, Linux
- AI IDE integration like Claude Desktop:  
  - `"command": "/your/path/.venv/bin/mcp-kr-legislation"`  
  - Environment variables specified in `.env` or config

---

## ⚠️ Notes/FAQ

- API keys must be issued and stored in `.env`
- Cache files are automatically managed, can be directly deleted/updated
- Detailed error messages returned when data is unavailable or analysis fails
- Unimplemented features (AI legislation interpretation, automatic report generation, etc.) are marked as "Under Development"

---

## 📝 Contribution/Inquiry/License

### License

This project follows the [CC BY-NC 4.0 (Non-commercial use only)](https://creativecommons.org/licenses/by-nc/4.0/) license.

- **Available for non-commercial, personal, research/learning, and non-profit purposes only.**
- **Use by for-profit companies, commercial services, and revenue-generating purposes is strictly prohibited.**
- If the purpose of use is unclear, please contact the author (Changoo Lee).
- For details, refer to the LICENSE file and the link above.

---

**Project Manager**: Changoo Lee  
**Contact**: lchangoo@gmail.com  
**GitHub**: https://github.com/ChangooLee/mcp-kr-legislation  
**Blog**: https://changoo.tech  
**LinkedIn**: https://linkedin.com/in/changoo-lee  

**Note**: This project is a legislation information tool utilizing public APIs, and the final responsibility for legislation interpretation lies with the user. For actual legal issues, please consult with experts.

**⚠️ 2025 Major Changes**: Due to structural changes in some API services, existing code modifications may be necessary. For details, refer to the [Change Log](https://github.com/ChangooLee/mcp-kr-legislation/blob/main/CHANGELOG.md). 
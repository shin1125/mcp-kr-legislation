[한국어](README.md) | English

# MCP Korean Legislation Information Server

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastMCP](https://img.shields.io/badge/FastMCP-Latest-green.svg)
![GitHub Stars](https://img.shields.io/github/stars/ChangooLee/mcp-kr-legislation)
![GitHub Issues](https://img.shields.io/github/issues/ChangooLee/mcp-kr-legislation)

Model Context Protocol (MCP) server integrating Korean Ministry of Legislation OPEN APIs. **125 comprehensive tools** provide complete access to all Korean legal information including laws, additional services, administrative rules, ordinances, precedents, committee decisions, treaties, forms, school regulations, legal terms, mobile services, custom services, knowledge base, miscellaneous, and ministry interpretations.

**🔗 GitHub Repository**: https://github.com/ChangooLee/mcp-kr-legislation

---

## Example Usage

Ask your AI assistant to:

- **📚 Legislation Search** - "Find the latest content of the Labor Standards Act"
- **🔍 Case Search** - "Search for recent cases related to personal information protection"
- **📖 Treaty Lookup** - "Find FTA treaties that Korea has concluded"
- **🏛️ Local Ordinances** - "Find Seoul's ordinances related to COVID-19"
- **📋 Administrative Rules** - "Show me Ministry of Employment and Labor rules for worker protection"

### Feature Demo

[Demo video will be added here]

### Supported Features

| Feature Category | Support Status | Tools | Description |
|-----------------|---------------|-------|-------------|
| **Current Legislation** | ✅ Fully supported | 2 tools | Search and view all current laws, presidential decrees, and ministerial ordinances |
| **English Legislation** | ✅ Fully supported | 2 tools | English translated legislation search and viewing for foreigners |
| **Effective Date Legislation** | ✅ Fully supported | 1 tool | Information on legislation scheduled to take effect |
| **Administrative Rules** | ✅ Fully supported | 2 tools | Administrative rules and guidelines from each ministry |
| **Local Ordinances** | ✅ Fully supported | 2 tools | Local government ordinances and rules |
| **Legal Cases** | ✅ Fully supported | 2 tools | Court cases from Supreme Court, High Courts, etc. |
| **Legal Terms** | ✅ Fully supported | 2 tools | Explanations of professional terms used in legislation |
| **International Treaties** | ✅ Fully supported | 2 tools | International treaties and agreements concluded by Korea |
| **Analysis Tools** | 🔧 Under Development | 2 tools | Legislation data analysis and statistics (planned) |

**Access all Korean legislation information with 125 comprehensive tools**

---

## Quick Start Guide

### 1. API Key Setup

Korean Ministry of Legislation API is **free** and requires only an email address:

1. No registration or application process required
2. Use your email address as the API key
3. Ready to use immediately

### 2. Installation

```bash
# Clone repository
git clone https://github.com/ChangooLee/mcp-kr-legislation.git
cd mcp-kr-legislation

# [IMPORTANT] Python 3.10+ required. See 'Python 3.10+ Installation Guide' below

# Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 3. Environment Variables Setup

Create a `.env` file with the following configuration:

```bash
# Korean Ministry of Legislation API Key (your email) - Required
LEGISLATION_API_KEY=your_email@example.com

# API Base URLs (recommended to use default values)
LEGISLATION_SEARCH_URL=http://www.law.go.kr/DRF/lawSearch.do
LEGISLATION_SERVICE_URL=http://www.law.go.kr/DRF/lawService.do

# MCP Server Configuration
HOST=0.0.0.0
PORT=8000
TRANSPORT=stdio
LOG_LEVEL=INFO
MCP_SERVER_NAME=kr-legislation-mcp
```

> **📋 API Key Information:**
> - The Korean Ministry of Legislation API is **free** to use
> - No registration or application process required - **only email address needed**
> - Enter your actual email address for `LEGISLATION_API_KEY`
> - Example: `LEGISLATION_API_KEY=user@gmail.com`

---

## Python 3.10+ Installation Guide

```bash
# Check Python version (must be 3.10 or higher)
python3 --version
```

If your Python version is lower than 3.10, follow the instructions below:

### macOS
```bash
# Using Homebrew
brew install python@3.10

# Or download from official website
# https://www.python.org/downloads/macos/
```

### Windows
- Download from [python.org](https://www.python.org/downloads/windows/)
- **Must check "Add Python to PATH" during installation**

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

## Claude Desktop Setup

### Claude Desktop Integration

To use with Claude Desktop, you need to modify the configuration file:

**macOS Configuration File Location:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows Configuration File Location:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Configuration Example:**
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

> **⚠️ Important Notes:**
> - Update the `command` path to your actual virtual environment path
> - Replace `LEGISLATION_API_KEY` with your email address
> - The Korean Ministry of Legislation API is free and only requires an email address

---

## Usage

### Direct MCP Server Execution

```bash
mcp-kr-legislation
```

### Direct Use in Python

```python
from mcp_kr_legislation.apis.client import LegislationClient
from mcp_kr_legislation.config import legislation_config

# Initialize client
client = LegislationClient(config=legislation_config)

# Search legislation
result = client.search("law", {"query": "Labor Standards Act"})
print(result)

# Get legislation details
law_info = client.service("law", {"ID": "012345"})
print(law_info)
```

---

## 🛠️ Supported Tools List

### Legislation Tools (2 tools)
- `search_law`: Search current legislation (laws, presidential decrees, ministerial ordinances)
- `get_law_info`: View complete text of specific legislation

### English Legislation Tools (2 tools)
- `search_englaw`: Search English translated legislation
- `get_englaw_info`: View English legislation content

### Effective Date Legislation Tools (1 tool)
- `search_eflaw`: Search legislation scheduled to take effect

### Administrative Rules Tools (2 tools)
- `search_admrul`: Search administrative rules (ministry guidelines and regulations)
- `get_admrul_info`: View administrative rules content

### Local Ordinances Tools (2 tools)
- `search_ordin`: Search local government ordinances and rules
- `get_ordin_info`: View local ordinance content

### Legal Cases Tools (2 tools)
- `search_prec`: Search court cases (Supreme Court, High Courts, etc.)
- `get_prec_info`: View detailed case information

### Legal Terms Tools (2 tools)
- `search_lstrm`: Search professional legal terms
- `get_lstrm_info`: View legal term definitions and explanations

### International Treaties Tools (2 tools)
- `search_trty`: Search international treaties concluded by Korea (FTA, investment agreements, etc.)
- `get_trty_info`: View treaty text and annexes

---

## 📊 Usage Examples

### Labor Standards Act Search and Inquiry
```python
# 1. Search Labor Standards Act
search_result = search_law(query="Labor Standards Act")
# → Returns list of Labor Standards Act related legislation

# 2. View specific legislation content
law_detail = get_law_info(law_id="012345")
# → Returns complete text of Labor Standards Act
```

### Personal Information Protection Case Search
```python
# Search personal information protection related cases
precedent_result = search_prec(query="personal information protection")
# → Returns list of personal information protection related cases

# View specific case details
precedent_detail = get_prec_info(prec_id="67890")
# → Returns detailed case information (case overview, court decision, etc.)
```

### Seoul City Ordinance Search
```python
# Search Seoul City related ordinances
ordinance_result = search_ordin(query="Seoul Metropolitan City")
# → Returns list of Seoul City ordinances and rules
```

---

## 🌟 Key Features

- **📚 Comprehensive Legal Information**: All legislation from current laws to cases and treaties
- **🔍 Powerful Search**: Supports search by legislation name, content, and ministry
- **🌍 Multilingual Support**: Both Korean original and English translations
- **⚡ Real-time Updates**: Real-time data connection with Ministry of Legislation
- **🛡️ Data Security**: Safe data management through local caching
- **🤖 AI-Friendly**: Perfect integration with AI tools like Claude Desktop

---

## ⚠️ Important Notes

- The Ministry of Legislation API is a free service, so please refrain from excessive requests
- Consult with experts for legal interpretation or legal advice
- This tool is for informational purposes and does not replace legal advice

---

## 🆘 Troubleshooting

### Frequently Asked Questions

**Q: API key error occurs**
A: Check if you entered the correct email address in `LEGISLATION_API_KEY`.

**Q: No search results appear**
A: Try more specific search terms (e.g., use "Labor" instead of "Labor Standards Act")

**Q: Tools don't appear in Claude Desktop**
A: Check if the configuration file path and environment variables are correct, then restart Claude Desktop.

---

## 📞 Support and Contribution

- **GitHub Issues**: [Issues Page](https://github.com/ChangooLee/mcp-kr-legislation/issues)
- **How to Contribute**: Contributions via Pull Requests are welcome
- **License**: MIT License

---

**📖 Related Projects**
- [MCP OpenDART](https://github.com/ChangooLee/mcp-opendart) - Korean Financial Supervisory Service Electronic Disclosure MCP Server
- [MCP Korean Real Estate](https://github.com/ChangooLee/mcp-kr-realestate) - Korean Real Estate Information MCP Server 
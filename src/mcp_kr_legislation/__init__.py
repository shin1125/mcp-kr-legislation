# src/mcp_kr_legislation/__init__.py 
import importlib
import click
from mcp_kr_legislation.server import mcp

# 도구 모듈 등록 (모든 @mcp.tool decorator)
for module_name in [
    "legislation_tools",
]:
    importlib.import_module(f"mcp_kr_legislation.tools.{module_name}")

@click.command()
def main():
    """법령 종합 정보 MCP 서버를 실행합니다."""
    mcp.run()

if __name__ == "__main__":
    main() 
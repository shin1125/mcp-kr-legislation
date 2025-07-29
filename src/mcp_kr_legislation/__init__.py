# src/mcp_kr_legislation/__init__.py
import importlib
import click
from mcp_kr_legislation.server import mcp

# 모듈별로 분리된 도구들을 import
# 순서: 기본 법령 도구들부터 순차적으로 import

__all__: list[str] = []

# 도구 모듈 등록 (모든 @mcp.tool decorator)
for module_name in [
    "administrative_rule_tools",     # 행정규칙 및 자치법규 도구들 (8개)
    "precedent_tools",               # 판례 관련 도구들 (8개)
    "committee_tools",               # 위원회 결정문 도구들 (24개)
    "specialized_tools",             # 전문화된 도구들 (조약, 별표서식, 학칙공단, 심판원 등)
    "additional_service_tools",      # 부가서비스 도구들 (지식베이스, FAQ, 상담 등)
    "custom_tools",                  # 맞춤형 도구들 (5개)
    "legal_term_tools",              # 법령용어 도구들 (6개)
    "ai_tools",                      # AI 기반 도구들 (1개)
    "ministry_interpretation_tools", # 중앙부처해석 도구들 (30개+)
    "linkage_tools",                 # 연계정보 도구들 (8개)
    "misc_tools",                    # 기타 도구들
    "legislation_tools",             # 나머지 도구들 (1개)
]:
    try:
        importlib.import_module(f"mcp_kr_legislation.tools.{module_name}")
        print(f"✅ {module_name} 모듈 로드 성공")
    except ImportError as e:
        print(f"⚠️ {module_name} 모듈 로드 실패: {e}")

@click.command()
def main():
    """법령 종합 정보 MCP 서버를 실행합니다."""
    mcp.run()

if __name__ == "__main__":
    main() 
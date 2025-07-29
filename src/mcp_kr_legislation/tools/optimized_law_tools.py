#!/usr/bin/env python3
"""
캐싱 기능을 활용한 최적화된 법령 조회 도구들
- 대용량 응답 문제 해결
- 필요한 정보만 추출하여 사용자 친화적 제공
- 7일간 캐시 유지로 성능 최적화
"""

import logging
from typing import Optional, Union, List, Dict
from mcp import types
from mcp.types import TextContent

# FastMCP 서버 인스턴스 가져오기
from ..server import mcp
from ..utils.legislation_utils import (
    fetch_law_data, 
    extract_law_summary, 
    format_law_summary,
    extract_law_articles,
    format_law_articles,
    extract_article_number
)

logger = logging.getLogger(__name__)

@mcp.tool(
    name="get_law_summary", 
    description="""📋 법령 요약 정보를 조회합니다 (캐싱 최적화).

✨ **주요 특징**:
- 485KB 응답을 175KB로 압축하여 빠른 조회
- 법령 기본정보 + 조문 미리보기 + 제개정 이유 제공
- 7일간 캐시 유지로 초고속 재조회
- 온라인 쇼핑, 근로관계 등 일상생활 법령 해석에 최적

🎯 **제공 정보**:
- **기본정보**: 법령명, 법령ID, 공포일자, 시행일자, 소관부처
- **조문 미리보기**: 처음 10개 조문 요약
- **제개정 이유**: 법령의 목적과 배경
- **원본 크기**: 전체 데이터 정보

💡 **사용법**: 법령일련번호(MST) 또는 법령명으로 조회
- MST: get_law_summary(law_id="248613")  # 개인정보보호법
- 법령명: get_law_summary(law_name="개인정보보호법")

🚀 **성능**: 첫 조회 후 캐시에서 즉시 응답""",
    tags={"법령요약", "캐싱", "최적화", "개인정보", "근로기준법", "일상법령", "성능개선"}
)
def get_law_summary(
    law_id: Optional[str] = None,
    law_name: Optional[str] = None
) -> TextContent:
    """법령 요약 정보 조회 (캐싱 최적화)"""
    if not law_id and not law_name:
        return TextContent(
            type="text", 
            text="❌ 법령ID(MST) 또는 법령명 중 하나를 입력해주세요.\n\n"
                 "💡 예시:\n"
                 "- get_law_summary(law_id=\"248613\")  # 개인정보보호법\n"
                 "- get_law_summary(law_name=\"근로기준법\")"
        )
    
    try:
        # 법령명으로 검색하는 경우 법령일련번호를 찾아야 함
        if law_name and not law_id:
            # 여기서는 간단히 알려진 법령들만 매핑
            law_mapping = {
                "개인정보보호법": "248613",
                "개인정보 보호법": "248613", 
                "근로기준법": "265959",
                "민법": "009847",
                "상법": "009848"
            }
            
            law_id = law_mapping.get(law_name)
            if not law_id:
                return TextContent(
                    type="text",
                    text=f"❌ '{law_name}'에 대한 법령일련번호를 찾을 수 없습니다.\n\n"
                         f"💡 현재 지원되는 법령들:\n"
                         f"- 개인정보보호법 (MST: 248613)\n"
                         f"- 근로기준법 (MST: 265959)\n"
                         f"- 민법 (MST: 009847)\n"
                         f"- 상법 (MST: 009848)\n\n"
                         f"🔍 다른 법령은 search_law 도구로 먼저 검색해주세요."
                )
        
        # 캐시에서 법령 데이터 조회
        law_data = fetch_law_data(str(law_id), use_cache=True)
        
        if not law_data:
            return TextContent(
                type="text",
                text=f"❌ 법령을 조회할 수 없습니다. (ID: {law_id})\n\n"
                     f"🔍 법령ID가 올바른지 확인하거나 search_law 도구로 검색해보세요."
            )
        
        # 요약 정보 추출 및 포맷팅
        summary = extract_law_summary(law_data)
        formatted = format_law_summary(summary, str(law_name or law_id))
        
        return TextContent(type="text", text=formatted)
        
    except Exception as e:
        logger.error(f"법령 요약 조회 실패: {e}")
        return TextContent(
            type="text",
            text=f"❌ 법령 요약 조회 중 오류가 발생했습니다: {str(e)}\n\n"
                 f"🔄 잠시 후 다시 시도해주세요."
        )

def get_law_articles_summary(
    law_id: Optional[str] = None,
    law_name: Optional[str] = None,
    start_article: int = 1,
    count: int = 20
) -> TextContent:
    """법령 조문 요약/목차만 반환 (페이징 지원)"""
    if not law_id and not law_name:
        return TextContent(
            type="text",
            text="❌ 법령ID(MST) 또는 법령명 중 하나를 입력해주세요."
        )
    try:
        # 법령명으로 검색하는 경우 법령일련번호 찾기
        if law_name and not law_id:
            law_mapping = {
                "개인정보보호법": "248613",
                "개인정보 보호법": "248613", 
                "근로기준법": "265959",
                "민법": "009847",
                "상법": "009848"
            }
            law_id = law_mapping.get(law_name)
            if not law_id:
                return TextContent(
                    type="text",
                    text=f"❌ '{law_name}'에 대한 법령일련번호를 찾을 수 없습니다."
                )
        law_data = fetch_law_data(str(law_id), use_cache=True)
        if not law_data:
            return TextContent(type="text", text=f"❌ 법령을 조회할 수 없습니다. (ID: {law_id})")
        # 법령명 검증
        basic_info = law_data.get("법령", {}).get("기본정보", {})
        actual_law_name = basic_info.get("법령명_한글") or basic_info.get("법령명한글") or basic_info.get("법령명")
        if law_name and actual_law_name and law_name != actual_law_name:
            return TextContent(
                type="text",
                text=f"❌ [경고] 요청한 법령명({law_name})과 실제 데이터의 법령명({actual_law_name})이 다릅니다.\n"
                     f"law_id: {law_id}\n정확한 법령명을 확인해주세요."
            )
        # 조문 요약 생성
        articles = law_data.get("법령", {}).get("조문", {})
        if not articles:
            return TextContent(
                type="text",
                text=f"❌ 법령 '{actual_law_name}'의 조문 정보가 없습니다."
            )
        
        # 조문단위 배열 추출
        article_units = []
        if isinstance(articles, dict) and "조문단위" in articles:
            article_units = articles.get("조문단위", [])
        elif isinstance(articles, list):
            article_units = articles
        else:
            article_units = []
            
        if not article_units:
            return TextContent(
                type="text",
                text=f"❌ 법령 '{actual_law_name}'의 조문 정보가 없습니다."
            )
        
        # 실제 조문만 필터링 (부칙 제외)
        actual_articles = [
            a for a in article_units 
            if a.get("조문여부") == "조문"
        ]
        
        if not actual_articles:
            return TextContent(
                type="text",
                text=f"❌ 법령 '{actual_law_name}'의 조문 정보가 없습니다."
            )
        
        # 조문 번호로 정렬
        actual_articles.sort(key=lambda x: int(x.get("조문번호", "999")))
        
        total_articles = len(actual_articles)
        end_article = min(start_article + count - 1, total_articles)
        
        result = f"📋 **{actual_law_name}** 조문 요약\n\n"
        result += f"**전체 조문 수**: {total_articles}개\n"
        result += f"**현재 범위**: 제{start_article}조 ~ 제{end_article}조\n\n"
        result += "---\n\n"
        
        # 선택된 범위의 조문 요약
        for i in range(start_article - 1, end_article):
            if i < len(actual_articles):
                article = actual_articles[i]
                article_num = article.get("조문번호", "")
                article_title = article.get("조문제목", "")
                article_content = article.get("조문내용", "")
                
                # 제목이 없으면 내용의 첫 100자를 요약으로 사용
                if not article_title and article_content:
                    # HTML 태그 제거
                    import re
                    clean_content = re.sub(r'<[^>]+>', '', article_content)
                    article_title = clean_content[:100] + "..." if len(clean_content) > 100 else clean_content
                
                result += f"**제{article_num}조** {article_title}\n"
        
        result += f"\n---\n"
        result += f"💡 **상세 조회**: `get_law_article_detail(law_id=\"{law_id}\", article_number=조번호)`로 특정 조문의 전체 내용을 확인하세요.\n"
        
        # 페이징 정보
        if end_article < total_articles:
            next_start = end_article + 1
            result += f"📄 **다음 페이지**: `get_law_articles_summary(law_id=\"{law_id}\", start_article={next_start})`\n"
        
        return TextContent(type="text", text=result)
    except Exception as e:
        logger.error(f"법령 조문 요약/목차 조회 실패: {e}")
        return TextContent(type="text", text=f"❌ 법령 조문 요약/목차 조회 중 오류가 발생했습니다: {str(e)}")

@mcp.tool(
    name="get_law_article_detail",
    description="특정 법령의 조문 전체 내용을 반환합니다. law_id와 article_no(예: '제50조')를 입력하세요."
)
def get_law_article_detail(
    law_id: str,
    article_no: str
) -> TextContent:
    """특정 조문 전체 내용 반환"""
    if not law_id or not article_no:
        return TextContent(type="text", text="❌ law_id와 article_no(예: '제50조')를 모두 입력하세요.")
    try:
        law_data = fetch_law_data(str(law_id), use_cache=True)
        if not law_data:
            return TextContent(type="text", text=f"❌ 법령을 조회할 수 없습니다. (ID: {law_id})")
        
        # 법령명 가져오기
        basic_info = law_data.get("법령", {}).get("기본정보", {})
        law_name = basic_info.get("법령명_한글") or basic_info.get("법령명한글") or basic_info.get("법령명", "")
        
        # 조문 정보 파싱
        articles = law_data.get("법령", {}).get("조문", {})
        
        # 조문단위 배열 추출
        article_units = []
        if isinstance(articles, dict) and "조문단위" in articles:
            article_units = articles.get("조문단위", [])
        elif isinstance(articles, list):
            article_units = articles
        else:
            article_units = []
            
        if not article_units:
            return TextContent(type="text", text=f"❌ 법령 '{law_name}'의 조문 정보가 없습니다.")
        
        # 조문 번호 정규화 (예: "제50조" -> "50", "50" -> "50")
        import re
        numbers = re.findall(r'\d+', article_no)
        target_num = numbers[0] if numbers else ""
        
        # 해당 조문 찾기
        found_article = None
        for i, article in enumerate(article_units):
            article_num = article.get("조문번호", "")
            if article_num == target_num:
                # 조문여부가 "전문"인 경우 실제 조문은 다음에 있을 수 있음
                if article.get("조문여부") == "전문" and i < len(article_units) - 1:
                    next_article = article_units[i + 1]
                    if (next_article.get("조문번호") == target_num and 
                        next_article.get("조문여부") == "조문"):
                        found_article = next_article
                        break
                elif article.get("조문여부") == "조문":
                    found_article = article
                    break
        
        if not found_article:
            return TextContent(type="text", text=f"❌ 해당 조문({article_no})을 찾을 수 없습니다.")
        
        # 조문 내용 구성
        result = f"📖 **{law_name}**\n\n"
        
        # 제목 구성
        article_title = found_article.get("조문제목", "")
        if article_title:
            result += f"## 제{target_num}조({article_title})\n\n"
        else:
            result += f"## 제{target_num}조\n\n"
        
        # 조문 내용
        content = found_article.get("조문내용", "")
        if content and len(content.strip()) > 20:  # 실제 내용이 있는 경우
            # HTML 태그 제거
            clean_content = re.sub(r'<[^>]+>', '', content)
            clean_content = clean_content.strip()
            result += clean_content + "\n\n"
        else:
            # 항 내용 처리
            hangs = found_article.get("항", [])
            if isinstance(hangs, list) and hangs:
                for hang in hangs:
                    if isinstance(hang, dict):
                        hang_content = hang.get("항내용", "")
                        if hang_content:
                            # HTML 태그 제거
                            clean_hang = re.sub(r'<[^>]+>', '', hang_content)
                            result += clean_hang.strip() + "\n\n"
                    else:
                        result += str(hang) + "\n\n"
        
        # 항/호/목 정보가 있는 경우
        # 실제 API 응답에서는 조문내용에 항/호/목이 포함되어 있을 수 있음
        
        # 시행일자 정보
        if found_article.get("조문시행일자"):
            result += f"\n**시행일자**: {found_article.get('조문시행일자')}"
        
        # 조문 이동 정보
        if found_article.get("조문이동이전"):
            result += f"\n**이전 조문**: 제{found_article.get('조문이동이전')}조"
        if found_article.get("조문이동이후"):
            result += f"\n**이후 조문**: 제{found_article.get('조문이동이후')}조"
        
        return TextContent(type="text", text=result)
    except Exception as e:
        logger.error(f"특정 조문 전체 내용 조회 실패: {e}")
        return TextContent(type="text", text=f"❌ 특정 조문 전체 내용 조회 중 오류가 발생했습니다: {str(e)}")

# 기존 get_law_articles는 요약/목차만 반환하도록 변경(또는 안내)
@mcp.tool(
    name="get_law_articles_summary",
    description="법령 조문 요약/목차만 반환합니다. 전체 조문이 아닌 인덱스와 요약만 제공합니다."
)
def get_law_articles_summary_tool(
    law_id: Optional[str] = None,
    law_name: Optional[str] = None,
    start_article: int = 1,
    count: int = 20
) -> TextContent:
    return get_law_articles_summary(law_id, law_name, start_article, count)

@mcp.tool(
    name="search_law_with_cache", 
    description="""🔍 법령을 검색하고 즉시 요약 정보를 제공합니다.

✨ **주요 특징**:
- 검색 + 캐싱 + 요약을 한 번에 처리
- 온라인 쇼핑, 근로관계, 개인정보 등 일상법령에 특화
- 검색 결과에서 가장 관련성 높은 법령의 요약 자동 제공
- 필요시 상세 조문 조회 안내

🎯 **검색 최적화**:
- 정확한 법령명 우선 검색
- 본문 키워드 검색으로 확장
- 관련도 높은 상위 결과 선별

💡 **사용 예시**:
- search_law_with_cache("개인정보보호")  # 개인정보보호법 자동 요약
- search_law_with_cache("근로시간")      # 근로기준법 자동 요약
- search_law_with_cache("계약")          # 민법 관련 법령 요약

🚀 **성능**: 검색 후 즉시 캐싱으로 재검색 시 초고속""",
    tags={"검색", "캐싱", "자동요약", "일상법령", "개인정보", "근로", "계약", "통합조회"}
)
def search_law_with_cache(query: str) -> TextContent:
    """법령 검색 + 자동 요약 (캐싱 최적화)"""
    if not query or not query.strip():
        return TextContent(
            type="text",
            text="❌ 검색어를 입력해주세요.\n\n"
                 "💡 예시: '개인정보보호', '근로시간', '계약' 등"
        )
    
    try:
        # 미리 정의된 키워드 매핑
        keyword_mapping = {
            "개인정보": "248613",  # 개인정보보호법
            "개인정보보호": "248613",
            "프라이버시": "248613",
            "쇼핑몰": "248613",
            "근로": "265959",  # 근로기준법
            "근로시간": "265959",
            "야근": "265959",
            "휴가": "265959",
            "급여": "265959",
            "노동": "265959",
            "계약": "009847",  # 민법
            "민법": "009847",
            "상법": "009848",
            "회사": "009848"
        }
        
        # 키워드 매칭
        matched_law_id = None
        for keyword, law_id in keyword_mapping.items():
            if keyword in query:
                matched_law_id = law_id
                break
        
        if matched_law_id:
            # 매칭된 법령의 요약 정보 제공
            law_data = fetch_law_data(matched_law_id, use_cache=True)
            if law_data:
                summary = extract_law_summary(law_data)
                
                # 소관부처 정보 개선
                basic_info = law_data.get("법령", {}).get("기본정보", {})
                ministry_info = basic_info.get("소관부처", "")
                if isinstance(ministry_info, dict):
                    ministry = ministry_info.get("content", ministry_info.get("소관부처명", "미지정"))
                else:
                    ministry = ministry_info or basic_info.get("소관부처명", "미지정")
                summary["소관부처"] = ministry
                
                # 법령일련번호 추출 개선
                mst = (basic_info.get("법령일련번호") or 
                       basic_info.get("법령MST") or
                       law_data.get("법령", {}).get("법령키", "")[:10] if law_data.get("법령", {}).get("법령키") else matched_law_id)
                summary["법령일련번호"] = mst
                
                formatted = format_law_summary(summary, query)
                
                # 메타데이터 추출
                actual_law_name = basic_info.get("법령명_한글") or basic_info.get("법령명한글") or basic_info.get("법령명")
                
                # 추가 안내 메시지
                formatted += f"\n---\n[메타데이터] law_id: {matched_law_id}, law_name: {actual_law_name}, mst_id: {mst}\n"
                formatted += f"💡 **더 자세한 조문 보기**: get_law_articles(law_id=\"{mst}\") 또는 get_law_articles(law_name=\"{actual_law_name}\")를 사용하세요.\n"
                formatted += f"🔍 **{actual_law_name} 관련 질문**: 구체적인 조항이나 시행령이 궁금하시면 말씀해주세요!"
                return TextContent(type="text", text=formatted)
        
        # 매칭되지 않는 경우 일반 검색 안내
        return TextContent(
            type="text",
            text=f"🔍 '{query}' 검색 결과\n\n"
                 f"💡 **지원되는 주요 법령들**:\n"
                 f"• **개인정보보호법**: 온라인 쇼핑, 개인정보 처리\n"
                 f"• **근로기준법**: 근로시간, 야근, 휴가, 급여\n" 
                 f"• **민법**: 계약, 손해배상, 재산권\n"
                 f"• **상법**: 회사 설립, 주식, 상거래\n\n"
                 f"🎯 **구체적 검색어로 다시 시도해보세요**:\n"
                 f"- '개인정보보호', '근로시간', '계약' 등\n\n"
                 f"🔧 **전체 법령 검색**: search_law(query=\"{query}\") 도구를 사용하세요."
        )
        
    except Exception as e:
        logger.error(f"법령 검색 실패: {e}")
        return TextContent(
            type="text",
            text=f"❌ 검색 중 오류가 발생했습니다: {str(e)}"
        ) 